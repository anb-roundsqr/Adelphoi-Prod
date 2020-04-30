/** @jsx jsx */
import React, { useState } from "react";
import { jsx } from "@emotion/core";
import { useHistory } from "react-router-dom";
import { Formik, ErrorMessage, FormikErrors } from "formik";
import Button from "@material-ui/core/Button";
import Backdrop from "@material-ui/core/Backdrop";
import CircularProgress from "@material-ui/core/CircularProgress";
import PictureAsPdfIcon from "@material-ui/icons/PictureAsPdf";
import {
  wrap,
  subHeading,
  fieldRow,
  selectField,
  mainContent,
  twoCol,
  inputField,
  label,
  txtDetail,
  backdrop
} from "./styles";
import Dropdown from "./Dropdown";
import { baseApiUrl } from "../api/api";
import * as Types from "../api/definitions";

interface ProgramSelectionProps {
  client: Types.Client;
  programList: Types.Program[];
  onProgramSelect: (selected_program: string) => void;
  onLocationSelect: (selected_location: string) => Promise<void>;
  submitPrediction: (client: Types.Client) => void;
  isLoading: boolean;
  hasError: boolean;
  error: string;
}

interface FormValues {
  Program: any;
  Confidence: string;
  client_selected_location: string;
}
const ProgramSelection: React.FC<ProgramSelectionProps> = props => {
  const [clientCode, setClientCode] = useState<string | null>(null);
  const history = useHistory();
  const programOptions = props.client.SuggestedPrograms
    ? props.client.SuggestedPrograms.map(p => {
        return {
          label: p,
          value: p,
          predicted: p === props.client.program_type
        };
      })
    : [];

  const getInitialValues = () => {
    const { client } = props;
    let program = null;
    if (client.client_selected_program) {
      program = {
        label: client.client_selected_program,
        value: client.client_selected_program,
        predicted: client.client_selected_program === client.program_type
      };
    }
    return {
      Program: program,
      Confidence: client.Confidence,
      client_selected_location: ""
    };
  };

  const onProgramChange = (program: any) => {
    props.onProgramSelect(program.value);
  };

  return (
    <div css={wrap}>
      <div css={mainContent}>
        <Backdrop css={backdrop} open={props.isLoading}>
          <CircularProgress color="inherit" />
        </Backdrop>
        <h1 css={subHeading}>FM Prediction</h1>
        <Formik
          initialValues={getInitialValues()}
          validate={values => {
            const errors: FormikErrors<FormValues> = {};
            if (!values.client_selected_location) {
              errors.client_selected_location = "Required";
            }
            return errors;
          }}
          enableReinitialize
          onSubmit={async values => {
            const clientCode = props.client.client_code;
            await props.onLocationSelect(values.client_selected_location);
            setClientCode(clientCode);
          }}
        >
          {({ values, handleSubmit, handleChange }) => (
            <form name="submitPredictionForm" onSubmit={handleSubmit}>
              <div css={fieldRow}>
                <div css={twoCol}>
                  <label css={label}>Program</label>
                </div>
                <div css={twoCol}>
                  <Dropdown
                    name="Program"
                    options={programOptions}
                    onChange={onProgramChange}
                    defaultValue={programOptions.find(
                      p => p.value === props.client.client_selected_program
                    )}
                    value={values.Program || null}
                  />
                </div>
              </div>

              <div css={fieldRow}>
                <div css={twoCol}>
                  <label css={label}>Program Completion Likelihood</label>
                </div>
                <div css={twoCol}>
                  <input
                    type="text"
                    readOnly
                    name="Confidence"
                    css={inputField}
                    placeholder=""
                    value={values.Confidence === null ? "" : values.Confidence}
                    onChange={handleChange}
                  />
                  <ErrorMessage component="span" name="Confidence" />
                </div>
              </div>
              <div css={fieldRow}>
                <div css={twoCol}>
                  <label css={label}>Location</label>
                </div>
                <div css={twoCol}>
                  <select
                    css={selectField}
                    name="client_selected_location"
                    value={values.client_selected_location}
                    onChange={handleChange}
                  >
                    <option value="">Select</option>
                    {props.client.SuggestedLocations &&
                      props.client.SuggestedLocations.map(loc => (
                        <option key={loc} value={loc}>
                          {loc}
                        </option>
                      ))}
                  </select>
                  <ErrorMessage
                    component="span"
                    name="client_selected_location"
                  />
                </div>
              </div>
              <div
                css={fieldRow}
                style={{ justifyContent: "flex-end", alignItems: "center" }}
              >
                {clientCode && (
                  <a
                    css={[txtDetail]}
                    style={{ display: "flex", marginRight: 15 }}
                    rel="noopener noreferrer"
                    target="_blank"
                    onClick={() => history.push("/new-client")}
                    href={`${baseApiUrl}/index/${clientCode}`}
                  >
                    <PictureAsPdfIcon /> Download Report
                  </a>
                )}
                <Button
                  type="submit"
                  size="large"
                  variant="contained"
                  color="primary"
                >
                  Submit
                </Button>
              </div>
            </form>
          )}
        </Formik>
      </div>
      {/* MAIN CONTENT */}
    </div>
  );
};

export default ProgramSelection;
