import * as Yup from "yup";
import { searchClient } from "../api/api";

let clientCodeResponse: { [key: number]: boolean } = {};

export const Step1ValidationSchema = Yup.object().shape({
  episode_start: Yup.string()
    .required("Required")
    .nullable(),
  episode_number: Yup.string()
    .required("Required")
    .nullable(),
  CYF_code: Yup.string()
    .required("Required")
    .nullable(),
  primaryRaceCode: Yup.string()
    // .required("Required")
    .nullable(),
  client_code: Yup.number()
    .required("Required")
    .positive()
    .integer()
    .typeError("Invalid. Enter numeric code.")
    .test("is-duplicate", "client code already exists", async value => {
      if (!value) {
        return false;
      }
      if (value in clientCodeResponse) {
        return clientCodeResponse[value];
      }
      const response = await searchClient(value);
      if (response && response.length > 0) {
        clientCodeResponse[value] = false;
        return false;
      }
      clientCodeResponse[value] = true;
      return true;
    })
    .nullable(),
  name: Yup.string()
    .required("Required")
    .nullable(),
  last_name: Yup.string()
    .required("Required")
    .nullable(),
  dob: Yup.string()
    .required("Required")
    .nullable(),
  age: Yup.string()
    .required("Required")
    .nullable(),
  gender: Yup.string()
    .required("Required")
    .nullable(),
  primary_language: Yup.string()
    .required("Required")
    .nullable(),
  ls_type: Yup.string()
    .required("Required")
    .nullable(),
  number_of_prior_placements: Yup.string()
    .required("Required")
    .nullable(),
  number_of_foster_care_placements: Yup.string()
    .required("Required")
    .nullable(),
  number_of_prior_AWOLS: Yup.string()
    .required("Required")
    .nullable(),
  number_of_prior_treatment_terminations: Yup.string()
    .required("Required")
    .nullable(),
  termination_directly_to_AV: Yup.string()
    .required("Required")
    .nullable(),
  length_of_time_since_living_at_home: Yup.string()
    .required("Required")
    .nullable(),
  hist_of_prior_program_SAO: Yup.string()
    .required("Required")
    .nullable(),
  autism_Diagnosis: Yup.string()
    .required("Required")
    .nullable(),
  borderline_Personality: Yup.string()
    .required("Required")
    .nullable(),
  reactive_Attachment_Disorder: Yup.string()
    .required("Required")
    .nullable(),
  animal_cruelty: Yup.string()
    .required("Required")
    .nullable(),
  schizophrenia: Yup.string()
    .required("Required")
    .nullable(),
  psychosis: Yup.string()
    .required("Required")
    .nullable(),
  borderline_IQ: Yup.string()
    .required("Required")
    .nullable(),
  significant_mental_health_symptoms: Yup.number()
    .required("Required")
    .min(0)
    .integer()
    .nullable(),
  prior_hospitalizations: Yup.number()
    .required("Required")
    .min(0)
    .integer()
    .nullable(),
  severe_mental_health_symptoms: Yup.string()
    .required("Required")
    .nullable(),
  compliant_with_meds: Yup.string()
    .required("Required")
    .nullable(),
  Exclusionary_Criteria: Yup.boolean(),

  incarcerated_caregivers: Yup.string()
    .when("Exclusionary_Criteria", {
      is: false,
      then: Yup.string().required("Required"),
      otherwise: Yup.string()
    })
    .nullable(),
  death_Caregiver: Yup.string()
    .when("Exclusionary_Criteria", {
      is: false,
      then: Yup.string().required("Required"),
      otherwise: Yup.string()
    })
    .nullable(),

  incarcerated_siblings: Yup.string()
    .when("Exclusionary_Criteria", {
      is: false,
      then: Yup.string().required("Required"),
      otherwise: Yup.string()
    })
    .nullable(),

  death_Silblings: Yup.string()
    .when("Exclusionary_Criteria", {
      is: false,
      then: Yup.string().required("Required"),
      otherwise: Yup.string()
    })
    .nullable(),

  alcohol_Use: Yup.string()
    .when("Exclusionary_Criteria", {
      is: false,
      then: Yup.string().required("Required"),
      otherwise: Yup.string()
    })
    .nullable(),

  drug_Use: Yup.string()
    .when("Exclusionary_Criteria", {
      is: false,
      then: Yup.string().required("Required"),
      otherwise: Yup.string()
    })
    .nullable(),

  abuse_neglect: Yup.string()
    .when("Exclusionary_Criteria", {
      is: false,
      then: Yup.string().required("Required"),
      otherwise: Yup.string()
    })
    .nullable()
});

// unused - all fields on step2 are optional.
export const Step2ValidationSchema = Yup.object().shape({
  /*yls_FamCircumstances_Score: Yup.string()
    .required("Required")
    .nullable(),
  yls_Edu_Employ_Score: Yup.string()
    .required("Required")
    .nullable(),
  yls_Peer_Score: Yup.string()
    .required("Required")
    .nullable(),
  yls_Subab_Score: Yup.string()
    .required("Required")
    .nullable(),
  yls_Leisure_Score: Yup.string()
    .required("Required")
    .nullable(),
  yls_Personality_Score: Yup.string()
    .required("Required")
    .nullable(),
  yls_Attitude_Score: Yup.string()
    .required("Required")
    .nullable(),
  yls_PriorCurrentOffenses_Score: Yup.string()
    .required("Required")
    .nullable(),
  family_support: Yup.string()
    .required("Required")
    .nullable(),
  fire_setting: Yup.string()
    .required("Required")
    .nullable(),
  level_of_aggression: Yup.string()
    .required("Required")
    .nullable(),
  client_self_harm: Yup.string()
    .required("Required")
    .nullable(),
  Screening_tool_Trauma: Yup.string()
    .required("Required")
    .nullable(),
  cans_LifeFunctioning: Yup.string()
    .required("Required")
    .nullable(),
  cans_YouthStrengths: Yup.string()
    .required("Required")
    .nullable(),
  cans_CareGiverStrengths: Yup.string()
    .required("Required")
    .nullable(),
  cans_Culture: Yup.string()
    .required("Required")
    .nullable(),
  cans_YouthBehavior: Yup.string()
    .required("Required")
    .nullable(),
  cans_YouthRisk: Yup.string()
    .required("Required")
    .nullable(),
  cans_Trauma_Exp: Yup.string()
    .required("Required")
    .nullable()
  referred_program: Yup.string()
    .required("Required")
    .nullable()*/
});

export const ConfigurationSchema = Yup.object().shape({
  gender: Yup.string()
    .required("Required")
    .nullable(),
  program: Yup.string()
    .required("Required")
    .nullable(),
  level_of_care: Yup.string()
    .required("Required")
    .nullable(),
  facility_type: Yup.string()
    .required("Required")
    .nullable(),
  program_model_suggested: Yup.string()
    .required("Required")
    .nullable()
  // program_type: Yup.string()
  //   .required("Required")
  //   .nullable()
});
