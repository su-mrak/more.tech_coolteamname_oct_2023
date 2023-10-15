import React, {useEffect} from "react"
import {MenuContainer} from "./components"
import {createMemoryRouter, Outlet} from "react-router-dom"
import {AtmFilters, AtmPage, BanksMap, OfficeFilters, OfficePage, SearchPage} from "./pages"
import "./App.scss"
import "mapbox-gl/dist/mapbox-gl.css"

function App(): React.JSX.Element {
  const webApp = window.Telegram.WebApp

  useEffect(() => {
    webApp.expand()
  }, [webApp])

  return (
    <>
      <BanksMap/>
      <MenuContainer>
        <Outlet/>
      </MenuContainer>
    </>
  )
}


const router = createMemoryRouter([{
  element: <App/>,
  children: [
    {
      element: <SearchPage/>,
      path: "/",
    },
    {
      element: <OfficePage/>,
      path: "/office/:officeId"
    },
    {
      element: <AtmPage/>,
      path: "/atm/:atmId"
    },
    {
      element: <AtmFilters/>,
      path: "/filter/atm",
    },
    {
      element: <OfficeFilters/>,
      path: "/filter/office"
    }
  ]
}])

export default router
