import { selectToken } from "./authSlice"
import { useSelector } from "react-redux"
import { Outlet, Navigate } from "react-router-dom"


const RequireNoAuth = () => {
    const token = useSelector(selectToken)
    console.log("Token: ", token)

    if (token) {
        return <Navigate to=""  replace={true} />
    }

    return <Outlet />
}

export default RequireNoAuth