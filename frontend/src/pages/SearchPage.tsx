import React, {useEffect, useMemo, useState} from "react"
import {Input, SearchResult, SelectButtons, SettingsButton} from "../components"
import {useMapContext, useStore} from "../store"
import {distance} from "@turf/turf"

import "./SearchPage.scss"
import {getTopTellerFiltered} from "../utils/backend"
import {useNavigate} from "react-router-dom"

export default function SearchPage(): React.JSX.Element {
  const [state, dispatch] = useStore()
  const [searchType, setSearchType] = useState<"office" | "atm">("office")
  const [searchText, setSearchText] = useState<string>("")
  const mapRef = useMapContext()
  const navigate = useNavigate()

  useEffect(() => {
    let userCoords = state.userCoords
    if (userCoords === null && mapRef.current) {
      const {lat, lng} = mapRef.current.getCenter()
      userCoords = [lng, lat]
    } else if (userCoords === null) {
      userCoords = [37.702547, 55.801432]
    }

    getTopTellerFiltered(
      userCoords,
      state.atmFilters,
      state.officeFilters,
    ).then(result => dispatch((prev) => (
      {...prev, atms: result.atms, offices: result.offices}
    )))
  }, [state.atmFilters, state.officeFilters, state.userCoords, mapRef, dispatch])

  const handleOpenFilters = () => {
    if (searchType === "atm") {
      navigate("/filter/atm")
    } else {
      navigate("/filter/office")
    }
  }

  const userCoords = state.userCoords

  const offices = useMemo(() => {
    return state.offices
      .filter(v => v.address.toLowerCase().indexOf(searchText.toLowerCase()) !== -1)
      .map(
        v => ({
          id: v.id,
          type: "office" as "office" | "atm",
          load: v.load,
          address: v.address,
          distance: userCoords !== null ?
            distance(userCoords, [v.coordinate.lng, v.coordinate.lat], {units: "meters"})
            : null
        })
      )
      .slice(0, 75)
  }, [searchText, userCoords, state.offices])

  const atms = useMemo(() => {
    return state.atms
      .filter(v => v.address.toLowerCase().indexOf(searchText.toLowerCase()) !== -1)
      .map(
        v => ({
          id: v.id,
          type: "atm" as "office" | "atm",
          load: v.load,
          address: v.address,
          distance: userCoords !== null ?
            distance(userCoords, [v.coordinate.lng, v.coordinate.lat], {units: "meters"})
            : null
        })
      )
      .slice(0, 75)
  }, [searchText, userCoords, state.atms])

  return (
    <div className="SearchPage">
      <div className="SearchPage__controls">
        <Input
          style={{width: "100%"}}
          placeholder="Поиск..."
          onChange={e => setSearchText(e.target.value)}
        />
        <SettingsButton onClick={handleOpenFilters}/>
      </div>
      <SelectButtons
        buttons={[
          {id: "office", text: "Отделения"},
          {id: "atm", text: "Банкоматы"}
        ]}
        selected={searchType}
        onChange={(id) => setSearchType(id as "office" | "atm")}
      />
      <SearchResult results={searchType === "atm" ? atms : offices}/>
    </div>
  )
}
