import React from "react";
import { connect, getIn, FormikContextType } from "formik";

interface ErrorMessageProps {
  name: string;
  component?: string;
}

const ErrorMessage: React.FC<ErrorMessageProps & {
  formik: FormikContextType<any>;
}> = props => {
  const error = getIn(props.formik.errors, props.name);
  const apiError = getIn(props.formik.initialErrors, props.name);
  const touch = getIn(props.formik.touched, props.name);
  if (apiError && error) {
    return <span>{error}</span>;
  }
  return touch && error ? <span>{error}</span> : null;
};

export default connect<
  ErrorMessageProps,
  ErrorMessageProps & { formik: FormikContextType<any> }
>(ErrorMessage);
