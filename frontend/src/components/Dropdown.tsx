import React from "react";
import Select, { OptionsType, ValueType } from "react-select";
import { useFormikContext, useField, FormikHandlers } from "formik";

interface DropdownProps {
  name: string;
  options: OptionsType<any>;
  onChange?: FormikHandlers["handleChange"];
  onBlur?: FormikHandlers["handleBlur"];
  defaultValue?: any;
  value?: any;
  disabled?: boolean;
  // error: string;
  // touched: boolean;
}
const Dropdown = ({ options, ...props }: DropdownProps) => {
  const { setFieldValue, setFieldTouched } = useFormikContext();
  const [field, meta] = useField(props);

  /**
   * Will manually set the value belong to the name props in the Formik form using setField
   */
  function handleOptionChange(selection: ValueType<any>) {
    setFieldValue(props.name, selection);
    if (props.onChange) {
      props.onChange(selection);
    }
  }

  const customStyles = {
    control: (provided: any, state: any) => ({
      ...provided,
      borderRadius: 0,
      borderColor: "#f5f5f5",
      borderBottom: "1px solid #8284e5",
      height: 44,
      backgroundColor: "#f5f5f5"
    }),
    option: (styles: any, { data, isDisabled, isFocused, isSelected }: any) => {
      return {
        ...styles,
        ...dot(data.predicted, isFocused, isSelected)
      };
    }
  };

  /**
   * Manually updated the touched property for the field in Formik
   */
  function updateBlur() {
    setFieldTouched(props.name, true);
  }

  const dot = (predicted: boolean, isFocused: boolean, isSelected: boolean) => {
    return predicted
      ? {
          display: "flex",
          alignItems: "center",
          fontWeight: "bold",
          ":after": {
            backgroundColor: isSelected ? "white" : "green",
            borderRadius: 10,
            content: '" "',
            display: "block",
            marginLeft: 8,
            height: 10,
            width: 10
          }
        }
      : {};
  };

  return (
    <React.Fragment>
      <Select
        styles={customStyles}
        isDisabled={props.disabled || false}
        options={options}
        {...field}
        {...props}
        onBlur={updateBlur}
        onChange={handleOptionChange}
      />
      {meta.touched && meta.error ? (
        <span className="custom-input-error">{meta.error}</span>
      ) : null}
    </React.Fragment>
  );
};

export default Dropdown;
