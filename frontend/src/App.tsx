import {
  createBrowserRouter,
  createRoutesFromElements,
  Route,
  RouterProvider
}from "react-router-dom"

import Layout from "./layouts/Layout"
import LoginPage from "./features/auth/LoginPage"
import RequireAuth from "./features/auth/RequireAuth"
import RequireNoAuth from "./features/auth/RequireNoAuth"
import Refresh from "./features/auth/Refresh"
import StandardsPage from "./features/standards/StandardsPage"
import ProjectsPage from "./pages/ProjectsPage"
import StandardDetails from "./features/standards/StandardDetails"
import UserRegisterPage from "./features/users/UserRegisterPage"

const router = createBrowserRouter(createRoutesFromElements(
  <Route element={<Refresh />}>
    <Route element={<Layout />}>
      <Route element={<RequireAuth />}>
        <Route index element={<ProjectsPage />} />
        <Route path="/standards/" element={<StandardsPage />} />
        <Route path="/standards/:id" element={<StandardDetails />} />
      </Route>
      <Route element={<RequireNoAuth />}> 
        <Route path="/login" element={<LoginPage />} />
        <Route path="/register" element={<UserRegisterPage />} />
      </Route>
    </Route>
  </Route>
))


const App = () => <RouterProvider router={router} />

export default App