import React from "react";
import Snackbar from "@material-ui/core/Snackbar";
import IconButton from "@material-ui/core/IconButton";
import CloseIcon from "@material-ui/icons/Close";
import Paper from "@material-ui/core/Paper";
import { connect } from "react-redux";
import * as client from "../redux-modules/client";

interface SnackNotificationProps<T> {
  errors: T;
  clearErrors: () => void;
}

function SnackNotification<T>(
  props: SnackNotificationProps<T> & { children?: React.ReactNode }
) {
  const { errors } = props;
  const [open, setOpen] = React.useState(Object.keys(errors).length > 0);

  const handleClose = (
    event: React.SyntheticEvent | React.MouseEvent,
    reason?: string
  ) => {
    if (reason === "clickaway") {
      return;
    }
    // clearErrors();
    setOpen(false);
  };

  React.useEffect(() => {
    setOpen(Object.keys(errors).length > 0);
  }, [errors]);

  return (
    <Snackbar
      anchorOrigin={{ vertical: "top", horizontal: "right" }}
      open={open}
      style={{ right: 10 }}
      autoHideDuration={3000}
      onClose={handleClose}
      action={
        <React.Fragment>
          <IconButton
            size="small"
            aria-label="close"
            color="default"
            onClick={handleClose}
          >
            <CloseIcon fontSize="small" />
          </IconButton>
        </React.Fragment>
      }
    >
      <Paper
        elevation={3}
        style={{
          minWidth: "85%",
          backgroundColor: "#C62828",
          color: "white",
          maxHeight: "200px",
          overflow: "auto",
          padding: 10
        }}
      >
        <p>Following error(s) occurred while trying to save the form</p>
        <ul>
          {(Object.keys(errors) as Array<keyof typeof errors>).map((key, i) => {
            return <li key={i}>{`${key}: ${errors[key]}`}</li>;
          })}
        </ul>
      </Paper>
    </Snackbar>
  );
}

const mapDispatchToProps = {
  clearErrors: client.actions.clearErrors
};

export default connect(null, mapDispatchToProps)(SnackNotification);
