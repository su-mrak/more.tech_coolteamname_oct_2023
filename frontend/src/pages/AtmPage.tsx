import React, {useEffect} from "react"
import "./AtmPage.scss"
import {Navigate, useNavigate, useParams} from "react-router-dom"
import {useMapContext, useStore} from "../store"
import {confirmTap, getRoutesByTeller} from "../utils/backend"
import {distance} from "@turf/turf"
import {FaCarRear, FaNfcSymbol, FaPersonWalking, FaXmark} from "react-icons/fa6"
import {Button} from "../components"
import {formatDistance} from "../utils"
// import {metroIcon} from "../assets"
import {FaClock, FaEyeSlash, FaQrcode, FaUserFriends, FaWallet} from "react-icons/fa"
import {TbDisabled} from "react-icons/tb"
import {metroIcon} from "../assets"
import ServiceLoad from "../components/ServiceLoad"


export default function AtmPage(): React.JSX.Element {
  const themeParams = window.Telegram.WebApp.themeParams
  const navigate = useNavigate()
  const {atmId} = useParams()
  const [state, dispatch] = useStore()
  const mapRef = useMapContext()

  const atm = state.atms.find(v => v.id === atmId)

  useEffect(() => {
    if (atm !== undefined) {
      mapRef.current?.flyTo({
        center: [atm.coordinate.lng, atm.coordinate.lat],
        duration: 750,
        zoom: 15,
      })

      void confirmTap(atm.id, "atm")
    }
  }, [atm, mapRef])

  useEffect(() => {
    return () => dispatch(prev => ({...prev, route: null}))
  }, [dispatch])

  if (atm === undefined) {
    return <Navigate to="/"/>
  }

  const buildRoute = () => {
    if (atm === undefined) return

    const userCoords = state.userCoords

    if (userCoords === null) {
      window.open(
        `https://maps.yandex.ru/?ll=${atm.coordinate.lng},${atm.coordinate.lat}&z=15`,
        "_blank"
      )?.focus()
      return
    }

    const profile = distance(
      userCoords, [atm.coordinate.lng, atm.coordinate.lat],
      {units: "meters"}
    ) > 3000 ? "driving-car" : "foot-walking"

    getRoutesByTeller(
      userCoords,
      atm.id,
      "atm",
      profile,
    ).then(route => {
      dispatch(prev => ({...prev, route}))
    })

    mapRef.current?.fitBounds(
      [userCoords, [atm.coordinate.lng, atm.coordinate.lat]],
      {
        duration: 750,
        padding: 40
      }
    )
  }

  const atmDistance = state.userCoords !== null
    ? distance(state.userCoords, [atm.coordinate.lng, atm.coordinate.lat], {units: "meters"})
    : null

  return (
    <div className="AtmPage">
      <div className="OfficePage__header">
        <span>Банкомат {atm.id.slice(0, 8)}</span>
        <div onClick={() => navigate("/")}>
          <FaXmark color={themeParams.button_color} size={24}/>
        </div>
      </div>
      <span className="OfficePage__address">
        {atm.address}
      </span>
      <div className="OfficePage__navigation">
        <Button onClick={() => buildRoute()}>
          {
            atmDistance === null
              ? `Построить маршрут`
              : `Построить маршрут · ${formatDistance(atmDistance)}`
          }
        </Button>
        <div className="OfficePage__duration">
          <div>
            <span>{atm.durationWalk !== undefined ? `${atm.durationWalk} мин` : "--"}</span>
            <FaPersonWalking color={themeParams.button_color} size={15}/>
          </div>
          <div>
            <span>{atm.durationCar !== undefined ? `${atm.durationCar} мин` : "--"}</span>
            <FaCarRear color={themeParams.button_color} size={15}/>
          </div>
        </div>
      </div>
      {
        atm.closestMetro &&
        <div className="AtmPage__feature">
          <img src={metroIcon} alt=""/>
          <div>
              <span>
                {`м. ${atm.closestMetro.name}`}
              </span>
            <span>
                {`${atm.closestMetro.line} линия`}
              </span>
          </div>
        </div>
      }
      <div className="OfficePage__separator"/>
      <span className="OfficePage__title">
        Загруженность в ближайшее время
      </span>
      <ServiceLoad load={atm.load}/>
      <div className="AtmPage__separator"/>
      <div className="AtmPage__feature">
        <FaUserFriends color={themeParams.button_color} size={24}/>
        <div>
          <span>Внесение и выдача наличных</span>
        </div>
      </div>
      <div className="AtmPage__feature">
        <FaWallet color={themeParams.button_color} size={24}/>
        <div>
          <span>Платежи наличными или картой</span>
        </div>
      </div>
      <div className="AtmPage__feature">
        <FaClock color={themeParams.button_color} size={24}/>
        <div>
          <span>Работает круглосуточно</span>
        </div>
      </div>
      <div className="AtmPage__separator"/>
      <div className="AtmPage__money">
        <span>Снять</span>
        <div>
          {
            atm.features.includes("WITHDRAWAL_RUB") &&
              <span className="AtmPage__money-icon">
                ₽
              </span>
          }
          {
            atm.features.includes("WITHDRAWAL_USD") &&
              <span className="AtmPage__money-icon">
                $
              </span>
          }
          {
            atm.features.includes("WITHDRAWAL_EUR") &&
              <span className="AtmPage__money-icon">
                €
              </span>
          }
        </div>
      </div>
      <div className="AtmPage__money">
        <span>Внести</span>
        <div>
          {
            atm.features.includes("REPLENISHMENT_RUB") &&
            <span className="AtmPage__money-icon">
                ₽
              </span>
          }
          {
            atm.features.includes("REPLENISHMENT_USD") &&
            <span className="AtmPage__money-icon">
                $
              </span>
          }
          {
            atm.features.includes("REPLENISHMENT_EUR") &&
            <span className="AtmPage__money-icon">
                €
              </span>
          }
        </div>
      </div>
      <div className="AtmPage__separator"/>
      {
        atm.features.includes("NFC_FOR_BANK_CARDS")
          && (
            <div className="AtmPage__feature">
              <FaNfcSymbol color={themeParams.button_color} size={24}/>
              <div>
                <span>NFC (бесконтактное обслуживание)</span>
              </div>
            </div>
          )
      }
      {
        atm.features.includes("QR_READ")
        && (
          <div className="AtmPage__feature">
            <FaQrcode color={themeParams.button_color} size={24}/>
            <div>
              <span>Снятие наличных и платежи по QR-коду</span>
            </div>
          </div>
        )
      }
      {
        atm.features.includes("WHEELCHAIR")
        && (
          <div className="AtmPage__feature">
            <TbDisabled color={themeParams.button_color} size={24}/>
            <div>
              <span>Доступно для маломобильных граждан</span>
            </div>
          </div>
        )
      }
      {
        atm.features.includes("BLIND")
        && (
          <div className="AtmPage__feature">
            <FaEyeSlash color={themeParams.button_color} size={24}/>
            <div>
              <span>Доступно для слабовидящих граждан</span>
            </div>
          </div>
        )
      }
    </div>
  )
}
