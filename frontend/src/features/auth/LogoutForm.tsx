import { FormEvent } from "react"
import { useLogoutMutation } from "./authApiSlice"
import { logout as sendLogout } from "./authSlice"
import { useDispatch } from "react-redux"


const LogoutForm = () => {
    const dispatch = useDispatch()
    const [logout] = useLogoutMutation()

    const handleSubmit = async (e: FormEvent<HTMLFormElement>) => {
        e.preventDefault()
        try {
            await logout(undefined).unwrap()
            dispatch(sendLogout())
        } catch (error) {
            console.error(error)
        }
    }

    return (
        <form onSubmit={handleSubmit}>
            <button className="py-1.5 px-4 rounded-sm text-white 
            font-semibold bg-indigo-400 hover:bg-indigo-300 focus:bg-indigo-200"
            >
                Log out
            </button>
        </form>
    )
}

export default LogoutForm