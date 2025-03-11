import { useRegisterUserMutation } from "./userApiSlice"
import { FormEvent, useState } from "react"
import { Link, useNavigate } from "react-router-dom"
import useValidateForm from "./useValidateForm"


const UserRegisterForm = () => {
    const [username, setUsername] = useState<string>("")
    const [password, setPassword] = useState<string>("")   
    const [password2, setPassword2] = useState<string>("")
    const [email, setEmail] = useState<string>("")
    const [showPassword, setShowPassword] = useState<boolean>(false)
    const [error, setError] = useState<string>("")

    const {
        usernameError, validateUsername,
        emailError, validateEmail,
        passwordError, validatePassword,
        password2Error, validatePassword2
    } = useValidateForm()

    const validInput = !usernameError && !passwordError && !password2Error && !emailError
    const emptyFields = !username || !email || !password || !password2
    const canNotSubmit = !validInput || emptyFields

    console.log(canNotSubmit)

    const [ register ] = useRegisterUserMutation()

    const navigate = useNavigate()


    const handleSubmit = async (e: FormEvent<HTMLFormElement>) => {
        e.preventDefault()

        try {
            const data = { username, email, password }
            setError("")
            await register(data).unwrap()
            navigate("/login")
        } catch (error: any) {
            setError(error.data.detail)
        }
    }

  return (
    <form onSubmit={handleSubmit} className="flex flex-col gap-4">
        <div>
            <label className="block mb-1 ml-1" htmlFor="username">Username</label>
            <input
                className={`block w-full py-1 px-2 text-inherit border border-zinc-200 rounded-[3px] ${usernameError ? "border-2 border-red-500" : "" }`}
                type="text"
                id="username"
                value={username}
                onChange={(e) => setUsername(e.target.value)}
                onBlur={validateUsername}
            />
            { usernameError && 
                <p className="text-red-500 pl-2 text-sm font-semibold mt-1">
                    {usernameError}
                </p> }
        </div>
        <div>
            <label className="block mb-1 ml-1" htmlFor="email">Email</label>
            <input
                className={`block w-full py-1 px-2 text-inherit border border-zinc-200 rounded-[3px] ${emailError ? "border-2 border-red-500" : "" }`}
                type="text"
                id="email"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                onBlur={validateEmail}
            />
            { emailError && 
                <p className="text-red-500 pl-2 text-sm font-semibold mt-1">
                    {emailError}
                </p> }
        </div>
        <div>
            <label className="block mb-1 ml-1" htmlFor="password">Password</label>
            <input
                className={`block w-full py-1 px-2 text-inherit border border-zinc-200 rounded-[3px] ${passwordError ? "border-2 border-red-500" : "" }`}
                type={showPassword ? "text" : "password"}
                id="password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                onBlur={validatePassword}
            />
            { passwordError && 
                <p className="pl-2 text-red-500 text-sm font-semibold mt-1">
                    {passwordError}
                </p> }
        </div>

        <div>
            <label className="block mb-1 ml-1" htmlFor="password2">
                Confirm Password
            </label>
            <input
                className={`block w-full py-1 px-2 text-inherit border border-zinc-200 rounded-[3px] ${password2Error ? "border-2 border-red-500" : "" }`}
                type={showPassword ? "text" : "password"}
                id="password2"
                value={password2}
                onChange={(e) => setPassword2(e.target.value)}
                onBlur={(e) => validatePassword2(e, password)}
            />
            { password2Error && 
                <p className="pl-2 text-red-500 text-sm font-semibold mt-1">
                    {password2Error}
                </p> }
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
            <button 
                disabled={canNotSubmit}
                className="
                button block
                bg-indigo-400 w-fit px-6 py-1.5 text-white 
                font-semibold rounded-sm hover:bg-indigo-300 
                focus:bg-indigo-200 disabled:opacity-50 disabled:hover:opacity-50
                disabled:hover:bg-indigo-400 disabled:cursor-not-allowed">
                Sign up
            </button>
            <p className="text-sm">
                <span>Already have an account? </span>
                <Link className="font-semibold text-indigo-600 hover:underline" to="/login">Log in</Link>
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

export default UserRegisterForm