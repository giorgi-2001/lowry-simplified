import { useEffect, useRef } from "react"
import { useSelector } from "react-redux"
import { useRefreshMutation } from "./authApiSlice"
import { selectToken } from "./authSlice"
import { Outlet } from "react-router-dom"

const Refresh = () => {
    const [ refresh, { isLoading, isUninitialized } ] = useRefreshMutation()
    const token = useSelector(selectToken)

    const refreshAttempted = useRef(false)

    useEffect(() => {
        if (token || refreshAttempted.current) return

        const refreshState = async () => {
            try {
                await refresh(undefined).unwrap()
            } catch (error) {
                console.log(error)
            }
        }
    
        refreshState()

        return () => { refreshAttempted.current = true }
    }, [])
  
    if (isLoading || isUninitialized ) return <p>Loading...</p>

    return <Outlet />

}

export default Refresh