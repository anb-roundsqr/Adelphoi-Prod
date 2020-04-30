/** @jsx jsx */
import React from "react";
import { jsx, css } from "@emotion/core";
import { withRouter, Route } from "react-router-dom";
import Link from "@material-ui/core/Link";
import Paper from "@material-ui/core/Paper";
import {
  ConfigIcon,
  NewClientIcon,
  ExistingClientIcon
} from "./components/icons";

const App = css`
  margin: 80px auto;
  width: 100%;
  background-color: #fff;
  padding: 16px;
  position: relative;
  @media all and (min-width: 520px) {
    padding: 40px;
    margin: 100px auto;
    width: 60vw;
  }
  @media all and (min-width: 520px) and (max-width: 1024px) {
    width: 90vw;
  }
`;

const nav = css`
  display: flex;
  flex-direction: row;
  align-items: center;
  justify-content: center;
  font-weight: bold;
  margin-top: 50px;
  @media all and (min-width: 520px) {
    flex-direction: row;
    align-items: flex-start;
    justify-content: center;
  }
`;

const menuButton = css`
  width: 260px;
  height: 140px;
  @media all and (max-width: 520px) {
    width: 110px;
    height: 80px;
    font-size: 12px !important;
  }
  @media all and (max-width: 768px) {
    font-size: 16px;
  }
  cursor: pointer;
  align-items: center;
  justify-content: center;
  text-decoration: none;
  text-transform: uppercase;
  display: flex;
  flex-direction: column;
  border-radius: 4px !important;
  font-size: 26px;
  color: #9c9c9c;
  @media all and (min-width: 520px) {
    &:not(:last-child) {
      border-right: 2px solid #c4c4c4 !important;
    }
  }
`;
const menuIcon = css`
  font-size: 72px !important;
  margin-bottom: 8px;
  @media all and (max-width: 520px) {
    font-size: 36px !important;
  }
`;

const logo = css`
  position: relative;
`;

const firstMatchLogo = css`
  position: absolute;
  transform: translate(-50%, -50%);
  left: 50%;
  top: -50px;
  @media all and (max-width: 520px) {
    width: 140px;
  }
`;

const adelphoiLogo = css`
  position: absolute;
  top: -25px;
  right: -25px;
  @media all and (max-width: 520px) {
    top: 0;
    right: 0;
  }
`;

const AppShell: React.FC = ({ children }) => {
  return (
    <Paper css={App} elevation={3}>
      <div css={logo}>
        <img
          css={firstMatchLogo}
          alt="First Match Logo"
          src="/img/logo_stroke.png"
        />
        <img
          css={adelphoiLogo}
          alt="Adelphoi Logo"
          src="/img/adelphoi_logo.png"
        />
      </div>
      <div css={nav}>
        <Route
          path="/new-client"
          // exact={activeOnlyWhenExact}
          children={({ match, history }) => (
            <Link
              onClick={() => {
                history.push("/new-client");
              }}
              href="#"
              css={menuButton}
              style={
                match
                  ? { backgroundColor: "#8284e5", color: "white" }
                  : { backgroundColor: "#f5f5f5", color: "#9d9d9d" }
              }
            >
              <NewClientIcon
                css={menuIcon}
                fillColor={match ? "white" : "#9d9d9d"}
              />
              New Client
            </Link>
          )}
        />

        <Route
          path="/existing-client"
          // exact={activeOnlyWhenExact}
          children={({ match, history }) => (
            <Link
              onClick={() => {
                history.push("/existing-client");
              }}
              css={menuButton}
              style={
                match
                  ? { backgroundColor: "#8284e5", color: "white" }
                  : { backgroundColor: "#f5f5f5", color: "#9d9d9d" }
              }
            >
              <ExistingClientIcon
                css={menuIcon}
                fillColor={match ? "white" : "#9d9d9d"}
              />
              Existing Client
            </Link>
          )}
        />
        <Route
          path="/configuration"
          // exact={activeOnlyWhenExact}
          children={({ match, history }) => (
            <Link
              onClick={() => {
                history.push("/configuration/programs");
              }}
              css={menuButton}
              style={
                match
                  ? { backgroundColor: "#8284e5", color: "white" }
                  : { backgroundColor: "#f5f5f5", color: "#9d9d9d" }
              }
            >
              <ConfigIcon
                css={menuIcon}
                fillColor={match ? "white" : "#9d9d9d"}
              />
              Configuration
            </Link>
          )}
        />
      </div>
      {children}
    </Paper>
  );
};

export default withRouter(AppShell);
