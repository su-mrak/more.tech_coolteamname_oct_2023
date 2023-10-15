import React, {ButtonHTMLAttributes, DetailedHTMLProps} from "react"
import "./Button.scss"


export default function Button(
  props: DetailedHTMLProps<ButtonHTMLAttributes<HTMLButtonElement>, HTMLButtonElement>
): React.JSX.Element {
  const {onClick, children, className = "", ...rest} = props

  const handleClick = event => {
    const haptic = window.Telegram.WebApp.HapticFeedback

    haptic.impactOccurred("light")
    onClick?.(event)
  }

  return (
    <button
      className={`Button ${className}`}
      onClick={handleClick}
      {...rest}
    >
      {children}
    </button>
  )
}
