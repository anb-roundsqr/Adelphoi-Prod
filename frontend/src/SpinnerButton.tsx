import React from 'react'
import Button from '@material-ui/core/Button'
import CircularProgress from '@material-ui/core/CircularProgress'

const SpinnerAdornment = () => (
  <CircularProgress
    size={18}
    style={{color: 'white', marginLeft: 5}}
  />
);
const SpinnerButton = (props: any) => {
  const {
    children,
    loading,
    ...rest
  } = props
  return (
    <Button {...rest}>
      {children}
      {loading && <SpinnerAdornment {...rest} />}
    </Button>
  )
}

export default SpinnerButton;