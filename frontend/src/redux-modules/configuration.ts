import { ThunkAction } from "redux-thunk";
import { AnyAction } from "redux";
import createReducer from "./createReducer";
import { ConfigurationState } from "./definitions/State";
import { AppState } from "../redux-modules/root";
import * as Types from "../api/definitions";
import { updateConfiguration } from "../api/api";

const initialState: ConfigurationState = {
  configuration: Types.emptyConfiguration
};

const { reducer, update } = createReducer<ConfigurationState>(
  "Configuration/UPDATE",
  initialState
);
export const configurationReducer = reducer;

export const actions = {
  update,

  updateConfiguration(
    configuration: Types.Configuration
  ): ThunkAction<Promise<string>, AppState, null, AnyAction> {
    return async (dispatch, getState) => {
      const response = await updateConfiguration(configuration);
      if (!response) {
        throw Error("something went wrong while saving the client");
      }
      dispatch(update({ configuration }));
      return response;
    };
  },

  // upsertConfiguration: (
  //   client: Types.Configuration
  // ): ThunkAction<void, AppState, void, any> => {
  //   const newCl = {
  //     ...client,
  //     primaryRaceCode: "1",
  //     ageAtEpisodeStart: "1",
  //     ageAtEnrollStart: "1",
  //     english_second_lang: "1",
  //     enrollStart_date: null,
  //     type_of_drugs: "aaa",
  //     FAST_FamilyTogetherScore: "0",
  //     FAST_CaregiverAdvocacyScore: "0"
  //   };
  //   return (dispatch, getState) => {
  //     dispatch(update({ client: newCl }));
  //   };
  // },

  clear(): ThunkAction<Promise<void>, AppState, null, AnyAction> {
    return async dispatch => {
      dispatch(update({ configuration: Types.emptyConfiguration }));
    };
  }
};

export const selectors = {
  //
};
