import { History } from "history";
import { applyMiddleware, compose, createStore, Store } from "redux";
import thunk from "redux-thunk";
// import { persistStore, persistReducer, Persistor } from "redux-persist";
// import storage from "redux-persist/lib/storage"; // defaults to localStorage for web
// import { AppState } from "./root";
import { rootReducer } from "./root";

// const persistConfig = {
//   key: "firstMatch",
//   storage
// };

// const persistedReducer = persistReducer(persistConfig, rootReducer);

export default (history: History): { store: Store<any, any> } => {
  // store: Store<any, any>; persistor: Persistor
  let composeEnhancers = compose;
  /* istanbul ignore next */
  if (process.env.NODE_ENV === "development") {
    // https://github.com/zalmoxisus/redux-devtools-extension
    // tslint:disable-next-line:no-any
    composeEnhancers =
      (window as any).__REDUX_DEVTOOLS_EXTENSION_COMPOSE__ || compose;
  }

  const enhancer = composeEnhancers(applyMiddleware(thunk));

  //return createStore<AppState, any, unknown, unknown>(persistedReducer, enhancer as any);

  let store = createStore<any, any, unknown, unknown>(
    rootReducer,
    enhancer as any
  );
  //let persistor = persistStore(store);
  // return { store, persistor };
  return { store };
};
