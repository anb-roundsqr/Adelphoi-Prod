/** @jsx jsx */
import { jsx, css } from "@emotion/core";
// import { useHistory } from "react-router-dom";
import { Formik, ErrorMessage } from "formik";
import Button from "@material-ui/core/Button";
import Select from "@material-ui/core/Select";
import FormControl from "@material-ui/core/FormControl";
import InputLabel from "@material-ui/core/InputLabel";
import MenuItem from "@material-ui/core/MenuItem";
import Chip from "@material-ui/core/Chip";
import Input from "@material-ui/core/Input";
import { ConfigurationSchema } from "./ValidationSchema";
import {
  wrap,
  // subHeading,
  selectField,
  fieldRow,
  mainContent,
  twoCol,
  inputField,
  fieldBox,
  label
} from "./styles";
import * as Types from "../api/definitions";

const chips = css`
  display: flex;
  flex-wrap: wrap;
`;

const chip = css`
  margin: 2px;
`;

const formControl = css`
  min-width: 98% !important;
`;

interface ConfigurationFormProps {
  programs: Types.Program[];
  locations: Types.Location[];
  onFormSubmit: (configuration: Types.Configuration) => void;
  isLoading: boolean;
  hasError: boolean;
  error: string;
}

const ConfigurationForm: React.FC<ConfigurationFormProps> = props => {
  // const history = useHistory();
  const { programs, locations, onFormSubmit } = props;
  return (
    <div css={wrap}>
      <div css={mainContent}>
        <Formik
          initialValues={Types.emptyConfiguration}
          enableReinitialize
          validationSchema={ConfigurationSchema}
          onSubmit={async (values, helpers) => {
            await onFormSubmit(values);
          }}
        >
          {({ values, handleSubmit, handleChange }) => (
            <form name="configurationForm" onSubmit={handleSubmit}>
              <div css={fieldRow}>
                <div css={twoCol}>
                  <label css={label} style={{ marginTop: 16 }}>
                    Program
                  </label>

                  <select
                    css={selectField}
                    name="program"
                    value={values.program || ""}
                    onChange={handleChange}
                  >
                    <option value="">Select</option>
                    {programs.map(p => (
                      <option key={p.program} value={p.program}>
                        {p.program_name}
                      </option>
                    ))}
                  </select>
                  <ErrorMessage component="span" name="program" />
                </div>
              </div>

              <div css={twoCol}>
                <label css={label}>Sex</label>
                <div css={fieldBox} style={{ width: "48%" }}>
                  <input
                    type="radio"
                    onChange={handleChange}
                    name="gender"
                    id="female"
                    value="1"
                    checked={
                      values.gender && values.gender.toString() === "1"
                        ? true
                        : false
                    }
                  />{" "}
                  <label htmlFor="female">Female</label>
                </div>
                <div css={fieldBox} style={{ width: "48%" }}>
                  <input
                    type="radio"
                    onChange={handleChange}
                    name="gender"
                    id="male"
                    value="2"
                    checked={
                      values.gender && values.gender.toString() === "2"
                        ? true
                        : false
                    }
                  />{" "}
                  <label htmlFor="male">Male</label>
                </div>
                <ErrorMessage component="span" name="gender" />
              </div>

              <div css={fieldRow}>
                <div css={twoCol}>
                  <label css={label}>Level of care</label>
                  <select
                    css={selectField}
                    name="level_of_care"
                    id="level_of_care"
                    value={values.level_of_care || ""}
                    onChange={handleChange}
                  >
                    <option value="">Select</option>
                    <option value="1">Mental health</option>
                    <option value="1">Intensive</option>
                    <option value="3">Independent Living</option>
                  </select>
                  <ErrorMessage component="span" name="level_of_care" />
                </div>
              </div>
              <div css={fieldRow}>
                <div css={twoCol}>
                  <label css={label}>Facility Type</label>
                  <select
                    css={selectField}
                    name="facility_type"
                    id="facility_type"
                    value={values.facility_type || ""}
                    onChange={handleChange}
                  >
                    <option value="">Select</option>
                    <option value="1">Group Home</option>
                    <option value="2">Secure</option>
                  </select>
                  <ErrorMessage component="span" name="facility_type" />
                </div>
              </div>
              <div css={fieldRow}>
                <div css={twoCol}>
                  <label css={label}>Program Name</label>
                  <input
                    css={inputField}
                    name="program_model_suggested"
                    type="text"
                    placeholder=""
                    value={values.program_model_suggested || ""}
                    onChange={handleChange}
                  />
                  <ErrorMessage
                    component="span"
                    name="program_model_suggested"
                  />
                </div>
              </div>
              <div css={fieldRow}>
                <div css={twoCol}>
                  <label css={label}>Program Type (Abbreviation)</label>
                  <input
                    css={inputField}
                    name="program_type"
                    type="text"
                    placeholder=""
                    value={values.program_type || ""}
                    onChange={handleChange}
                  />
                  <ErrorMessage component="span" name="program_type" />
                </div>
              </div>
              <div css={fieldRow}>
                <div css={twoCol}>
                  <label css={label} style={{ marginTop: 16 }}>
                    Locations
                  </label>

                  <FormControl css={formControl}>
                    <InputLabel
                      style={{ padding: 16 }}
                      htmlFor="locations-label"
                    >
                      Select
                    </InputLabel>
                    <Select
                      labelId="locations-label"
                      id="locations"
                      name="location"
                      multiple
                      // css={inputField}
                      style={{
                        padding: 16
                      }}
                      value={values.location}
                      onChange={e => {
                        handleChange(e);
                      }}
                      input={<Input id="locations-input" />}
                      renderValue={selected => (
                        <div css={chips}>
                          {(selected as string[]).map(value => (
                            <Chip
                              key={value}
                              label={
                                locations[Number(value) - 1].location_names
                              }
                              css={chip}
                            />
                          ))}
                        </div>
                      )}
                    >
                      {locations.map(loc => (
                        <MenuItem key={loc.location} value={loc.location}>
                          {loc.location_names}
                        </MenuItem>
                      ))}
                    </Select>
                  </FormControl>
                  <ErrorMessage component="span" name="location" />
                </div>
              </div>

              <div css={fieldRow} style={{ justifyContent: "flex-start" }}>
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

export default ConfigurationForm;
