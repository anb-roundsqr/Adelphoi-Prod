import { ThunkAction } from "redux-thunk";
import { AnyAction } from "redux";
import createReducer from "./createReducer";
import { ProgramState } from "./definitions/State";
import { AppState } from "../redux-modules/root";
import * as Types from "../api/definitions";
import {
  fetchPrograms,
  createProgram,
  updateProgram,
  fetchAvailablePrograms
} from "../api/api";

const initialState: ProgramState = {
  programList: [],
  availableProgramList: []
};

const { reducer, update } = createReducer<ProgramState>(
  "Program/UPDATE",
  initialState
);
export const programReducer = reducer;

export const actions = {
  update,

  getPrograms(): ThunkAction<Promise<void>, AppState, null, AnyAction> {
    return async (dispatch, getState) => {
      const response = await fetchPrograms();
      if (!response) {
        throw Error("something went wrong getting list of programs");
      }
      dispatch(update({ programList: response }));
    };
  },

  getAvailablePrograms(): ThunkAction<
    Promise<void>,
    AppState,
    null,
    AnyAction
  > {
    return async (dispatch, getState) => {
      const response = await fetchAvailablePrograms();
      if (!response) {
        throw Error("something went wrong getting list of available programs");
      }
      dispatch(update({ availableProgramList: response }));
    };
  },

  createProgram(
    program: Types.Program
  ): ThunkAction<Promise<void>, AppState, null, AnyAction> {
    return async (dispatch, getState) => {
      const response = await createProgram(program);
      if (!response) {
        throw Error("something went wrong while creating the program");
      }
      const newProgram: Types.Program = {
        program: response.program_id,
        program_name: program.program_name
      };
      const programState = getState().program;
      const existingList = programState ? programState.programList : [];
      const programList = [newProgram, ...existingList];
      dispatch(update({ programList }));
    };
  },

  updateProgram(
    program: Types.Program
  ): ThunkAction<Promise<void>, AppState, null, AnyAction> {
    return async (dispatch, getState) => {
      const response = await updateProgram(program);
      if (!response) {
        throw Error("something went wrong while updating the program");
      }
      const programState = getState().program;
      let existingList = programState ? programState.programList : [];
      if (existingList.length > 0) {
        existingList = existingList.filter(p => p.program !== program.program);
      }
      const programList = [program, ...existingList];
      dispatch(update({ programList }));
    };
  },

  clear(): ThunkAction<Promise<void>, AppState, null, AnyAction> {
    return async dispatch => {
      dispatch(update({ programList: [] }));
    };
  }
};

export const selectors = {
  //
};
