import LogoutForm from "../features/auth/LogoutForm"

const Header = () => {
  return (
    <header>
        <div className="wrapper">
            <nav className="flex items-center justify-end gap-8 py-4 border-b border-zinc-300">
                <h1 className="mr-auto">Lowry simplified</h1>
                <LogoutForm />
            </nav>
        </div>
    </header>
  )
}

export default Header