import React, {ButtonHTMLAttributes, DetailedHTMLProps} from "react"
import "./SettingsButton.scss"

export default function SettingsButton(
  props: Omit<DetailedHTMLProps<ButtonHTMLAttributes<HTMLButtonElement>, HTMLButtonElement>, "children">,
): React.JSX.Element {
  const webApp = window.Telegram.WebApp
  const {onClick, className = "", ...rest} = props

  const handleClick = event => {
    webApp.HapticFeedback.impactOccurred("light")
    onClick?.(event)
  }

  return (
    <button
      className={`SettingsButton ${className}`}
      onClick={handleClick}
      {...rest}
    >
      <svg
        className="SettingsButton__icon"
        width="18"
        height="12"
        viewBox="0 0 18 12"
        fill="none"
        xmlns="http://www.w3.org/2000/svg"
      >
        <path fillRule="evenodd" clipRule="evenodd" d="M0 3C0 3.55225 0.447754 4 1 4H4.17081C4.58265 5.16523 5.69382 6 7 6C8.30618 6 9.41735 5.16523 9.82919 4H17C17.5522 4 18 3.55225 18 3C18 2.44775 17.5522 2 17 2H9.82919C9.41735 0.834773 8.30618 0 7 0C5.69382 0 4.58265 0.834773 4.17081 2H1C0.447754 2 0 2.44775 0 3ZM7 4.12671C6.37769 4.12671 5.87329 3.62219 5.87329 3C5.87329 2.37781 6.37769 1.87329 7 1.87329C7.62231 1.87329 8.12671 2.37781 8.12671 3C8.12671 3.62219 7.62231 4.12671 7 4.12671Z"
        />
        <path fillRule="evenodd" clipRule="evenodd" d="M18 9C18 9.55225 17.5522 10 17 10H13.8292C13.4173 11.1652 12.3062 12 11 12C9.69382 12 8.58265 11.1652 8.17081 10H1C0.447754 10 0 9.55225 0 9C0 8.44775 0.447754 8 1 8H8.17081C8.58265 6.83477 9.69382 6 11 6C12.3062 6 13.4173 6.83477 13.8292 8H17C17.5522 8 18 8.44775 18 9ZM11 10.1267C11.6223 10.1267 12.1267 9.62219 12.1267 9C12.1267 8.37781 11.6223 7.87329 11 7.87329C10.3777 7.87329 9.87329 8.37781 9.87329 9C9.87329 9.62219 10.3777 10.1267 11 10.1267Z"
        />
      </svg>
    </button>
  )
}
