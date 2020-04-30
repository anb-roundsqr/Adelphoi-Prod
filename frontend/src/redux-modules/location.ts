import { ThunkAction } from "redux-thunk";
import { AnyAction } from "redux";
import createReducer from "./createReducer";
import { LocationState } from "./definitions/State";
import { AppState } from "../redux-modules/root";
import * as Types from "../api/definitions";
import { fetchLocationsList, createLocation, updateLocation } from "../api/api";

const initialState: LocationState = {
  locationList: []
};

const { reducer, update } = createReducer<LocationState>(
  "Location/UPDATE",
  initialState
);
export const locationReducer = reducer;

export const actions = {
  update,

  getLocations(): ThunkAction<Promise<void>, AppState, null, AnyAction> {
    return async (dispatch, getState) => {
      const response = await fetchLocationsList();
      if (!response) {
        throw Error("something went wrong getting list of locations");
      }
      dispatch(update({ locationList: response }));
    };
  },

  createLocation(
    location: Types.Location
  ): ThunkAction<Promise<void>, AppState, null, AnyAction> {
    return async (dispatch, getState) => {
      const response = await createLocation(location);
      if (!response) {
        throw Error("something went wrong while creating the location");
      }
      const newLocation: Types.Location = {
        location: response.location_id,
        location_names: location.location_names
      };
      const locationState = getState().programLocation;
      const existingList = locationState ? locationState.locationList : [];
      const locationList = [newLocation, ...existingList];
      dispatch(update({ locationList }));
    };
  },

  updateLocation(
    location: Types.Location
  ): ThunkAction<Promise<void>, AppState, null, AnyAction> {
    return async (dispatch, getState) => {
      const response = await updateLocation(location);
      if (!response) {
        throw Error("something went wrong while updating the location");
      }
      const locationState = getState().programLocation;
      let existingList = locationState ? locationState.locationList : [];
      if (existingList.length > 0) {
        existingList = existingList.filter(
          p => p.location !== location.location
        );
      }
      const locationList = [location, ...existingList];
      dispatch(update({ locationList }));
    };
  },

  clear(): ThunkAction<Promise<void>, AppState, null, AnyAction> {
    return async dispatch => {
      dispatch(update({ locationList: [] }));
    };
  }
};

export const selectors = {
  //
};
