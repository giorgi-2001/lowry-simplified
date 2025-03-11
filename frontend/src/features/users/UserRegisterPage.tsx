import UserRegisterForm from "./UserRegisterForm"

const UserRegisterPage = () => {

    return (
        <section className="wrapper">
            <div className="w-[50%] min-w-fit p-8 mx-auto bg-zinc-100 border border-zinc-200 rounded-sm">
                <h1 className="mb-8 text-center text-xl">Sign up</h1>
                <UserRegisterForm />
            </div>
        </section>
      )
}

export default UserRegisterPage