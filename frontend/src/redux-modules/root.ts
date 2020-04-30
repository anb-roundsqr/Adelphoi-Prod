import { combineReducers } from "redux";

import { clientReducer } from "./client";
import { programReducer } from "./program";
import { locationReducer } from "./location";

export const rootReducer = combineReducers({
  client: clientReducer,
  program: programReducer,
  programLocation: locationReducer
});

export type AppState = ReturnType<typeof rootReducer>;
