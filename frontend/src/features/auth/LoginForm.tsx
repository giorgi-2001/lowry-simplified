import { useLoginMutation } from "./authApiSlice"
import { FormEvent, useState } from "react"
import { Link } from "react-router-dom"


const LoginForm = () => {
    const [username, setUsername] = useState<string>("")
    const [password, setPassword] = useState<string>("")
    const [showPassword, setShowPassword] = useState<boolean>(false)
    const [error, setError] = useState<string>("")

    const canNotSubmit = !username || !password

    const [login] = useLoginMutation()

    const handleSubmit = async (e: FormEvent<HTMLFormElement>) => {
        e.preventDefault()

        if (canNotSubmit) {
            setError("Field are required")
            return
        }

        setError("")

        try {
            const data = {
                username: username,
                password: password
            }
            setError("")
            await login(data).unwrap()
        } catch (error: any) {
            setError(error.data.detail)
        }
    }


  return (
    <form onSubmit={handleSubmit} className="flex flex-col gap-4">
        <div>
            <label className="block mb-1 ml-1" htmlFor="username">Username</label>
            <input
                className="block w-full py-1 px-2 text-inherit border border-zinc-200"
                type="text"
                id="username"
                value={username}
                onChange={(e) => setUsername(e.target.value)}
            />
        </div>
        <div>
            <label className="block mb-1 ml-1" htmlFor="password">Password</label>
            <input
                className="block w-full py-1 px-2 text-inherit border border-zinc-200"
                type={showPassword ? "text" : "password"}
                id="password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
            />
        </div>
        <div className="flex gap-4 justify-end pr-4">
            <label className="block mb-1 ml-1" htmlFor="show-pass">
                Show Password
            </label>
            <input
                type="checkbox"
                id="show-pass"
                checked={showPassword}
                onChange={(e) => setShowPassword(e.target.checked)}
            />
        </div>
        <div className="flex items-center gap-4 justify-between">
            <button disabled={canNotSubmit} className="
                button block
                bg-indigo-400 w-fit px-6 py-1.5 text-white 
                font-semibold rounded-sm hover:bg-indigo-300 
                focus:bg-indigo-200 disabled:hover:bg-indigo-400 
                disabled:opacity-50 disabled:cursor-not-allowed
            ">
                Log in
            </button>
            <p className="text-sm">
                <span>No account yet? </span>
                <Link className="font-semibold text-indigo-600 hover:underline" to="/register">
                    Register
                </Link>
            </p>
        </div>

        {
            error && 
            <p aria-live="assertive"
                className="text-center mt-2 p-2
                 bg-red-200 text-red-800 border
                  border-red-800 rounded-sm">
                {error}
            </p>
        }
    </form>
  )
}

export default LoginForm