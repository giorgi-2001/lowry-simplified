import { FormEvent, useState } from "react"
import useValidateForm from "./useValidateForm"
import { useRequestPasswordResetMutation } from "./userApiSlice"


const PwdResetInit = () => {
    const [email, setEmail] = useState<string>("")
    const [error, setError] = useState<string>("")
    const [successMessage, setSuccessMessage] = useState("")

    const {
        emailError, validateEmail,
    } = useValidateForm()

    const canNotSubmit =  () => !email || Boolean(error) || Boolean(emailError)

    const [requestPasswordReset] = useRequestPasswordResetMutation()

    const handleSubmit = async (e: FormEvent<HTMLFormElement>) => {
        e.preventDefault()

        if (canNotSubmit()) return

        try {
            setError("")
            const data = { email }
            const responseData = await requestPasswordReset(data).unwrap()
            setSuccessMessage(responseData.detail)
        } catch (error: any) {
            setError(JSON.stringify(error.data.detail))
        }
    }

    const reponseFlash = (
        <div className="w-[50%] min-w-fit p-8 mx-auto text-teal-700 font-semibold bg-teal-100 border border-teal-200 rounded-sm">
            <p className="text-center">{successMessage}</p>
        </div>
    )

    const requestForm = (
        <div className="w-[50%] min-w-fit p-8 mx-auto bg-zinc-100 border border-zinc-200 rounded-sm">
            <h1 className="mb-8 text-center text-xl">Request Password Reset:</h1>
            <form onSubmit={handleSubmit}>
                <div className="mb-6">
                    <label className="block mb-1 ml-1" htmlFor="email">
                        Enter your Email
                    </label>
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
                <div className="flex items-center gap-4 justify-between">
                    <button 
                        disabled={canNotSubmit()}
                        className="
                        button block
                        bg-indigo-400 w-fit px-6 py-1.5 text-white 
                        font-semibold rounded-sm hover:bg-indigo-300 
                        focus:bg-indigo-200 disabled:opacity-50 disabled:hover:opacity-50
                        disabled:hover:bg-indigo-400 disabled:cursor-not-allowed">
                        Submit 
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
        {Boolean(successMessage) ? reponseFlash : requestForm}
    </section>
  )
}

export default PwdResetInit