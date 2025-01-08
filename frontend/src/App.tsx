import {
  createBrowserRouter,
  createRoutesFromElements,
  Route,
  RouterProvider
}from "react-router-dom"

import Layout from "./layouts/Layout"
import LoginPage from "./pages/LoginPage"
import HomePage from "./pages/HomePage"
import RequireAuth from "./features/auth/RequireAuth"
import RequireNoAuth from "./features/auth/RequireNoAuth"
import Refresh from "./features/auth/Refresh"

const router = createBrowserRouter(createRoutesFromElements(
  <Route element={<Refresh />}>
    <Route element={<Layout />}>
      <Route element={<RequireAuth />}>
        <Route index element={<HomePage />} />
      </Route>
      <Route element={<RequireNoAuth />}> 
        <Route path="/login" element={<LoginPage />} />
      </Route>
    </Route>
  </Route>
))


const App = () => <RouterProvider router={router} />

export default App