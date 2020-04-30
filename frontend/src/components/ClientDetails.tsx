/** @jsx jsx */
import { jsx } from "@emotion/core";
import { useState, useEffect } from "react";
import { useParams } from "react-router-dom";
import { format } from "date-fns";
import { Formik, ErrorMessage, FormikErrors } from "formik";
import Button from "@material-ui/core/Button";
import ExpansionPanel from "@material-ui/core/ExpansionPanel";
import ExpansionPanelSummary from "@material-ui/core/ExpansionPanelSummary";
import ExpansionPanelDetails from "@material-ui/core/ExpansionPanelDetails";
import ExpandMoreIcon from "@material-ui/icons/ExpandMore";
import Backdrop from "@material-ui/core/Backdrop";
import CircularProgress from "@material-ui/core/CircularProgress";
import PictureAsPdfIcon from "@material-ui/icons/PictureAsPdf";
import {
  label,
  backdrop,
  selectField,
  subHeading,
  fieldRow,
  inputField,
  twoCol,
  txtLabel,
  panel,
  panelHeading,
  panelHeader,
  txtDetail,
  fieldBox
} from "./styles";
import Dropdown from "./Dropdown";
import * as Types from "../api/definitions";
import { baseApiUrl } from "../api/api";
// import ProgramList from "./ProgramList";

interface ClientDetailsProps {
  client: Types.Client;
  onProgramSelect: (
    client_code: string,
    selected_program: string,
    values: any
  ) => Promise<void>;
  onFormSubmit: (
    client_code: string,
    program_completion: number | null,
    returned_to_care: number | null,
    program_significantly_modified: number,
    Program: string | null,
    Location: string | null
  ) => void;
  isLoading: boolean;
  hasError: boolean;
  error: string;
  program_completion_response: string | null;
}

interface FormValues {
  Program_Completion: string | number | null;
  Returned_to_Care: string | number | null;
  program_significantly_modified: number | string | null;
  Program: any;
  confidence: string;
  Location: any;
}

const ClientDetails: React.FC<ClientDetailsProps> = props => {
  const [predicted_program, setPredictedProgram] = useState<string | null>(
    null
  );

  const [predicted_location, setPredictedLocation] = useState<string | null>(
    null
  );

  useEffect(() => {
    if (
      !predicted_program ||
      predicted_program === props.client.selected_program
    ) {
      setPredictedProgram(props.client.selected_program);
    }
  }, [props.client.selected_program]);

  useEffect(() => {
    if (
      !predicted_location ||
      predicted_location === props.client.selected_location
    ) {
      setPredictedLocation(props.client.selected_location);
    }
  }, [props.client.selected_location]);

  const onProgramChange = (program: any, values: any) => {
    props.onProgramSelect(props.client.client_code!, program.value, values);
  };

  let { index } = useParams();
  if (!index) {
    return <h1 css={subHeading}>No client found</h1>;
  }
  const { client } = props;
  if (!client || !client.client_code) {
    return <h1 css={subHeading}>No client found</h1>;
  }

  const programOptions = props.client.SuggestedPrograms
    ? props.client.SuggestedPrograms.map(p => {
        return {
          label: p,
          value: p,
          predicted: p === predicted_program
        };
      })
    : [];

  const locationOptions = props.client.SuggestedLocations
    ? props.client.SuggestedLocations.map(l => {
        return {
          label: l,
          value: l,
          predicted: l === predicted_location
        };
      })
    : [];
  const getInitialValues = (): FormValues => {
    const { client } = props;
    let program: any = null;
    let location: any = null;
    if (client.selected_program) {
      program = {
        label: client.selected_program,
        value: client.selected_program,
        predicted: client.selected_program === predicted_program
      };
    }
    if (client.selected_location) {
      location = {
        label: client.selected_location,
        value: client.selected_location,
        predicted: client.selected_location === predicted_location
      };
    }
    return {
      Program_Completion:
        client.Program_Completion === null
          ? ""
          : client.Program_Completion.toString(),
      Returned_to_Care:
        client.Returned_to_Care === null
          ? ""
          : client.Returned_to_Care.toString(),
      program_significantly_modified: Number(
        client.program_significantly_modified
      ),
      Program: program,
      confidence:
        client.confidence !== null ? client.confidence.toString() : "",
      Location: location || ""
    };
  };

  return (
    <div>
      <Backdrop css={backdrop} open={props.isLoading}>
        <CircularProgress color="inherit" />
      </Backdrop>
      <div
        style={{
          display: "flex",
          justifyContent: "flex-end",
          textAlign: "right",
          paddingTop: 20,
          paddingBottom: 20
        }}
      >
        <a
          rel="noopener noreferrer"
          target="_blank"
          css={txtDetail}
          href={`${baseApiUrl}/index/${client.client_code}`}
        >
          <PictureAsPdfIcon /> Download Report
        </a>
      </div>
      <ExpansionPanel defaultExpanded>
        <ExpansionPanelSummary
          css={panelHeader}
          expandIcon={<ExpandMoreIcon />}
          aria-controls="panel1a-content"
        >
          <h1 css={panelHeading}>Demographics</h1>
        </ExpansionPanelSummary>
        <ExpansionPanelDetails css={panel}>
          <div css={fieldRow}>
            <div css={twoCol}>
              <label css={txtLabel}>Date of Referral</label>
              <div css={txtDetail}>
                {client.episode_start
                  ? format(new Date(client.episode_start), "MM-dd-yyyy")
                  : ""}
              </div>
            </div>
            <div css={twoCol}>
              <label css={txtLabel}>Previously Referred</label>
              <div css={txtDetail}>
                {Types.episode_number[Number(client.episode_number)]}
              </div>
            </div>
          </div>
          <div css={fieldRow}>
            <div css={twoCol}>
              <label css={txtLabel}>Client Code/ID</label>
              <div css={txtDetail}>{client.client_code}</div>
            </div>
          </div>
          <div css={fieldRow}>
            <div css={twoCol}>
              <label css={txtLabel}>First Name</label>
              <div css={txtDetail}>{client.name}</div>
            </div>
            <div css={twoCol}>
              <label css={txtLabel}>Last Name</label>
              <div css={txtDetail}>{client.last_name}</div>
            </div>
          </div>
          <div css={fieldRow}>
            <div css={twoCol}>
              <label css={txtLabel}>DOB</label>
              <div css={txtDetail}>
                {client.dob ? format(new Date(client.dob), "MM-dd-yyyy") : ""}
              </div>
            </div>
            <div style={{ display: "flex", width: "100%" }}>
              <div css={twoCol}>
                <label css={txtLabel}>Age</label>
                <div css={txtDetail}>{client.age}</div>
              </div>
              <div css={twoCol}>
                <label css={txtLabel}>Sex</label>
                <div css={txtDetail}>
                  {client.gender ? Types.gender[Number(client.gender)] : ""}
                </div>
              </div>
            </div>
          </div>
          <div css={fieldRow}>
            <div css={twoCol}>
              <label css={txtLabel}>Primary Language</label>
              <div css={txtDetail}>
                {Types.primary_language[Number(client.primary_language)]}
              </div>
            </div>
            <div css={twoCol}>
              <label css={txtLabel}>Referral Source</label>
              <div css={txtDetail}>
                {Types.RefSourceCode[Number(client.RefSourceCode)]}
              </div>
            </div>
          </div>
          <div css={fieldRow}>
            <div css={twoCol}>
              <label css={txtLabel}>Legal Status</label>

              <div css={txtDetail}>
                {client.ls_type ? Types.ls_type[client.ls_type] : ""}
              </div>
            </div>
            <div css={twoCol}>
              <label css={txtLabel}>C & Y Involvement</label>

              <div css={txtDetail}>
                {client.CYF_code !== null
                  ? Types.CYF_code[client.CYF_code]
                  : "NA"}
              </div>
            </div>
          </div>
        </ExpansionPanelDetails>
      </ExpansionPanel>

      <ExpansionPanel>
        <ExpansionPanelSummary
          css={panelHeader}
          expandIcon={<ExpandMoreIcon />}
          aria-controls="panel1a-content"
        >
          <h1 css={panelHeading}>Placement History</h1>
        </ExpansionPanelSummary>
        <ExpansionPanelDetails css={panel}>
          <div css={fieldRow}>
            <div css={twoCol}>
              <label css={txtLabel}>Number of prior placements</label>
              <div css={txtDetail}>
                {client.number_of_prior_placements
                  ? Types.number_of_prior_placements[
                      client.number_of_prior_placements
                    ]
                  : "NA"}
              </div>
            </div>
            <div css={twoCol}>
              <label css={txtLabel}>Number of prior foster homes</label>
              <div css={txtDetail}>
                {client.number_of_foster_care_placements !== null
                  ? Types.number_of_foster_care_placements[
                      client.number_of_foster_care_placements
                    ]
                  : ""}
              </div>
            </div>
          </div>
          <div css={fieldRow}>
            <div css={twoCol}>
              <label css={txtLabel}>History of AWOLS</label>
              <div css={txtDetail}>
                {client.number_of_prior_AWOLS !== null
                  ? Types.number_of_prior_AWOLS[client.number_of_prior_AWOLS]
                  : ""}
              </div>
            </div>
            <div css={twoCol}>
              <label css={txtLabel}>Total Prior Placement Terminations</label>
              <div css={txtDetail}>
                {client.number_of_prior_treatment_terminations !== null
                  ? Types.number_of_prior_treatment_terminations[
                      client.number_of_prior_treatment_terminations
                    ]
                  : ""}
              </div>
            </div>
          </div>
          <div css={fieldRow}>
            <div css={twoCol}>
              <label css={txtLabel}>
                Terminations directly before referred
              </label>
              <div css={txtDetail}>
                {client.termination_directly_to_AV !== null
                  ? Types.termination_directly_to_AV[
                      client.termination_directly_to_AV
                    ]
                  : "NA"}
              </div>
            </div>
            <div css={twoCol}>
              <label css={txtLabel}>Time since living at home</label>
              <div css={txtDetail}>
                <div css={txtDetail}>
                  {client.length_of_time_since_living_at_home !== null
                    ? Types.length_of_time_since_living_at_home[
                        client.length_of_time_since_living_at_home
                      ]
                    : ""}
                </div>
              </div>
            </div>
          </div>
          <div css={fieldRow}>
            <div css={twoCol}>
              <label css={txtLabel}>
                Sexually Acting Out behaviors in Placement
              </label>
              <div css={txtDetail}>
                {Types.radioValues[Number(client.hist_of_prior_program_SAO)]}
              </div>
            </div>
          </div>
        </ExpansionPanelDetails>
      </ExpansionPanel>

      <ExpansionPanel>
        <ExpansionPanelSummary
          css={panelHeader}
          expandIcon={<ExpandMoreIcon />}
          aria-controls="panel1a-content"
        >
          <h1 css={panelHeading}>Mental Health</h1>
        </ExpansionPanelSummary>
        <ExpansionPanelDetails css={panel}>
          <div css={fieldRow}>
            <div css={twoCol}>
              <label css={txtLabel}>Autism Dx</label>
              <div css={txtDetail}>
                {Types.radioValues[Number(client.autism_Diagnosis)]}
              </div>
            </div>
            <div css={twoCol}>
              <label css={txtLabel}>Borderline Personality Disorder</label>
              <div css={txtDetail}>
                {Types.radioValues[Number(client.borderline_Personality)]}
              </div>
            </div>
          </div>
          <div css={fieldRow}>
            <div css={twoCol}>
              <label css={txtLabel}>RAD</label>
              <div css={txtDetail}>
                {Types.radioValues[Number(client.reactive_Attachment_Disorder)]}
              </div>
            </div>
            <div css={twoCol}>
              <label css={txtLabel}>Animal Cruelty</label>
              <div css={txtDetail}>
                {Types.radioValues[Number(client.animal_cruelty)]}
              </div>
            </div>
          </div>
          <div css={fieldRow}>
            <div css={twoCol}>
              <label css={txtLabel}>Schizophrenia</label>
              <div css={txtDetail}>
                {Types.radioValues[Number(client.schizophrenia)]}
              </div>
            </div>
            <div css={twoCol}>
              <label css={txtLabel}>Psychosis</label>
              <div css={txtDetail}>
                {Types.radioValues[Number(client.psychosis)]}
              </div>
            </div>
          </div>

          <div css={fieldRow}>
            <div css={twoCol}>
              <label css={txtLabel}>IQ</label>
              <div css={txtDetail}>
                {Types.borderline_IQ[Number(client.borderline_IQ)]}
              </div>
            </div>
          </div>
          <div css={fieldRow}>
            <div css={twoCol}>
              <label css={txtLabel}>Significant MH Symptoms Score</label>
              <div css={txtDetail}>
                {client.significant_mental_health_symptoms}
              </div>
            </div>
            <div css={twoCol}>
              <label css={txtLabel}>Number of Prior MH Hospitalizations</label>
              <div css={txtDetail}>
                {client.prior_hospitalizations !== null
                  ? client.prior_hospitalizations
                  : ""}
              </div>
            </div>
          </div>
          <div css={fieldRow}>
            <div css={twoCol}>
              <label css={txtLabel}>Time since last hospitalization</label>
              <div css={txtDetail}>
                {client.severe_mental_health_symptoms !== null
                  ? Types.severe_mental_health_symptoms[
                      client.severe_mental_health_symptoms
                    ]
                  : ""}
              </div>
            </div>
            <div css={twoCol}>
              <label css={txtLabel}>Medication Compliant</label>
              <div css={txtDetail}>
                {Types.radioValues[Number(client.compliant_with_meds)]}
              </div>
            </div>
          </div>
        </ExpansionPanelDetails>
      </ExpansionPanel>

      <ExpansionPanel>
        <ExpansionPanelSummary
          css={panelHeader}
          expandIcon={<ExpandMoreIcon />}
          aria-controls="panel1a-content"
        >
          <h1 css={panelHeading}>Social/Family Hx</h1>
        </ExpansionPanelSummary>
        <ExpansionPanelDetails css={panel}>
          <div css={fieldRow}>
            <div css={twoCol}>
              <label css={txtLabel}>Incarcerated Caregiver</label>
              <div css={txtDetail}>
                {Types.radioValues[Number(client.incarcerated_caregivers)]}
              </div>
            </div>
            <div css={twoCol}>
              <label css={txtLabel}>Deceased Caregiver</label>
              <div css={txtDetail}>
                {Types.radioValues[Number(client.death_Caregiver)]}
              </div>
            </div>
          </div>
          <div css={fieldRow}>
            <div css={twoCol}>
              <label css={txtLabel}>Incarcerated Siblings</label>
              <div css={txtDetail}>
                {Types.radioValues[Number(client.incarcerated_siblings)]}
              </div>
            </div>
            <div css={twoCol}>
              <label css={txtLabel}>Deceased Siblings</label>
              <div css={txtDetail}>
                {Types.radioValues[Number(client.death_Silblings)]}
              </div>
            </div>
          </div>
          <div css={fieldRow}>
            <div css={twoCol}>
              <label css={txtLabel}>Alcohol Use</label>
              <div css={txtDetail}>
                {Types.radioValues[Number(client.alcohol_Use)]}
              </div>
            </div>
            <div css={twoCol}>
              <label css={txtLabel}>Drug Use</label>
              <div css={txtDetail}>
                {Types.radioValues[Number(client.drug_Use)]}
              </div>
            </div>
          </div>
          <div css={fieldRow}>
            <div css={twoCol}>
              <label css={txtLabel}>Abuse/Neglect</label>
              <div css={txtDetail}>
                {Types.radioValues[Number(client.abuse_neglect)]}
              </div>
            </div>
          </div>
        </ExpansionPanelDetails>
      </ExpansionPanel>

      <ExpansionPanel>
        <ExpansionPanelSummary
          css={panelHeader}
          expandIcon={<ExpandMoreIcon />}
          aria-controls="panel1a-content"
        >
          <h1 css={panelHeading}>Assessment Scores</h1>
        </ExpansionPanelSummary>
        <ExpansionPanelDetails css={panel}>
          <div css={fieldRow}>
            <div css={twoCol}>
              <label css={txtLabel}>YLS Family Circumstances Score</label>
              <div css={txtDetail}>{client.yls_FamCircumstances_Score}</div>
            </div>
          </div>
          <div css={fieldRow}>
            <div css={twoCol}>
              <label css={txtLabel}>YLS Education/Employment Score</label>
              <div css={txtDetail}>{client.yls_Edu_Employ_Score}</div>
            </div>
          </div>
          <div css={fieldRow}>
            <div css={twoCol}>
              <label css={txtLabel}>YLS Peer Score</label>
              <div css={txtDetail}>{client.yls_Peer_Score}</div>
            </div>
          </div>
          <div css={fieldRow}>
            <div css={twoCol}>
              <label css={txtLabel}>YLS Subab Score</label>
              <div css={txtDetail}>{client.yls_Subab_Score}</div>
            </div>
          </div>
          <div css={fieldRow}>
            <div css={twoCol}>
              <label css={txtLabel}>YLS Leisure Score</label>
              <div css={txtDetail}>{client.yls_Leisure_Score}</div>
            </div>
          </div>
          <div css={fieldRow}>
            <div css={twoCol}>
              <label css={txtLabel}>YLS Personality Score</label>
              <div css={txtDetail}>{client.yls_Personality_Score}</div>
            </div>
          </div>
          <div css={fieldRow}>
            <div css={twoCol}>
              <label css={txtLabel}>YLS Attitude Score</label>
              <div css={txtDetail}>{client.yls_Attitude_Score}</div>
            </div>
          </div>
          <div css={fieldRow}>
            <div css={twoCol}>
              <label css={txtLabel}>YLS Prior/Current Offenses Score</label>
              <div css={txtDetail}>{client.yls_PriorCurrentOffenses_Score}</div>
            </div>
          </div>
          <div css={fieldRow}>
            <div css={twoCol}>
              <label css={txtLabel}>Family Support</label>
              <div css={txtDetail}>{client.family_support}</div>
            </div>
          </div>
          <div css={fieldRow}>
            <div css={twoCol}>
              <label css={txtLabel}>Fire Setting</label>
              <div css={txtDetail}>{client.fire_setting}</div>
            </div>
          </div>
          <div css={fieldRow}>
            <div css={twoCol}>
              <label css={txtLabel}>Level of Aggression</label>
              <div css={txtDetail}>{client.level_of_aggression}</div>
            </div>
          </div>
          <div css={fieldRow}>
            <div css={twoCol}>
              <label css={txtLabel}>Self-Harm</label>
              <div css={txtDetail}>{client.client_self_harm}</div>
            </div>
          </div>
          <div css={fieldRow}>
            <div css={twoCol}>
              <label css={txtLabel}>Trauma Assessment Score</label>
              <div css={txtDetail}>{client.Screening_tool_Trauma}</div>
            </div>
          </div>
          <div css={fieldRow}>
            <div css={twoCol}>
              <label css={txtLabel}>CANS Life Functioning</label>
              <div css={txtDetail}>{client.cans_LifeFunctioning}</div>
            </div>
          </div>
          <div css={fieldRow}>
            <div css={twoCol}>
              <label css={txtLabel}>CANS Youth Strengths</label>
              <div css={txtDetail}>{client.cans_YouthStrengths}</div>
            </div>
          </div>
          <div css={fieldRow}>
            <div css={twoCol}>
              <label css={txtLabel}>CANS Caregiver Strengths</label>
              <div css={txtDetail}>{client.cans_CareGiverStrengths}</div>
            </div>
          </div>
          <div css={fieldRow}>
            <div css={twoCol}>
              <label css={txtLabel}>CANS Culture</label>
              <div css={txtDetail}>{client.cans_Culture}</div>
            </div>
          </div>
          <div css={fieldRow}>
            <div css={twoCol}>
              <label css={txtLabel}>CANS Youth Behavior</label>
              <div css={txtDetail}>{client.cans_YouthBehavior}</div>
            </div>
          </div>
          <div css={fieldRow}>
            <div css={twoCol}>
              <label css={txtLabel}>CANS Youth Risk</label>
              <div css={txtDetail}>{client.cans_YouthRisk}</div>
            </div>
          </div>
          <div css={fieldRow}>
            <div css={twoCol}>
              <label css={txtLabel}>CANS Trauma Experience</label>
              <div css={txtDetail}>{client.cans_Trauma_Exp}</div>
            </div>
          </div>
        </ExpansionPanelDetails>
      </ExpansionPanel>

      {/* <h1 css={subHeading}>Referred Program</h1>

      <div css={fieldRow}>
        <div css={twoCol}>
          <div css={txtDetail}>{client.client_selected_program}</div>
        </div>
      </div> */}

      <Formik
        initialValues={getInitialValues()}
        enableReinitialize
        validate={values => {
          const errors: FormikErrors<FormValues> = {};
          if (values.Program !== predicted_program) {
            if (!values.Location) {
              errors.Location = "Required";
            }
          }

          return errors;
        }}
        onSubmit={async (values, helpers) => {
          if (!client.client_code) {
            return false;
          }

          const Program_Completion =
            values.Program_Completion === ""
              ? null
              : Number(values.Program_Completion);
          const Returned_to_Care =
            values.Returned_to_Care === ""
              ? null
              : Number(values.Returned_to_Care);

          await props.onFormSubmit(
            client.client_code,
            Program_Completion,
            Returned_to_Care,
            Number(values.program_significantly_modified),
            values.Program!.value!,
            values.Location!.value!
          );
          // helpers.resetForm();
        }}
      >
        {({ values, handleSubmit, handleChange }) => (
          <form
            name="clientDetailsForm"
            onSubmit={handleSubmit}
            style={{ marginTop: 20 }}
          >
            <div css={fieldRow}>
              <div css={twoCol}>
                <label css={label}>Program</label>
              </div>
              <div css={twoCol}>
                <Dropdown
                  name="Program"
                  disabled={values.Program_Completion !== ""}
                  options={programOptions}
                  onChange={(p: any) => onProgramChange(p, values)}
                  defaultValue={programOptions.find(
                    p => p.value === predicted_program
                  )}
                  value={values.Program || null}
                />
              </div>
            </div>
            <div css={fieldRow}>
              <div css={twoCol}>
                <label css={label}>Location</label>
              </div>
              <div css={twoCol}>
                <Dropdown
                  name="Location"
                  disabled={values.Program_Completion !== ""}
                  options={locationOptions}
                  // onChange={(p: any) => onLocationChange(p, values)}
                  defaultValue={locationOptions.find(
                    l => l.value === predicted_location
                  )}
                  value={values.Location || null}
                />
                {/* <select
                  css={selectField}
                  name="Location"
                  disabled={values.Program_Completion !== ""}
                  value={values.Location}
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
                <ErrorMessage component="span" name="Location" />*/}
              </div>
            </div>
            <div css={fieldRow}>
              <div css={twoCol}>
                <label css={label}>Program Completion Likelihood</label>
              </div>
              <div css={twoCol}>
                <input
                  type="text"
                  name="confidence"
                  readOnly
                  css={inputField}
                  // disabled={Number(values.Program_Completion) === 0}
                  placeholder=""
                  value={values.confidence || ""}
                  onChange={handleChange}
                />
                <ErrorMessage component="span" name="confidence" />
              </div>
            </div>
            <div css={fieldRow}>
              <div css={twoCol}>
                <label css={label}>Program Completion</label>
              </div>
              <div css={twoCol}>
                <select
                  css={selectField}
                  onChange={handleChange}
                  name="Program_Completion"
                  value={
                    values.Program_Completion !== null
                      ? values.Program_Completion.toString()
                      : ""
                  }
                >
                  <option value="">Select</option>
                  <option value="1">Yes</option>
                  <option value="0">No</option>
                </select>
                <ErrorMessage component="span" name="Program_Completion" />
              </div>
            </div>

            <div css={fieldRow}>
              <div css={twoCol}>
                <label css={label} htmlFor="program_significantly_modified">
                  Was the program significantly modified to treat this client?
                </label>
              </div>
              <div css={twoCol}>
                <div css={fieldBox}>
                  <input
                    type="checkbox"
                    disabled={
                      values.Program_Completion !== ""
                        ? values.Program_Completion === "0"
                        : true
                    }
                    onChange={handleChange}
                    name="program_significantly_modified"
                    id="program_significantly_modified"
                    value="true"
                    checked={
                      values.program_significantly_modified !== null
                        ? Number(values.program_significantly_modified) === 1
                        : false
                    }
                  />
                </div>
                <ErrorMessage
                  component="span"
                  name="program_significantly_modified"
                />
              </div>
            </div>
            <div css={fieldRow}>
              <div css={twoCol}>
                <label css={label}>Remained out of care</label>
              </div>
              <div css={twoCol}>
                <select
                  css={selectField}
                  onChange={handleChange}
                  disabled={
                    values.Program_Completion !== ""
                      ? values.Program_Completion === "0"
                      : true
                  }
                  name="Returned_to_Care"
                  value={
                    values.Returned_to_Care !== null
                      ? values.Returned_to_Care.toString()
                      : ""
                  }
                >
                  <option value="">Select</option>
                  <option value="1">Yes</option>
                  <option value="0">No</option>
                </select>
              </div>

              <ErrorMessage component="span" name="Returned_to_Care" />
            </div>

            <div css={fieldRow} style={{ justifyContent: "flex-end" }}>
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
      {props.program_completion_response && (
        <div css={subHeading}>{props.program_completion_response}</div>
      )}
    </div>
  );
};

export default ClientDetails;
