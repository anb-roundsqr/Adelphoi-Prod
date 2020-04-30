/** @jsx jsx */
import React from "react";
import { SnackbarProvider } from "notistack";

import createHistory from "history/createBrowserHistory";
import { Provider } from "react-redux";
//import { PersistGate } from "redux-persist/integration/react";
import configureStore from "./redux-modules/configureStore";

import { css, jsx, Global } from "@emotion/core";
import {
  Switch,
  Route,
  BrowserRouter as Router,
  Redirect
} from "react-router-dom";
import AppShell from "./AppShell";
import NewClientContainer from "./containers/NewClientContainer";
import ExistingClientContainer from "./containers/ExistingClientContainer";
import ConfigurationContainer from "./containers/ConfigurationContainer";

export const { store } = configureStore(createHistory());

const App: React.FC = () => {
  return (
    <React.Fragment>
      <Global
        styles={css`
          *,
          *::before,
          *::after {
            box-sizing: inherit;
          }
          html {
            box-sizing: border-box;
          }
          html,
          body {
            padding: 0;
            margin: 0;
            background: url(img/repeated_bg.png);
            min-height: 100%;
            font-family: "Quicksand", Helvetica, sans-serif;
          }
        `}
      />
      <Provider store={store}>
        <SnackbarProvider
          anchorOrigin={{ vertical: "top", horizontal: "center" }}
        >
          <Router>
            <AppShell>
              <Switch>
                <Route exact path="/">
                  <Redirect to="/new-client" />
                </Route>
                <Route path="/new-client" component={NewClientContainer} />
                <Route
                  path="/existing-client"
                  component={ExistingClientContainer}
                />
                <Route
                  path="/configuration"
                  component={ConfigurationContainer}
                />
              </Switch>
            </AppShell>
          </Router>
        </SnackbarProvider>
      </Provider>
    </React.Fragment>
  );
};

export default App;
