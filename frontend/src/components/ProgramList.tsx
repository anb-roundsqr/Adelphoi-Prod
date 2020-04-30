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

interface ProgramListProps {
  programList: Types.Program[];
  isLoading: boolean;
  hasError: boolean;
  error: string;
  createProgram: (program: Types.Program) => Promise<void>;
  updateProgram: (program: Types.Program) => Promise<void>;
}

interface FormValues {
  program_name: string;
  editing_program_name: string;
}

const initialValues: FormValues = {
  program_name: "",
  editing_program_name: ""
};

const ProgramList: React.FC<ProgramListProps> = props => {
  const { enqueueSnackbar } = useSnackbar();

  const [editingProgram, setEditingProgram] = useState<Types.Program | null>(
    null
  );

  const renderCell = (
    program: Types.Program,
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
    if (editingProgram && editingProgram.program === program.program) {
      return (
        <React.Fragment>
          <TableCell>
            <input
              type="text"
              name="editing_program_name"
              css={inputField}
              style={{ width: "100%" }}
              placeholder="Add program name"
              value={values.editing_program_name || ""}
              onChange={handleChange}
            />
            <ErrorMessage component="span" name="editing_program_name" />
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
              onClick={() => setEditingProgram(null)}
            >
              cancel
            </Button>
          </TableCell>
        </React.Fragment>
      );
    }
    return (
      <React.Fragment>
        <TableCell>{program.program_name}</TableCell>
        <TableCell>
          <Link
            onClick={() => {
              setEditingProgram(program);
              setFieldValue(
                "editing_program_name",
                program.program_name,
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
  const { programList } = props;
  return (
    <div css={wrap}>
      <div css={mainContent}>
        <Backdrop css={backdrop} open={props.isLoading}>
          <CircularProgress color="inherit" />
        </Backdrop>
        <div>
          <h1 css={subHeading}>Programs</h1>
          <Formik
            initialValues={initialValues}
            enableReinitialize
            validate={values => {
              const errors: FormikErrors<FormValues> = {};
              if (!editingProgram && !values.program_name) {
                errors.program_name = "Required";
              }
              if (editingProgram && !values.editing_program_name) {
                errors.program_name = "Required";
              }
              return errors;
            }}
            onSubmit={async (values, helpers) => {
              try {
                if (editingProgram) {
                  const program: Types.Program = {
                    program: editingProgram.program,
                    program_name: values.editing_program_name
                  };
                  await props.updateProgram(program);
                  enqueueSnackbar("program updated successfully");
                  helpers.resetForm();
                  setEditingProgram(null);
                } else {
                  const program: Types.Program = {
                    program: 0,
                    program_name: values.program_name
                  };
                  await props.createProgram(program);
                  enqueueSnackbar("program created successfully");
                  helpers.resetForm();
                }
              } catch (error) {
                enqueueSnackbar("Could create/update program");
              }
            }}
          >
            {({ values, handleSubmit, handleChange, setFieldValue }) => (
              <form name="ProgramForm" onSubmit={handleSubmit}>
                <div css={fieldRow}>
                  <div css={twoCol}>
                    <input
                      type="text"
                      name="program_name"
                      css={inputField}
                      placeholder="Add new program.."
                      value={values.program_name || ""}
                      onChange={e => {
                        setEditingProgram(null);
                        handleChange(e);
                      }}
                    />
                    <ErrorMessage component="span" name="program_name" />
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

                <Table aria-label="programs table" css={dataTable}>
                  <TableHead>
                    <TableRow css={tableHeader}>
                      <TableCell style={{ width: "600px" }}>
                        Program Name
                      </TableCell>
                      <TableCell>Edit</TableCell>
                    </TableRow>
                  </TableHead>
                  <TableBody>
                    {programList.length > 0 ? (
                      programList.map(p => (
                        <TableRow key={p.program} css={tableRow}>
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

export default ProgramList;
