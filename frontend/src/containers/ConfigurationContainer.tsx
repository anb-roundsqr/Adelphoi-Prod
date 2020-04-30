/** @jsx jsx */
import { jsx } from "@emotion/core";
import React from "react";
import { connect } from "react-redux";
import { withSnackbar, WithSnackbarProps } from "notistack";
import Tabs from "@material-ui/core/Tabs";
import Paper from "@material-ui/core/Paper";
import Tab from "@material-ui/core/Tab";
import { Switch, Route, Link } from "react-router-dom";
import { AppState } from "../redux-modules/root";
import { ContainerProps } from "./Container";
import * as Types from "../api/definitions";
import * as program from "../redux-modules/program";
import * as programLocation from "../redux-modules/location";
import ProgramList from "../components/ProgramList";
import LocationList from "../components/LocationList";
import ConfigurationForm from "../components/ConfigurationForm";
import { updateConfiguration } from "../api/api";

export interface ConfigurationContainerState {
  isLoading: boolean;
  error: string;
  hasError: boolean;
}

export interface ConfigurationContainerProp
  extends ContainerProps,
    WithSnackbarProps {
  getPrograms: () => Promise<void>;
  createProgram: (program: Types.Program) => Promise<void>;
  updateProgram: (program: Types.Program) => Promise<void>;
  getLocations: () => Promise<void>;
  createLocation: (program: Types.Location) => Promise<void>;
  updateLocation: (program: Types.Location) => Promise<void>;
}

export class ConfigurationContainer extends React.Component<
  ConfigurationContainerProp,
  ConfigurationContainerState
> {
  constructor(props: ConfigurationContainerProp) {
    super(props);
    this.state = this.getInitialState();
  }
  getInitialState() {
    return {
      isLoading: false,
      hasError: false,
      error: "",
      config_update_response: null
    };
  }

  saveConfiguration = async (config: Types.Configuration) => {
    try {
      await updateConfiguration(config);
      this.props.enqueueSnackbar("Configuration Data saved successfully.");
    } catch (error) {
      this.props.enqueueSnackbar(
        "An error occurred while saving configuration"
      );
    }
  };

  componentDidMount() {
    this.props.closeSnackbar();
    this.props.getPrograms();
    this.props.getLocations();
  }

  render() {
    const {
      program: programState,
      createProgram,
      updateProgram,
      programLocation: locationState,
      createLocation,
      updateLocation
    } = this.props;
    const programList = (programState && programState.programList) || [];
    const locationList = (locationState && locationState.locationList) || [];
    const { match, location } = this.props;

    return (
      <Switch>
        <Route path="/configuration">
          <React.Fragment>
            <Paper style={{ flexGrow: 1, marginTop: 30 }}>
              <Tabs value={location.pathname} centered>
                <Tab
                  label="Programs"
                  component={Link}
                  to={`${match.url}/programs`}
                  value={`${match.url}/programs`}
                />
                <Tab
                  label="Locations"
                  component={Link}
                  to={`${match.url}/locations`}
                  value={`${match.url}/locations`}
                />
                <Tab
                  label="Configuration"
                  component={Link}
                  to={`${match.url}/linking`}
                  value={`${match.url}/linking`}
                />
              </Tabs>
            </Paper>
            <Switch>
              <Route path={`${match.url}/programs`}>
                <ProgramList
                  programList={programList}
                  {...this.state}
                  createProgram={createProgram}
                  updateProgram={updateProgram}
                />
              </Route>
              <Route path={`${match.url}/locations`}>
                <LocationList
                  locationList={locationList}
                  {...this.state}
                  createLocation={createLocation}
                  updateLocation={updateLocation}
                />
              </Route>
              <Route path={`${match.url}/linking`}>
                <ConfigurationForm
                  locations={locationList}
                  programs={programList}
                  {...this.state}
                  onFormSubmit={this.saveConfiguration}
                />
              </Route>
              <Route path={`${match.url}`}>
                <div>Programs default page</div>
              </Route>
            </Switch>
          </React.Fragment>
        </Route>
      </Switch>
    );
  }
}

const mapStateToProps = (state: AppState) => {
  return {
    program: state.program,
    programLocation: state.programLocation
  };
};

const mapDispatchToProps = {
  getPrograms: program.actions.getPrograms,
  createProgram: program.actions.createProgram,
  updateProgram: program.actions.updateProgram,
  getLocations: programLocation.actions.getLocations,
  createLocation: programLocation.actions.createLocation,
  updateLocation: programLocation.actions.updateLocation
};

export default connect(
  mapStateToProps,
  mapDispatchToProps
)(withSnackbar(ConfigurationContainer));
