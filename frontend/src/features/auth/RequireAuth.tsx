import { selectToken } from "./authSlice"
import { useSelector } from "react-redux"
import { Outlet, Navigate } from "react-router-dom"


const RequireAuth = () => {
    const token = useSelector(selectToken)

    if (!token) {
        return <Navigate to="/login" replace={true} />
    }

    return <Outlet />
}

export default RequireAuth