import {createContext, createRef, useContext, useState} from "react"
import {createContainer} from "react-tracked"
import {Office, Atm, AtmFeature, OfficeFeature} from "./utils/backend"
import {MapRef} from "react-map-gl"
import type {FeatureCollection} from "geojson"


interface State {
  offices: Office[],
  atms: Atm[],
  userCoords: [number, number] | null
  route: FeatureCollection | null,
  atmFilters: AtmFeature[],
  officeFilters: OfficeFeature[],
}

const mapRef = createRef<MapRef>()
const MapContext = createContext(mapRef)

const initialState: State = {
  offices: [],
  atms: [],
  userCoords: null,
  route: null,
  atmFilters: [],
  officeFilters: [],
}

const useMyState = () => useState(initialState)

export const MapContextProvider = ({children}) => {
  return (
    <MapContext.Provider value={mapRef}>
      {children}
    </MapContext.Provider>
  )
}

export const useMapContext = () => useContext(MapContext)

export const {Provider: StoreProvider, useTracked: useStore} = createContainer(useMyState)
