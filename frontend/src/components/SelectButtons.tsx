import React from "react"
import "./SelectButtons.scss"

interface Props {
  buttons: {id: string, text: string}[],
  selected: string,
  style?: CSSStyleDeclaration,
  className?: string,
  onChange?: (id: string) => void
}

export default function SelectButtons(props: Props): React.JSX.Element {
  const {buttons, selected, style = {}, className = "", onChange} = props

  return (
    <div className={`SelectButtons ${className}`} style={style}>
      {
        buttons.map(v => (
          <button
            key={v.id}
            className={`
              SelectButtons__button
              ${v.id === selected ? "SelectButtons__active" : "SelectButtons__inactive"}
            `}
            onClick={() => onChange?.(v.id)}
          >
            {v.text}
          </button>
        ))
      }
    </div>
  )
}
