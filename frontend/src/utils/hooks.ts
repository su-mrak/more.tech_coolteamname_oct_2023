import {useEffect, useState} from "react"
import {useStore} from "../store"


interface Location {
  accuracy: number,
  altitude: number | null,
  altitudeAccuracy: number | null,
  heading: number | null,
  latitude: number,
  longitude: number,
  speed: number | null,
  timestamp: EpochTimeStamp,
}

interface Position {
  location: Location | null,
  compassHeading: number | null,
  isLoading: boolean,
  error: null | GeolocationPositionError
}

export function usePosition(): Position {
  const [compass, setCompass] = useState<number | null>(null)
  const [isLoading, setIsLoading] = useState<boolean>(true)
  const [location, setLocation] = useState<Location | null>(null)
  const [error, setError] = useState<GeolocationPositionError | null>(null)

  const [, dispatch] = useStore()

  useEffect(() => {
    const handleLocation = ({coords, timestamp}: GeolocationPosition) => {
      setIsLoading(false)
      setError(null)
      setLocation({
        timestamp,
        accuracy: coords.accuracy,
        altitude: coords.altitude,
        altitudeAccuracy: coords.altitudeAccuracy,
        heading: coords.heading,
        latitude: coords.latitude,
        longitude: coords.longitude,
        speed: coords.speed,
      })

      dispatch(prev => ({...prev, userCoords: [coords.longitude, coords.latitude]}))
    }

    const handleError = (error: GeolocationPositionError) => {
      setIsLoading(false)
      setError(error)
    }

    navigator.geolocation.getCurrentPosition(handleLocation, handleError)
    const watchId = navigator.geolocation.watchPosition(handleLocation, handleError)
    return () => navigator.geolocation.clearWatch(watchId)
  }, [])

  useEffect(() => {
    // TODO: iOS support

    const handleOrientation = ({absolute, alpha, beta, gamma}: DeviceOrientationEvent) => {
      if (!absolute || alpha == null || beta == null || gamma == null) {
        return
      }

      let compassHeading = -(alpha + beta * gamma / 90)
      compassHeading -= Math.floor(compassHeading / 360) * 360

      setCompass(compassHeading)
    }

    // eslint-disable-next-line @typescript-eslint/ban-ts-comment
    // @ts-ignore
    window.addEventListener("deviceorientationabsolute", handleOrientation)

    // eslint-disable-next-line @typescript-eslint/ban-ts-comment
    // @ts-ignore
    return () => window.removeEventListener("deviceorientationabsolute", handleOrientation)
  }, [])

  return {location, isLoading, error, compassHeading: compass}
}
