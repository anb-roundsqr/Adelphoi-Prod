// Model definitions

export interface Client {
  client_code: string | null;
  episode_start: string | null;
  episode_number: string | null;
  name: string | null;
  last_name: string | null;
  dob: string | null;
  age: string | null;
  gender: string | null;
  primary_language: string | null;
  RefSourceCode: string | null;
  ls_type: string | null;
  CYF_code: string | null;
  number_of_prior_placements: string | null;
  number_of_foster_care_placements: string | null;
  number_of_prior_AWOLS: string | null;
  number_of_prior_treatment_terminations: string | null;
  termination_directly_to_AV: string | null;
  length_of_time_since_living_at_home: string | null;
  hist_of_prior_program_SAO: string | null;
  autism_Diagnosis: string | null;
  borderline_Personality: string | null;
  reactive_Attachment_Disorder: string | null;
  animal_cruelty: string | null;
  schizophrenia: string | null;
  psychosis: string | null;
  borderline_IQ: string | null;
  significant_mental_health_symptoms: string | null;
  prior_hospitalizations: string | null;
  severe_mental_health_symptoms: string | null;
  compliant_with_meds: string | null;
  Exclusionary_Criteria: boolean;
  incarcerated_caregivers: string | null;
  death_Caregiver: string | null;
  incarcerated_siblings: string | null;
  death_Silblings: string | null;
  alcohol_Use: string | null;
  drug_Use: string | null;
  abuse_neglect: string | null;
  yls_FamCircumstances_Score: string | null;
  yls_Edu_Employ_Score: string | null;
  yls_Peer_Score: string | null;
  yls_Subab_Score: string | null;
  yls_Leisure_Score: string | null;
  yls_Personality_Score: string | null;
  yls_Attitude_Score: string | null;
  yls_PriorCurrentOffenses_Score: string | null;
  family_support: string | null;
  fire_setting: string | null;
  level_of_aggression: string | null;
  client_self_harm: string | null;
  Screening_tool_Trauma: string | null;
  cans_LifeFunctioning: string | null;
  cans_YouthStrengths: string | null;
  cans_CareGiverStrengths: string | null;
  cans_Culture: string | null;
  cans_YouthBehavior: string | null;
  cans_YouthRisk: string | null;
  cans_Trauma_Exp: string | null;
  primaryRaceCode: string | null;
  ageAtEpisodeStart: string | null;
  ageAtEnrollStart: string | null;
  enrollStart_date: string | null;
  english_second_lang: string | null;
  type_of_drugs: string | null;
  FAST_FamilyTogetherScore: string | null;
  FAST_CaregiverAdvocacyScore: string | null;
  Confidence: number | null;
  confidence: number | null;
  Level_of_care: string | null;
  program_type: string | null;
  referred_program: string | null;
  model_program: string | null;
  client_selected_program: string | null;
  client_selected_locations: string | null;
  SuggestedPrograms: string[] | null;
  program_model_suggested: string[] | null;
  selected_program: string | null;
  selected_location: string | null;
  SuggestedLocations: string[] | null;
  result_final: string | null;
  inclusionary_criteria: boolean;
  Program_Completion: number | null;
  Returned_to_Care: number | null;
  program_significantly_modified: number | null;
}

export interface Program {
  program: number;
  program_name: string;
}

export interface Location {
  location: number;
  location_names: string;
}

export interface Configuration {
  gender: number | null;
  program: number | null;
  level_of_care: number | null;
  location: number[] | null;
  facility_type: number | null;
  program_model_suggested: string;
  program_type: string;
}

export interface Prediction {
  Program: string;
  Confidence: number;
  Level_of_care: string;
}

export interface ResultPrograms {
  Program: string;
  Confidence: number;
  Level_of_care: string;
}

export interface SuggestedLocations {
  SuggestedLocations: [string];
}

interface ObjectLiteral {
  [key: string]: any;
}

export const emptyClient: Client = {
  client_code: null,
  episode_start: null,
  episode_number: null,
  name: null,
  last_name: null,
  dob: null,
  age: null,
  gender: null,
  primary_language: null,
  RefSourceCode: null,
  ls_type: null,
  CYF_code: null,
  number_of_prior_placements: null,
  number_of_foster_care_placements: null,
  number_of_prior_AWOLS: null,
  number_of_prior_treatment_terminations: null,
  termination_directly_to_AV: null,
  length_of_time_since_living_at_home: null,
  hist_of_prior_program_SAO: null,
  autism_Diagnosis: null,
  borderline_Personality: null,
  reactive_Attachment_Disorder: null,
  animal_cruelty: null,
  schizophrenia: null,
  psychosis: null,
  borderline_IQ: null,
  significant_mental_health_symptoms: null,
  prior_hospitalizations: null,
  severe_mental_health_symptoms: null,
  compliant_with_meds: null,
  Exclusionary_Criteria: false,
  incarcerated_caregivers: null,
  death_Caregiver: null,
  incarcerated_siblings: null,
  death_Silblings: null,
  alcohol_Use: null,
  drug_Use: null,
  abuse_neglect: null,
  yls_FamCircumstances_Score: null,
  yls_Edu_Employ_Score: null,
  yls_Peer_Score: null,
  yls_Subab_Score: null,
  yls_Leisure_Score: null,
  yls_Personality_Score: null,
  yls_Attitude_Score: null,
  yls_PriorCurrentOffenses_Score: null,
  family_support: null,
  fire_setting: null,
  level_of_aggression: null,
  client_self_harm: null,
  Screening_tool_Trauma: null,
  cans_LifeFunctioning: null,
  cans_YouthStrengths: null,
  cans_CareGiverStrengths: null,
  cans_Culture: null,
  cans_YouthBehavior: null,
  cans_YouthRisk: null,
  cans_Trauma_Exp: null,
  primaryRaceCode: null,
  ageAtEpisodeStart: null,
  ageAtEnrollStart: null,
  enrollStart_date: null,
  english_second_lang: null,
  type_of_drugs: null,
  FAST_FamilyTogetherScore: null,
  FAST_CaregiverAdvocacyScore: null,
  referred_program: null,
  client_selected_program: null,
  client_selected_locations: null,
  program_type: null,
  Confidence: null,
  confidence: null,
  Level_of_care: null,
  SuggestedLocations: null,
  SuggestedPrograms: null,
  model_program: null,
  selected_program: null,
  selected_location: null,
  result_final: null,
  inclusionary_criteria: false,
  Program_Completion: null,
  Returned_to_Care: null,
  program_significantly_modified: null,
  program_model_suggested: null
};

export const emptyConfiguration: Configuration = {
  gender: null,
  program: null,
  level_of_care: null,
  location: [],
  facility_type: null,
  program_model_suggested: "",
  program_type: ""
};

export const primary_language: string[] = ["", "English", "Other"];

export const RefSourceCode: ObjectLiteral = {
  "1": "Adams",
  "2": "Allegheny",
  "3": "Beaver",
  "4": "Bedford",
  "5": "Berks",
  "6": "Blair",
  "7": "Bucks",
  "8": "Butler",
  "9": "Cambria",
  "10": "Centre",
  "11": "Chester",
  "12": "Cumberland",
  "13": "Dauphin",
  "14": "Delaware",
  "15": "Erie",
  "16": "Fayette",
  "17": "Franklin",
  "18": "Huntingdon",
  "19": "Juniata",
  "20": "Kent",
  "21": "Lackawanna",
  "22": "Lancaster",
  "23": "Lebanon",
  "24": "Lehigh",
  "25": "Lycoming",
  "26": "Monroe",
  "27": "Montgomery",
  "28": "Montour",
  "29": "Northumberland",
  "30": "Perry",
  "31": "Philadelphia",
  "32": "Pike",
  "34": "Snyder",
  "35": "Tioga",
  "36": "Washington",
  "37": "Westmoreland",
  "38": "York",
  "39": "Armstrong",
  "40": "Columbia",
  "41": "Crawford",
  "42": "Cayahoga OH",
  "43": "Franklin OH",
  "44": "Greene",
  "45": "Indiana",
  "46": "Lawrence",
  "47": "MH",
  "48": "Mckean",
  "49": "Mercer",
  "50": "outside tri-county",
  "51": "Northampton",
  "52": "Pike",
  "53": "Schukill",
  "54": "Somerset",
  "55": "Union",
  "56": "Venango",
  "57": "Fulton",
  "59": "WV",
  "60": "SE PA"
};

export const ls_type: ObjectLiteral = {
  "1": "Voluntary",
  "2": "Dependant",
  "3": "Voluntary Delinquent",
  "4": "Dependant Delinquent",
  "5": "Delinquent"
};

export const number_of_prior_placements: ObjectLiteral = {
  "0": "None",
  "1": "One",
  "2": "Two",
  "3": "Many"
};

export const number_of_foster_care_placements: ObjectLiteral = {
  "0": "None",
  "1": "One",
  "2": "Two",
  "3": "Many"
};

export const number_of_prior_AWOLS: ObjectLiteral = {
  "0": "None",
  "1": "One",
  "2": "Two",
  "3": "Many"
};

export const number_of_prior_treatment_terminations: ObjectLiteral = {
  "0": "None",
  "1": "One",
  "2": "Two",
  "3": "Many"
};

export const termination_directly_to_AV: ObjectLiteral = {
  "0": "None",
  "1": "Unknown",
  "2": "One",
  "3": "Two or more"
};

export const length_of_time_since_living_at_home: ObjectLiteral = {
  "0": "0-6 months",
  "1": "6-12 months",
  "2": "12+ months"
};

export const gender: ObjectLiteral = {
  "1": "Female",
  "2": "Male"
};

export const radioValues = ["No", "Yes", "", "", "", "", "", "", "", "N/A"];

export const borderline_IQ = ["70+", "<70"];

export const episode_number: ObjectLiteral = {
  "1": "No - Episode 1",
  "2": "Yes - Episode 2",
  "3": "Yes - Episode 3",
  "4": "Yes - Episode 4",
  "5": "Yes - Episode 5",
  "6": "Yes - More than 5 episodes"
};

export const severe_mental_health_symptoms: ObjectLiteral = {
  "0": "No ER/hospitalizations",
  "1": "last 3 months",
  "2": "6 months ago",
  "3": "9 months ago",
  "4": "1 year or more ago"
};

export const CYF_code: ObjectLiteral = {
  "1": "CYF",
  "2": "Juvenile Justice"
};

export const primaryRaceCode: ObjectLiteral = {
  "2": "African American",
  "1": "Caucasian",
  "3": "Hispanic",
  "4": "Other"
};
