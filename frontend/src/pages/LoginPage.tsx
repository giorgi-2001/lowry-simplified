import LoginForm from "../features/auth/LoginForm"

const LoginPage = () => {
  return (
    <section className="wrapper">
        <div className="w-[50%] min-w-fit p-8 mx-auto bg-zinc-100 border border-zinc-200 rounded-sm">
            <h1 className="mb-8 text-center text-xl">Login</h1>
            <LoginForm />
        </div>
    </section>
  )
}

export default LoginPage