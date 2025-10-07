import { FormEvent, useState } from "react"
import useValidateForm from "./useValidateForm"
import { usePasswordResetConfirmMutation } from "./userApiSlice"
import { useSearchParams, Link } from "react-router-dom"


const PwdResetConfirm = () => {
    const [password, setPassword] = useState("")
    const [password2, setPassword2] = useState("")
    const [showPassword, setShowPassword] = useState(false)
    
    const [error, setError] = useState("")
    const [successMessage, setSuccessMessage] = useState("")

    const {
        passwordError, password2Error, validatePassword, validatePassword2
    } = useValidateForm()


    const haveSomeErrors = [passwordError, password2Error, error].some(Boolean)
    const emptyFields = !password || !password2

    const canNotSubmit = () => haveSomeErrors || emptyFields

    const [searchParams] = useSearchParams()
    const token = searchParams.get("token")

    if (!token) return null

    const [passwordResetConfirm] = usePasswordResetConfirmMutation()


    const handleSubmit = async (e: FormEvent<HTMLFormElement>) => {
        e.preventDefault()
        if (canNotSubmit()) return
        try {
            setError("")
            const data = { token, password }
            const responseData = await passwordResetConfirm(data).unwrap()
            setSuccessMessage(responseData.detail)
        } catch (err) {
            console.log(err)
            setError(JSON.stringify(err))
        }
    }

    const reponseFlash = (
        <div className="w-[50%] min-w-fit p-8 mx-auto text-teal-700 font-semibold bg-teal-100 border border-teal-200 rounded-sm">
            <p className="text-center mb-6">{successMessage}</p>
            <p className="text-center">
                <span>Go to the </span>
                <Link className="text-indigo-500 hover:underline" to="/">
                    Login Page
                </Link>
            </p>
        </div>
    )
    
    const requestForm = (
        <div className="w-[50%] min-w-fit p-8 mx-auto bg-zinc-100 border border-zinc-200 rounded-sm">
            <h1 className="mb-8 text-center text-xl">Reset the Password</h1>
            <form onSubmit={handleSubmit} className="flex flex-col gap-4">
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
                        disabled={canNotSubmit()}
                        className="
                        button block
                        bg-indigo-400 w-fit px-6 py-1.5 text-white 
                        font-semibold rounded-sm hover:bg-indigo-300 
                        focus:bg-indigo-200 disabled:opacity-50 disabled:hover:opacity-50
                        disabled:hover:bg-indigo-400 disabled:cursor-not-allowed">
                        Reset
                    </button>
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
        </div>
    )

  return (
    <section className="wrapper">
        { Boolean(successMessage) ? reponseFlash : requestForm }
    </section>
  )
}

export default PwdResetConfirm