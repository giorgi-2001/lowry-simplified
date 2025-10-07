import LoginForm from "./LoginForm"
import { Link } from "react-router-dom"

const LoginPage = () => {
  return (
    <section className="wrapper">
        <div className="w-[50%] min-w-fit p-8 mx-auto bg-zinc-100 border border-zinc-200 rounded-sm">
            <h1 className="mb-8 text-center text-xl">Login</h1>
            <LoginForm />
            <div className="mt-6 text-center text-sm font-semibold text-zinc-700">
                <span>Forgot Password? </span>
                <Link className="text-indigo-500 hover:underline" to="/password-reset">
                    Click here to reset it
                </Link>
            </div>
        </div>
    </section>
  )
}

export default LoginPage