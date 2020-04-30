import React from "react";
import { connect } from "react-redux";
import { Switch, Route, RouteComponentProps } from "react-router-dom";
import { withSnackbar, WithSnackbarProps } from "notistack";
import { AppState } from "../redux-modules/root";
import * as program from "../redux-modules/program";
import { ContainerProps } from "./Container";
import * as client from "../redux-modules/client";
import ClientSearch from "../components/ClientSearch";
import ClientDetailsContainer from "./ClientDetailsContainer";

interface MatchParams {
  index: string;
}

interface MatchProps extends RouteComponentProps<MatchParams> {}

export interface ExistingClientContainerState {
  isLoading: boolean;
  error: string;
  hasError: boolean;
  program_completion_response: string | null;
}

export interface ExistingClientContainerProp
  extends ContainerProps,
    WithSnackbarProps {
  searchClient: (client_code: string, client_name: string) => void;
  getAvailablePrograms: () => Promise<void>;
}

export class ExistingClientContainer extends React.Component<
  ExistingClientContainerProp,
  ExistingClientContainerState
> {
  constructor(props: ExistingClientContainerProp) {
    super(props);
    this.state = this.getInitialState();
  }
  getInitialState() {
    return {
      isLoading: false,
      hasError: false,
      error: "",
      program_completion_response: null
    };
  }

  componentDidMount() {
    this.props.closeSnackbar();
    this.props.getAvailablePrograms();
  }

  searchClient = async (client_code: string, client_name: string) => {
    await this.props.searchClient(client_code, client_name);
  };

  render() {
    const { client: clientState, program: programState } = this.props;

    const clientList = (clientState && clientState.clientList) || {};
    // const availableProgramList =
    // (programState && programState.availableProgramList) || [];

    return (
      <Switch>
        <Route exact path="/existing-client">
          <ClientSearch
            clientList={Object.values(clientList)}
            {...this.state}
            onFormSubmit={this.searchClient}
          />
        </Route>
        <Route
          exact
          path="/existing-client/client-details/:index"
          component={ClientDetailsContainer}
        ></Route>
      </Switch>
    );
  }
}

const mapStateToProps = (state: AppState) => {
  return {
    client: state.client,
    program: state.program
  };
};

const mapDispatchToProps = {
  searchClient: client.actions.searchClient,
  getAvailablePrograms: program.actions.getAvailablePrograms
};

export default connect(
  mapStateToProps,
  mapDispatchToProps
)(withSnackbar(ExistingClientContainer));
