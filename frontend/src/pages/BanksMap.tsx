import React, {useEffect, useState} from "react"
import {isLightTheme, usePosition} from "../utils"
import {LocationMarker} from "../components"
import Map, {Layer, Marker, Source} from "react-map-gl"
import {useMapContext, useStore} from "../store"
import {markers} from "../assets"
import {useNavigate} from "react-router-dom"

const MAPBOX_TOKEN = "pk.eyJ1IjoiZWdlc2hhIiwiYSI6ImNsbmhpMmp4NDEycjYya3RjZXdkdXZvaGUifQ.og7rsjgzZnHwSOqKxmwWOA"

export default function BanksMap(): React.JSX.Element {
  const webApp = window.Telegram.WebApp
  const mapRef = useMapContext()
  const [gotLocation, setGotLocation] = useState<boolean>(false)
  const {location, compassHeading, isLoading, error} = usePosition()
  const [state] = useStore()
  const navigate = useNavigate()

  useEffect(() => {
    if (gotLocation) return
    if (isLoading || error || !location?.latitude || !location.longitude) return
    if (!mapRef.current) return
    setGotLocation(true)
    mapRef.current.flyTo(
      {center: [location.longitude, location.latitude], zoom: 15, duration: 750}
    )
  }, [location, gotLocation, mapRef, isLoading, error])

  return (
    <Map
      ref={mapRef}
      mapboxAccessToken={MAPBOX_TOKEN}
      cursor="auto"
      initialViewState={{
        longitude: 37.617734,
        latitude: 55.752004,
        zoom: 8
      }}
      style={{width: "100vw", height: "100vh"}}
      mapStyle={
        isLightTheme() ?
          "mapbox://styles/mapbox/light-v11"
          : "mapbox://styles/mapbox/dark-v11"
      }
    >
      {
        location !== null && (
          <LocationMarker
            coords={[location.longitude, location.latitude]}
            accuracy={location.accuracy}
            heading={compassHeading !== null ? compassHeading : location.heading}
          />
        )
      }
      {
        state.atms.map(v => (
          <Marker
            key={`atm-${v.id}`}
            longitude={v.coordinate.lng}
            latitude={v.coordinate.lat}
            anchor="bottom"
            onClick={() => navigate(`/atm/${v.id}`)}
            style={{cursor: "pointer"}}
          >
            <img src={markers.atm} alt=""/>
          </Marker>
        ))
      }
      {
        state.offices.map(v => (
          <Marker
            key={`office-${v.id}`}
            longitude={v.coordinate.lng}
            latitude={v.coordinate.lat}
            anchor="bottom"
            onClick={() => navigate(`/office/${v.id}`)}
            style={{cursor: "pointer"}}
          >
            <img src={markers.default} alt=""/>
          </Marker>
        ))
      }
      {
        state.route !== null &&
        <Source type="geojson" data={state.route}>
          <Layer
            type="line"
            paint={{
              "line-color": webApp.themeParams.button_color,
              "line-width": 4,
            }}
          />
        </Source>
      }
    </Map>
  )
}
