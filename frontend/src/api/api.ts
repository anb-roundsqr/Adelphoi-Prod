import axios from "axios";
import * as Types from "./definitions";

export const baseApiUrl = "http://13.233.251.14:8000/first_match";

interface PredictionResponse {
  referred_program: string;
  model_program: string;
}

interface LocationsResponse {
  result?: string;
  "Suggested Locations": string[];
}

export const updateConfiguration = async (
  configuration: Types.Configuration
) => {
  try {
    const response = await axios.post(`${baseApiUrl}/dataSave`, configuration);
    return response.data.data;
  } catch (error) {
    console.error("api function updateConfiguration error");
    throwError(error);
  }
};

export const insertClient = async (client: Types.Client) => {
  try {
    const response = await axios.post(`${baseApiUrl}/list_view/`, client);
    if (response.data["ERROR"] && response.data["ERROR"].trim() !== "") {
      throw new Error(response.data["ERROR"]);
    }
    if (response.data["Result"] && response.data["Result"].trim() !== "") {
      return response.data;
    }
    const r = {
      ...response.data,
      program_type: response.data.program_type[0],
      referred_program: response.data.program_type[0],
      model_program: response.data.program_type[0]
    };

    return (r as unknown) as Partial<Types.Client>;
  } catch (error) {
    const data = error.response.data;
    let clientErrors: { [x: string]: any } = {};
    Object.keys(data).map(key => {
      return (clientErrors[key] = data[key][0]);
    });
    console.error("api function insertClient error");
    console.log(clientErrors);
    throw clientErrors;
  }
};

export const insertPrediction = async (client: Types.Client) => {
  if (!client.client_code) {
    throw new Error("client code required");
  }
  try {
    const response = await axios.put(
      `${baseApiUrl}/refer/${client.client_code}/`,
      { referred_program: client.program_type }
    );
    return response;
  } catch (error) {
    console.error("api function insertPrediction error");
    throwError(error);
  }
};

export const fetchPrograms = async () => {
  try {
    const response = await axios.get(`${baseApiUrl}/program_list`);
    const data = (response.data as unknown) as Types.Program[];

    return data;
  } catch (error) {
    console.error("api function fetchPrograms error");
    throwError(error);
  }
};

export const fetchAvailablePrograms = async () => {
  try {
    const response = await axios.get(`${baseApiUrl}/available_programs`);
    const data = (response.data as unknown) as Types.Program[];

    return data;
  } catch (error) {
    console.error("api function fetchAvailablePrograms error");
    throwError(error);
  }
};

export const createProgram = async (program: Types.Program) => {
  try {
    const response = await axios.post(`${baseApiUrl}/program_save`, {
      program_name: program.program_name
    });
    return response.data;
  } catch (error) {
    console.error("api function createProgram error");
    throwError(error);
  }
};

export const updateProgram = async (program: Types.Program) => {
  try {
    const response = await axios.put(
      `${baseApiUrl}/programs/${program.program}/`,
      {
        program_name: program.program_name
      }
    );
    return response.data;
  } catch (error) {
    console.error("api function updateProgram error");
    throwError(error);
  }
};

export const fetchLocationsList = async () => {
  try {
    const response = await axios.get(`${baseApiUrl}/location_list`);
    const data = (response.data as unknown) as Types.Location[];

    return data;
  } catch (error) {
    console.error("api function fetchLocationsList error");
    throwError(error);
  }
};

export const createLocation = async (location: Types.Location) => {
  try {
    const response = await axios.post(`${baseApiUrl}/location_save`, {
      location_name: location.location_names
    });
    return response.data;
  } catch (error) {
    console.error("api function createLocation error");
    throwError(error);
  }
};

export const updateLocation = async (location: Types.Location) => {
  try {
    const response = await axios.put(
      `${baseApiUrl}/locations/${location.location}/`,
      {
        location_names: location.location_names
      }
    );
    return response.data;
  } catch (error) {
    console.error("api function updateLocation error");
    throwError(error);
  }
};

export const fetchLocations = async (
  client_code: string,
  referred_program: string
) => {
  try {
    const response = await axios.get(
      `${baseApiUrl}/location/${client_code}?referred_program=${referred_program}`
    );
    const data = (response.data as unknown) as LocationsResponse;
    return data;
    // return data["Suggested Locations"];
  } catch (error) {
    console.error("api function fetchLocations error");
    throwError(error);
  }
};

export const fetchPcr = async (
  client_code: string,
  referred_program: string
) => {
  try {
    const response = await axios.put(
      `${baseApiUrl}/program_pcr/${client_code}/`,
      { client_selected_program: referred_program }
    );
    const data = (response.data as unknown) as any;
    return data;
  } catch (error) {
    console.error("api function fetch program_pcr error");
    throwError(error);
  }
};

export const saveLocationAndProgram = async (
  client_code: string,
  selected_program: string,
  selected_location: string
) => {
  try {
    const response = await axios.put(
      `${baseApiUrl}/update_list/${client_code}/`,
      {
        client_selected_program: selected_program,
        client_selected_locations: selected_location
      }
    );
    return response.data;
  } catch (error) {
    console.error("api function saveLocationAndProgram error");
    throwError(error);
  }
};

export const updateProgramCompletion = async (
  client_code: string,
  Program_Completion: number | null,
  Returned_to_Care: number | null,
  program_significantly_modified: number
) => {
  try {
    const response = await axios.put(
      `${baseApiUrl}/program_complete/${client_code}/`,
      {
        Program_Completion,
        Returned_to_Care,
        program_significantly_modified
      }
    );
    return response.data.data;
  } catch (error) {
    console.error("api function updateProgramCompletion error");
    throwError(error);
  }
};

export const searchClient = async (
  client_code: string,
  client_name: string = ""
) => {
  try {
    const response = await axios.get(
      `${baseApiUrl}/search/?name=${client_name}&client_code=${client_code}`
    );
    return response.data;
  } catch (error) {
    console.error("api function searchClient error");
    throwError(error);
  }
};

// EXISTING CLIENT PAGE APIs
// list of programs for existing client
// http://13.232.1.126:8000/first_match/program/100/
// Program completion likelihood

export const fetchProgramsForClient = async (client_code: string) => {
  try {
    const response = await axios.get(`${baseApiUrl}/program/${client_code}/`);
    const data = (response.data as unknown) as any;
    return data;
  } catch (error) {
    console.error("api function fetch fetchProgramForClient error");
    throwError(error);
  }
};

function throwError(error: any) {
  if (error.response) {
    // The request was made and the server responded with a status code
    // that falls out of the range of 2xx
    console.log(error.response.data);
    console.log(error.response.status);
    console.log(error.response.headers);
    const errorResponse = {
      data: error.response.data || undefined,
      status: error.response.status || undefined
    };
    throw errorResponse;
  } else if (error.request) {
    // The request was made but no response was received
    // `error.request` is an instance of XMLHttpRequest in the browser and an instance of
    // http.ClientRequest in node.js
    console.log(error.request);
    const errorResponse = {
      data: { Error: "unknown error occurred while contacting the server" },
      status: undefined
    };
    throw errorResponse;
  } else {
    // Something happened in setting up the request that triggered an Error
    console.log("Error", error.message);
  }
}
