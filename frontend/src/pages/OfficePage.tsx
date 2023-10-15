import React, {useEffect} from "react"
import "./OfficePage.scss"
import {Navigate, useNavigate, useParams} from "react-router-dom"
import {useMapContext, useStore} from "../store"
import {confirmTap, getRoutesByTeller} from "../utils/backend"
import {distance} from "@turf/turf"
import {FaCarRear, FaPersonWalking, FaXmark} from "react-icons/fa6"
import {Button} from "../components"
import {formatDistance, reduceSchedule} from "../utils"
import {metroIcon} from "../assets"
import {FaClock, FaUserFriends, FaUserTie} from "react-icons/fa"
import {TbDisabled} from "react-icons/tb"
import ServiceLoad from "../components/ServiceLoad"

export default function OfficePage(): React.JSX.Element {
  const themeParams = window.Telegram.WebApp.themeParams
  const navigate = useNavigate()
  const {officeId} = useParams()
  const [state, dispatch] = useStore()
  const mapRef = useMapContext()

  const office = state.offices.find(v => v.id === officeId)

  useEffect(() => {
    if (office !== undefined) {
      mapRef.current?.flyTo({
        center: [office.coordinate.lng, office.coordinate.lat],
        duration: 750,
        zoom: 15,
      })

      void confirmTap(office.id, "office")
    }
  }, [office, mapRef])

  useEffect(() => {
    return () => dispatch(prev => ({...prev, route: null}))
  }, [dispatch])

  if (office === undefined) {
    return <Navigate to="/"/>
  }

  const buildRoute = () => {
    if (office === undefined) return

    const userCoords = state.userCoords

    if (userCoords === null) {
      window.open(
        `https://maps.yandex.ru/?ll=${office.coordinate.lng},${office.coordinate.lat}&z=15`,
        "_blank"
      )?.focus()
      return
    }

    const profile = distance(
      userCoords, [office.coordinate.lng, office.coordinate.lat],
      {units: "meters"}
    ) > 3000 ? "driving-car" : "foot-walking"


    getRoutesByTeller(
      userCoords,
      office.id,
      "office",
      profile,
    ).then(route => {
      dispatch(prev => ({...prev, route}))
    })

    mapRef.current?.fitBounds(
      [userCoords, [office.coordinate.lng, office.coordinate.lat]],
      {
        duration: 750,
        padding: 40
      }
    )
  }

  const officeDistance = state.userCoords !== null
    ? distance(state.userCoords, [office.coordinate.lng, office.coordinate.lat], {units: "meters"})
    : null

  return (
    <div className="OfficePage">
      <div className="OfficePage__header">
        <span>{office.salePointName}</span>
        <div onClick={() => navigate("/")}>
          <FaXmark color={themeParams.button_color} size={24}/>
        </div>
      </div>
      <span className="OfficePage__address">
        {office.address}
      </span>
      <div className="OfficePage__navigation">
        <Button onClick={() => buildRoute()}>
          {
            officeDistance === null
              ? `Построить маршрут`
              : `Построить маршрут · ${formatDistance(officeDistance)}`
          }
        </Button>
        <div className="OfficePage__duration">
          <div>
            <span>{office.durationWalk !== undefined ? `${office.durationWalk} мин` : "--"}</span>
            <FaPersonWalking color={themeParams.button_color} size={15}/>
          </div>
          <div>
            <span>{office.durationCar !== undefined ? `${office.durationCar} мин` : "--"}</span>
            <FaCarRear color={themeParams.button_color} size={15}/>
          </div>
        </div>
      </div>
      {
        office.closestMetro &&
          <div className="OfficePage__feature">
            <img src={metroIcon} alt=""/>
            <div>
              <span>
                {`м. ${office.closestMetro.name}`}
              </span>
              <span>
                {`${office.closestMetro.line} линия`}
              </span>
            </div>
          </div>
      }
      <div className="OfficePage__separator"/>
      <span className="OfficePage__title">
        Загруженность в ближайшее время
      </span>
      <ServiceLoad load={office.load}/>
      <div className="OfficePage__separator"/>
      <span className="OfficePage__title">
        Режим работы отделения
      </span>
      <div className="OfficePage__schedule">
        <span className="OfficePage__title">
          Для физических лиц
        </span>
        <div>
          <FaClock color={themeParams.button_color} size={14}/>
          <span>
            {reduceSchedule(office.individualSchedule).join("\n")}
          </span>
        </div>
      </div>
      <div className="OfficePage__schedule">
        <span className="OfficePage__title">
          Для юридических лиц
        </span>
        <div>
          <FaClock color={themeParams.button_color} size={14} style={{marginTop: 4}}/>
          <span>
            {reduceSchedule(office.legalEntitySchedule).join("\u000A")}
          </span>
        </div>
      </div>
      <div className="OfficePage__separator"/>
      <span className="OfficePage__title">
        Обслуживание
      </span>
      {
        office.features.some(v => v.startsWith("INDIVIDUAL"))
          && (
            <div className="OfficePage__feature">
              <FaUserFriends color={themeParams.button_color} size={24}/>
              <div>
                <span>Физические лица</span>
                <span>Все клиенты банка</span>
              </div>
            </div>
          )
      }
      {
        office.features.some(v => v.startsWith("LEGAL_ENTITY"))
        && (
          <div className="OfficePage__feature">
            <FaUserTie color={themeParams.button_color} size={24}/>
            <div>
              <span>Юридические лица</span>
            </div>
          </div>
        )
      }

      {
        office.features.includes("HAS_RAMP")
        && (
          <>
            <div className="OfficePage__separator"/>
            <div className="OfficePage__feature">
              <TbDisabled color={themeParams.button_color} size={24}/>
              <div>
                <span>Доступно для маломобильных граждан</span>
              </div>
            </div>
          </>
        )
      }
    </div>
  )
}
