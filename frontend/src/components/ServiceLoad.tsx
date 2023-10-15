import React from "react"
import "./ServiceLoad.scss"

interface Props {
  load?: number
}

const loadWaitTimes = {
  0: "<10 мин",
  1: "10-20 мин",
  2: "20-30 мин",
  3: "30-40 мин",
  4: "40-50 мин",
  5: "1+ час"
}

const loadColors = {
  0: "#8EC26A",
  1: "#c5d261",
  2: "#FBE158",
  3: "#FF9D56",
  4: "#ff906c",
  5: "#ff8282"
}

export default function ServiceLoad(props: Props): React.JSX.Element {
  const {load} = props

  const loadTime = load !== undefined ?
    loadWaitTimes[load] || "--" : "--"
  const loadColor = load !== undefined ?
    loadColors[load] || loadColors[0] : loadColors[0]
  const loadWidth = load !== undefined && loadColors[load] ?
    (10 + 18 * load).toFixed(0) : 10

  return (
    <div className="ServiceLoad">
      <div className="ServiceLoad__status">
        <span>Время ожидания</span>
        <span>{loadTime}</span>
      </div>
      <div className="ServiceLoad__bar">
        <div style={{
          backgroundColor: loadColor,
          width: `${loadWidth}%`
        }}/>
      </div>
    </div>
  )
}
