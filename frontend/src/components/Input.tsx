import React, {DetailedHTMLProps, InputHTMLAttributes} from "react"
import "./Input.scss"

export default function Input(
  props: DetailedHTMLProps<InputHTMLAttributes<HTMLInputElement>, HTMLInputElement>
): React.JSX.Element {
  const {className = "", ...rest} = props

  return (
    <input
      className={`Input ${className}`}
      {...rest}
    />
  )
}
