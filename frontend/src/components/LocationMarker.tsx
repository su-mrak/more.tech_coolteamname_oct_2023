import React from "react"
import {Layer, Marker, Source} from "react-map-gl"
import circle from "@turf/circle"

interface Props {
  coords: [number, number],
  accuracy?: number,
  heading: number | null,
}

export default function LocationMarker(props: Props): React.JSX.Element | null {
  const themeParams = window.Telegram.WebApp.themeParams
  const {coords, heading, accuracy = 0} = props

  const userLocation = circle(coords, accuracy, {units: "meters"})

  return (
    <>
      <Marker
        longitude={coords[0]}
        latitude={coords[1]}
        anchor="center"
        pitchAlignment="map"
        style={{width: 81, height: 81, cursor: "default"}}
      >
        <svg
          width="81" height="81"
          viewBox="0 0 66 66"
          fill="none"
          xmlns="http://www.w3.org/2000/svg"
        >
          <circle cx="33" cy="33" r="9" fill={themeParams.button_color} stroke={themeParams.button_text_color}/>
          {heading !== null &&
            <path
              d="M26.4149 22.5316L33 11.0078L39.585 22.5316C37.6091 21.486 35.3709 20.8957 33 20.8957C30.629 20.8957 28.3908 21.486 26.4149 22.5316Z"
              fill={themeParams.button_color} stroke={themeParams.button_text_color}
              transform={`rotate(${heading} 33 33)`}
            />
          }
        </svg>
      </Marker>
      <Source
        id="user-location"
        type="geojson"
        data={userLocation}
      >
        <Layer
          type="fill"
          paint={{
            "fill-color": "#9A9EA5",
            "fill-opacity": 0.4
          }}
        />
      </Source>
    </>
  )
}
