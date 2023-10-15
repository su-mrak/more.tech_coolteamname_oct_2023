import ReactDOM from "react-dom/client"
import router from "./App.tsx"
import {setupStyles} from "./utils"
import {StoreProvider} from "./store"
import {RouterProvider} from "react-router-dom"
import "./index.scss"

setupStyles()

ReactDOM.createRoot(document.getElementById("root")!).render(
  <StoreProvider>
    <RouterProvider router={router}/>
  </StoreProvider>,
)
