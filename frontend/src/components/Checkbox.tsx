import React, {MouseEvent} from "react"
import "./Checkbox.scss"


interface Props {
  className?: string,
  style?: CSSStyleDeclaration,
  checked?: boolean,
  disabled?: boolean,
  onClick?: (event: MouseEvent<HTMLDivElement>) => void
}

export default function Checkbox(props: Props): React.JSX.Element {
  const {
    onClick, checked,
    style = {}, className = "",
    disabled = false
  } = props

  const handleClick = (event) => {
    onClick?.(event)
  }

  return (
    <div
      onClick={handleClick}
      style={style}
      className={`
        Checkbox
        ${checked ? "Checkbox__checked" : ""}
        ${disabled ? "Checkbox__disabled" : ""}
        ${className}
      `}
    >
      <svg
        className="Checkbox__checkmark"
        width="16" height="16" viewBox="0 0 16 16"
        fill="none" xmlns="http://www.w3.org/2000/svg"
      >
        <path d="M13.3333 4L6 11.3333L2.66667 8" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
      </svg>
    </div>
  )
}
