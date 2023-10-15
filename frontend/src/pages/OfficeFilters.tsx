import React, {useState} from "react"
import {useStore} from "../store"
import {FaXmark} from "react-icons/fa6"
import {OfficeFeature} from "../utils/backend"
import {Button, Checkbox} from "../components"
import {useNavigate} from "react-router-dom"
import "./OfficeFilters.scss"

export default function OfficeFilters(): React.JSX.Element {
  const themeParams = window.Telegram.WebApp.themeParams
  const [state, dispatch] = useStore()
  const [filters, setFilters] = useState<OfficeFeature[]>(state.officeFilters)
  const navigate = useNavigate()

  const handleUpdate = (feature: OfficeFeature) => {
    return () => {
      if (filters.includes(feature)) {
        setFilters(filters.filter(v => v != feature))
      } else {
        setFilters([...filters, feature])
      }
    }
  }

  const handleSave = () => {
    dispatch((prev) => ({...prev, officeFilters: filters}))
    navigate("/")
  }

  return (
    <div className="OfficeFilters">
      <div className="OfficeFilters__header">
        <span>Фильтры отделений</span>
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
      <span className="OfficeFilters__subtitle">
        Для физических лиц
      </span>
      <div className="OfficeFilters__feature">
        <span>Ипотечное кредитование</span>
        <Checkbox
          onClick={handleUpdate("INDIVIDUAL_MORTGAGE_LENDING")}
          checked={filters.includes("INDIVIDUAL_MORTGAGE_LENDING")}
        />
      </div>
      <div className="OfficeFilters__feature">
        <span>Пополнение счетов</span>
        <Checkbox
          onClick={handleUpdate("INDIVIDUAL_DEPOSITS")}
          checked={filters.includes("INDIVIDUAL_DEPOSITS")}
        />
      </div>
      <div className="OfficeFilters__feature">
        <span>Обмен валют</span>
        <Checkbox
          onClick={handleUpdate("INDIVIDUAL_CURRENCY_EXCHANGE_OPERATIONS")}
          checked={filters.includes("INDIVIDUAL_CURRENCY_EXCHANGE_OPERATIONS")}
        />
      </div>

      <span className="OfficeFilters__separator"/>
      <span className="OfficeFilters__subtitle">
        Для юридических лиц
      </span>
      <div className="OfficeFilters__feature">
        <span>Кредитование</span>
        <Checkbox
          onClick={handleUpdate("LEGAL_ENTITY_LENDING")}
          checked={filters.includes("LEGAL_ENTITY_LENDING")}
        />
      </div>
      <div className="OfficeFilters__feature">
        <span>Рассчётные услуги</span>
        <Checkbox
          onClick={handleUpdate("LEGAL_ENTITY_SETTLEMENT_SERVICE")}
          checked={filters.includes("LEGAL_ENTITY_SETTLEMENT_SERVICE")}
        />
      </div>

      <span className="OfficeFilters__separator"/>
      <span className="OfficeFilters__subtitle">
        Дополнительно
      </span>
      <div className="OfficeFilters__feature">
        <span>Доступно для маломобильных граждан</span>
        <Checkbox
          onClick={handleUpdate("HAS_RAMP")}
          checked={filters.includes("HAS_RAMP")}
        />
      </div>

      <Button style={{marginTop: 32}} onClick={handleSave}>
        Применить
      </Button>
    </div>

  )
}
