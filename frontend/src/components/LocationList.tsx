/** @jsx jsx */
import { jsx } from "@emotion/core";
import React, { useState } from "react";
// import { useHistory } from "react-router-dom";
import { Formik, ErrorMessage, FormikErrors } from "formik";
import { useSnackbar } from "notistack";
import Button from "@material-ui/core/Button";
import Link from "@material-ui/core/Link";
import Table from "@material-ui/core/Table";
import TableBody from "@material-ui/core/TableBody";
import TableCell from "@material-ui/core/TableCell";
import TableHead from "@material-ui/core/TableHead";
import TableRow from "@material-ui/core/TableRow";
import Backdrop from "@material-ui/core/Backdrop";
import CircularProgress from "@material-ui/core/CircularProgress";
import {
  wrap,
  subHeading,
  fieldRow,
  mainContent,
  twoCol,
  inputField,
  tableHeader,
  tableRow,
  dataTable,
  backdrop
} from "./styles";
import * as Types from "../api/definitions";

interface LocationListProps {
  locationList: Types.Location[];
  isLoading: boolean;
  hasError: boolean;
  error: string;
  createLocation: (location: Types.Location) => Promise<void>;
  updateLocation: (location: Types.Location) => Promise<void>;
}

interface FormValues {
  location_names: string;
  editing_location_names: string;
}

const initialValues: FormValues = {
  location_names: "",
  editing_location_names: ""
};

const LocationList: React.FC<LocationListProps> = props => {
  const { enqueueSnackbar } = useSnackbar();

  const [editingLocation, setEditingLocation] = useState<Types.Location | null>(
    null
  );

  const renderCell = (
    location: Types.Location,
    values: FormValues,
    handleChange:
      | ((event: React.ChangeEvent<HTMLInputElement>) => void)
      | undefined,
    setFieldValue: (
      field: string,
      value: any,
      shouldValidate?: boolean | undefined
    ) => void
  ) => {
    if (editingLocation && editingLocation.location === location.location) {
      return (
        <React.Fragment>
          <TableCell>
            <input
              type="text"
              name="editing_location_names"
              css={inputField}
              style={{ width: "100%" }}
              placeholder="Add location name"
              value={values.editing_location_names || ""}
              onChange={handleChange}
            />
            <ErrorMessage component="span" name="editing_location_names" />
          </TableCell>
          <TableCell>
            <Button
              type="submit"
              size="small"
              variant="contained"
              color="primary"
            >
              Update
            </Button>
            <Button
              type="button"
              size="small"
              variant="contained"
              color="default"
              onClick={() => setEditingLocation(null)}
            >
              cancel
            </Button>
          </TableCell>
        </React.Fragment>
      );
    }
    return (
      <React.Fragment>
        <TableCell>{location.location_names}</TableCell>
        <TableCell>
          <Link
            onClick={() => {
              setEditingLocation(location);
              setFieldValue(
                "editing_location_names",
                location.location_names,
                false
              );
            }}
          >
            Edit
          </Link>
        </TableCell>
      </React.Fragment>
    );
  };

  // const history = useHistory();
  /** */
  const { locationList } = props;
  return (
    <div css={wrap}>
      <div css={mainContent}>
        <Backdrop css={backdrop} open={props.isLoading}>
          <CircularProgress color="inherit" />
        </Backdrop>
        <div>
          <h1 css={subHeading}>Locations</h1>
          <Formik
            initialValues={initialValues}
            enableReinitialize
            validate={values => {
              const errors: FormikErrors<FormValues> = {};
              if (!editingLocation && !values.location_names) {
                errors.location_names = "Required";
              }
              if (editingLocation && !values.editing_location_names) {
                errors.location_names = "Required";
              }
              return errors;
            }}
            onSubmit={async (values, helpers) => {
              try {
                if (editingLocation) {
                  const location: Types.Location = {
                    location: editingLocation.location,
                    location_names: values.editing_location_names
                  };
                  await props.updateLocation(location);
                  enqueueSnackbar("location updated successfully");
                  helpers.resetForm();
                  setEditingLocation(null);
                } else {
                  const location: Types.Location = {
                    location: 0,
                    location_names: values.location_names
                  };
                  await props.createLocation(location);
                  enqueueSnackbar("location created successfully");
                  helpers.resetForm();
                }
              } catch (error) {
                enqueueSnackbar("Could create/update location");
              }
            }}
          >
            {({ values, handleSubmit, handleChange, setFieldValue }) => (
              <form name="LocationForm" onSubmit={handleSubmit}>
                <div css={fieldRow}>
                  <div css={twoCol}>
                    <input
                      type="text"
                      name="location_names"
                      css={inputField}
                      placeholder="Add new location.."
                      value={values.location_names || ""}
                      onChange={e => {
                        setEditingLocation(null);
                        handleChange(e);
                      }}
                    />
                    <ErrorMessage component="span" name="location_names" />
                  </div>

                  <Button
                    type="submit"
                    size="large"
                    variant="contained"
                    color="primary"
                  >
                    Submit
                  </Button>
                </div>

                <Table aria-label="locations table" css={dataTable}>
                  <TableHead>
                    <TableRow css={tableHeader}>
                      <TableCell style={{ width: "600px" }}>
                        Location Name
                      </TableCell>
                      <TableCell>Edit</TableCell>
                    </TableRow>
                  </TableHead>
                  <TableBody>
                    {locationList.length > 0 ? (
                      locationList.map(p => (
                        <TableRow key={p.location} css={tableRow}>
                          {renderCell(p, values, handleChange, setFieldValue)}
                        </TableRow>
                      ))
                    ) : (
                      <TableRow key={9999}>
                        <TableCell colSpan={2} style={{ textAlign: "center" }}>
                          &nbsp;
                        </TableCell>
                      </TableRow>
                    )}
                  </TableBody>
                </Table>
              </form>
            )}
          </Formik>
        </div>
      </div>
      {/* MAIN CONTENT */}
    </div>
  );
};

export default LocationList;
