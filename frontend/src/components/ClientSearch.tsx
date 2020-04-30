/** @jsx jsx */
import { jsx } from "@emotion/core";
import { useHistory } from "react-router-dom";
import { Formik, ErrorMessage, FormikErrors } from "formik";
import Button from "@material-ui/core/Button";
import SearchIcon from "@material-ui/icons/Search";
import Table from "@material-ui/core/Table";
import TableBody from "@material-ui/core/TableBody";
import TableCell from "@material-ui/core/TableCell";
import TableHead from "@material-ui/core/TableHead";
import TableRow from "@material-ui/core/TableRow";
import {
  wrap,
  subHeading,
  fieldRow,
  mainContent,
  twoCol,
  inputField,
  tableHeader,
  tableRow,
  dataTable
} from "./styles";
import * as Types from "../api/definitions";

interface ClientSearchProps {
  clientList: Types.Client[];
  onFormSubmit: (client_code: string, client_name: string) => void;
  isLoading: boolean;
  hasError: boolean;
  error: string;
}

interface FormValues {
  client_name: string;
  client_code: string;
}

const initialValues: FormValues = {
  client_name: "",
  client_code: ""
};

const ClientSearch: React.FC<ClientSearchProps> = props => {
  const history = useHistory();
  /** */
  const { clientList } = props;
  return (
    <div css={wrap}>
      <div css={mainContent}>
        <Formik
          initialValues={initialValues}
          enableReinitialize
          validate={values => {
            const errors: FormikErrors<FormValues> = {};
            if (!values.client_code && !values.client_name) {
              errors.client_code = "Enter either of the fields";
            }
            return errors;
          }}
          onSubmit={async (values, helpers) => {
            await props.onFormSubmit(values.client_code, values.client_name);
            // helpers.resetForm();
          }}
        >
          {({ values, handleSubmit, handleChange }) => (
            <form name="clientSearchForm" onSubmit={handleSubmit}>
              <div css={fieldRow}>
                <div css={twoCol}>
                  <input
                    type="text"
                    name="client_code"
                    css={inputField}
                    placeholder="Client Code"
                    value={values.client_code || ""}
                    onChange={handleChange}
                  />
                  <ErrorMessage component="span" name="client_code" />
                </div>
                <div css={twoCol}>
                  <input
                    type="text"
                    name="client_name"
                    css={inputField}
                    placeholder="client Name"
                    value={values.client_name || ""}
                    onChange={handleChange}
                  />
                  <ErrorMessage component="span" name="client_name" />
                </div>
                <Button
                  type="submit"
                  size="small"
                  variant="contained"
                  color="primary"
                  style={{ maxHeight: 44 }}
                >
                  <SearchIcon />
                </Button>
              </div>
            </form>
          )}
        </Formik>
        <div>
          <h1 css={subHeading}>Client List</h1>
          <Table aria-label="clients table" css={dataTable}>
            <TableHead>
              <TableRow css={tableHeader}>
                <TableCell>Client Name</TableCell>
                <TableCell>Client Code</TableCell>
                <TableCell>Age</TableCell>
                <TableCell>Gender</TableCell>
              </TableRow>
            </TableHead>
            <TableBody>
              {clientList.length > 0 ? (
                clientList.map(cl => (
                  <TableRow
                    hover
                    key={cl.client_code || undefined}
                    onClick={() =>
                      history.push(
                        `existing-client/client-details/${cl.client_code}`
                      )
                    }
                    css={tableRow}
                  >
                    <TableCell>{cl.name}</TableCell>
                    <TableCell>{cl.client_code}</TableCell>
                    <TableCell>{cl.age}</TableCell>
                    <TableCell>
                      {cl.gender && cl.gender.toString() === "1"
                        ? "Female"
                        : "Male"}
                    </TableCell>
                  </TableRow>
                ))
              ) : (
                <TableRow key={9999}>
                  <TableCell colSpan={4} style={{ textAlign: "center" }}>
                    No results found
                  </TableCell>
                </TableRow>
              )}
            </TableBody>
          </Table>
        </div>
      </div>
      {/* MAIN CONTENT */}
    </div>
  );
};

export default ClientSearch;
