import React, {useState} from "react"
import {useStore} from "../store"
import {FaXmark} from "react-icons/fa6"
import {AtmFeature} from "../utils/backend"
import "./AtmFilters.scss"
import {Button, Checkbox} from "../components"
import {useNavigate} from "react-router-dom"

export default function AtmFilters(): React.JSX.Element {
  const themeParams = window.Telegram.WebApp.themeParams
  const [state, dispatch] = useStore()
  const [filters, setFilters] = useState<AtmFeature[]>(state.atmFilters)
  const navigate = useNavigate()

  const handleUpdate = (feature: AtmFeature) => {
    return () => {
      if (filters.includes(feature)) {
        setFilters(filters.filter(v => v != feature))
      } else {
        setFilters([...filters, feature])
      }
    }
  }

  const handleSave = () => {
    dispatch((prev) => ({...prev, atmFilters: filters}))
    navigate("/")
  }

  return (
    <div className="AtmFilters">
      <div className="AtmFilters__header">
        <span>Фильтры банкоматов</span>
        <div onClick={() => navigate("/")}>
          <FaXmark color={themeParams.button_color} size={24}/>
        </div>
      </div>
      <span
        className="AtmFilters__reset"
        onClick={() => setFilters([])}
      >
        Сбросить фильтры
      </span>
      <div className="AtmFilters__money">
        <span>Внести</span>
        <div>
          <span
            className={`
              AtmFilters__money-button
              ${
                filters.includes("REPLENISHMENT_RUB") ?
                  "AtmFilters__money-button-active" : ""
              }
            `}
            onClick={handleUpdate("REPLENISHMENT_RUB")}
          >
            ₽
          </span>
          <span
            className={`
              AtmFilters__money-button
              ${
                filters.includes("REPLENISHMENT_USD") ?
                  "AtmFilters__money-button-active" : ""
              }
            `}
            onClick={handleUpdate("REPLENISHMENT_USD")}
          >
            $
          </span>
          <span
            className={`
              AtmFilters__money-button
              ${
                filters.includes("REPLENISHMENT_EUR") ?
                  "AtmFilters__money-button-active" : ""
              }
            `}
            onClick={handleUpdate("REPLENISHMENT_EUR")}
          >
            €
          </span>
        </div>
      </div>
      <div className="AtmFilters__money">
        <span>Снять</span>
        <div>
          <span
            className={`
              AtmFilters__money-button
              ${
                filters.includes("WITHDRAWAL_RUB") ?
                  "AtmFilters__money-button-active" : ""
              }
            `}
            onClick={handleUpdate("WITHDRAWAL_RUB")}
          >
            ₽
          </span>
          <span
            className={`
              AtmFilters__money-button
              ${
                filters.includes("WITHDRAWAL_USD") ?
                  "AtmFilters__money-button-active" : ""
              }
            `}
            onClick={handleUpdate("WITHDRAWAL_USD")}
          >
            $
          </span>
          <span
            className={`
              AtmFilters__money-button
              ${
                filters.includes("WITHDRAWAL_EUR") ?
                  "AtmFilters__money-button-active" : ""
              }
            `}
            onClick={handleUpdate("WITHDRAWAL_EUR")}
          >
            €
          </span>
        </div>
      </div>
      <div className="AtmFilters__separator"/>
      <div className="AtmFilters__feature">
        <span>Поддержка NFC</span>
        <Checkbox
          onClick={handleUpdate("NFC_FOR_BANK_CARDS")}
          checked={filters.includes("NFC_FOR_BANK_CARDS")}
        />
      </div>
      <div className="AtmFilters__feature">
        <span>Снятие наличных по QR-коду</span>
        <Checkbox
          onClick={handleUpdate("QR_READ")}
          checked={filters.includes("QR_READ")}
        />
      </div>
      <div className="AtmFilters__feature">
        <span>Оборудован для слабовидящих</span>
        <Checkbox
          onClick={handleUpdate("BLIND")}
          checked={filters.includes("BLIND")}
        />
      </div>
      <div className="AtmFilters__feature">
        <span>Доступно для маломобильных граждан</span>
        <Checkbox
          onClick={handleUpdate("WHEELCHAIR")}
          checked={filters.includes("WHEELCHAIR")}
        />
      </div>
      <Button style={{marginTop: 32}} onClick={handleSave}>
        Применить
      </Button>
    </div>

  )
}
