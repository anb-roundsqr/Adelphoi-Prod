import React from "react";
import { connect } from "react-redux";
import { withSnackbar, WithSnackbarProps } from "notistack";
import { wrap, mainContent } from "../components/styles";
import { AppState } from "../redux-modules/root";
import * as program from "../redux-modules/program";
import { ContainerProps } from "./Container";
import * as client from "../redux-modules/client";
import * as Types from "../api/definitions";
import ClientDetails from "../components/ClientDetails";

interface MatchParams {
  index: string;
}

export interface ClientDetailsContainerState {
  isLoading: boolean;
  error: string;
  hasError: boolean;
  program_completion_response: string | null;
}

export interface ClientDetailsContainerProps
  extends ContainerProps<MatchParams>,
    WithSnackbarProps {
  searchClient: (client_code: string, client_name: string) => Promise<void>;
  updateProgramCompletion: (
    client_code: string,
    program_completion: number | null,
    returned_to_care: number | null,
    program_significantly_modified: number,
    program: string | null,
    location: string | null
  ) => Promise<string>;
  getAvailablePrograms: () => Promise<void>;
  submitPrediction: (client: Types.Client) => Promise<void>;
  getLocations: (
    client_code: string,
    selected_program: string
  ) => Promise<void>;
  getPcr: (client_code: string, selected_program: string) => Promise<void>;
  saveLocationAndProgram: (
    selected_location: string,
    selected_program: string,
    client_code: string
  ) => Promise<void>;
  clearErrors: () => void;
  clearClient: () => void;
  getProgramsForClient: (client_code: string) => Promise<void>;
  updateFormValues: (client_code: string, values: any) => void;
}

export class ClientDetailsContainer extends React.Component<
  ClientDetailsContainerProps,
  ClientDetailsContainerState
> {
  constructor(props: ClientDetailsContainerProps) {
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

  async componentDidMount() {
    const { client: clientState } = this.props;
    const clientList = (clientState && clientState.clientList) || {};
    const { index } = this.props.match.params;
    this.setState({ isLoading: true });

    if (!clientList[index]) {
      await this.searchClient(index, "");
    }
    // fetch program for this client
    await this.props.getProgramsForClient(index);
    this.setState({ isLoading: false });
    this.props.closeSnackbar();
    this.props.getAvailablePrograms();
  }

  searchClient = async (client_code: string, client_name: string) => {
    await this.props.searchClient(client_code, client_name);
  };

  updateProgramCompletion = async (
    client_code: string,
    program_completion: number | null,
    returned_to_care: number | null,
    program_significantly_modified: number,
    program: string | null,
    location: string | null
  ) => {
    try {
      this.setState({ isLoading: true });

      const response = await this.props.updateProgramCompletion(
        client_code,
        program_completion,
        returned_to_care,
        program_significantly_modified,
        program,
        location
      );
      this.setState({
        isLoading: false
        // program_completion_response: response
      });
      this.props.enqueueSnackbar("Data saved successfully.");
    } catch (error) {
      this.setState({
        isLoading: false
        // program_completion_response: "An error occured. Please try again."
      });
      this.props.enqueueSnackbar("An error occured. Please try again.");
    }
  };

  getLocationsAndPcr = async (
    client_code: string,
    selected_program: string,
    values: any
  ) => {
    this.setState({ isLoading: true });
    await this.props.getPcr(client_code, selected_program);
    await this.props.getLocations(client_code, selected_program);
    this.props.updateFormValues(client_code, values);
    this.setState({ isLoading: false });
  };

  submitProgram = async (client: Types.Client) => {
    // const { client: clientState } = this.props;
    // if (!clientState || !clientState.client) {
    //   return false;
    // }
    if (!client.client_code) {
      this.props.enqueueSnackbar(
        "Error. Client information is required to process this form."
      );
      return false;
    }
    try {
      this.setState({ isLoading: true });
      await this.props.submitPrediction(client);
    } catch (error) {
      let errorMessage: string = "An error occurred while saving.";
      if (error["referred_program"]) {
        errorMessage = error["referred_program"][0];
      } else if (error.message) {
        errorMessage = error.message;
      }
      this.props.enqueueSnackbar(errorMessage);
    }
    this.setState({ isLoading: false });
  };

  // saveProgramAndLocation = async (selected_location: string) => {
  //   // const { history } = this.props;
  //   const { client: clientState } = this.props;
  //   if (!clientState || !clientState.client) {
  //     this.props.enqueueSnackbar("Error. Client info not available.");
  //     return;
  //   }
  //   this.setState({ isLoading: true });
  //   await this.props.saveLocationAndProgram(selected_location);
  //   this.setState({ isLoading: false });
  //   this.props.clearClient();
  //   this.props.enqueueSnackbar("Data saved successfully.");
  // };

  render() {
    const { client: clientState } = this.props;
    const clientList = (clientState && clientState.clientList) || {};
    const { index } = this.props.match.params;
    return (
      <div css={wrap}>
        <div css={mainContent}>
          {!clientList[index] ? null : (
            <ClientDetails
              client={clientList[index]}
              onProgramSelect={this.getLocationsAndPcr}
              // onLocationSelect={this.saveProgramAndLocation}
              {...this.state}
              onFormSubmit={this.updateProgramCompletion}
              program_completion_response={
                this.state.program_completion_response
              }
            />
          )}
        </div>
      </div>
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
  updateProgramCompletion: client.actions.updateProgramCompletion,
  getAvailablePrograms: program.actions.getAvailablePrograms,
  submitPrediction: client.actions.submitPrediction,
  getLocations: client.actions.getLocations,
  getPcr: client.actions.getPcr,
  saveLocationAndProgram: client.actions.saveLocationAndProgram,
  clearErrors: client.actions.clearErrors,
  clearClient: client.actions.clear,
  getProgramsForClient: client.actions.getProgramsForClient,
  updateFormValues: client.actions.updateFormValues
};

export default connect(
  mapStateToProps,
  mapDispatchToProps
)(withSnackbar(ClientDetailsContainer));
