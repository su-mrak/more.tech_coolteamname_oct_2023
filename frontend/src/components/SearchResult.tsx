import React from "react"

import "./SearchResult.scss"
import {officeIcons} from "../assets"
import {formatDistance} from "../utils"
import {useNavigate} from "react-router-dom"

interface Result {
  address: string,
  distance: number | null,

  id: string,
  type: "office" | "atm",
  load?: number,
}

interface Props {
  results: Result[],
}

interface ResultsByDistance {
  1: Result[],
  3: Result[],
  5: Result[],
  more: Result[],
}

const loadWaitTimes = {
  0: "<10 мин",
  1: "20 мин",
  2: "30 мин",
  3: "40 мин",
  4: "50 мин",
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

export default function SearchResult(props: Props): React.JSX.Element {
  const {results} = props
  const navigate = useNavigate()

  const resultsByDistance: ResultsByDistance = {
    1: [],
    3: [],
    5: [],
    more: [],
  }

  for (const v of results) {
    if (v.distance === null) {
      resultsByDistance.more.push(v)
    } else if (v.distance <= 1000) {
      resultsByDistance[1].push(v)
    } else if (v.distance <= 3000) {
      resultsByDistance[3].push(v)
    } else if (v.distance <= 5000) {
      resultsByDistance[5].push(v)
    } else {
      resultsByDistance.more.push(v)
    }
  }

  return (
    <div className="SearchResult">
      {
        Object.keys(resultsByDistance).sort().map(
          v => (
            resultsByDistance[v].length !== 0 &&
              <>
                <span className="SearchResult__header" key={v}>
                  {v !== "more" ? `В радиусе ${v} км` : "Далеко"}
                </span>
                {
                  resultsByDistance[v].map(
                    office => (
                      <div
                        className="SearchResult__container"
                        onClick={() => {
                          navigate(`/${office.type}/${office.id}`)
                        }}
                      >
                        <img src={office.type === "office" ? officeIcons.default: officeIcons.atm} alt=""/>
                        <span className="SearchResult__address">
                          {office.address}
                        </span>
                        <span className="SearchResult__distance">
                          <span>{formatDistance(office.distance)}</span>
                          <span style={{
                            color: office.load !== undefined ? loadColors[office.load] || loadColors[0] : loadColors[0]
                          }}>
                            {office.load !== undefined ? loadWaitTimes[office.load] || loadWaitTimes[0] : loadWaitTimes[0]}
                          </span>
                        </span>
                      </div>
                    )
                  )
                }
              </>
          )
        )
      }
    </div>
  )
}
