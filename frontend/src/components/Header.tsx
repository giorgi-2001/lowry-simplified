import LogoutForm from "../features/auth/LogoutForm"
import { NavLink } from "react-router-dom"
import { useSelector } from "react-redux"
import { selectToken } from "../features/auth/authSlice"

const Header = () => {

  const token = useSelector(selectToken)

  const logedInLinks = (
    <>
      <NavLink to="/">Projects</NavLink>
      <NavLink to="/standards/">Standards</NavLink>
      <LogoutForm />
    </>
  )

  const logedOutLinks = (
    <>
      <NavLink to="/login">Log in</NavLink>
      <NavLink to="/register">Sign up</NavLink>
    </>
  )

  const navContent = token ? logedInLinks : logedOutLinks

  return (
    <header>
        <div className="wrapper">
            <nav className="font-semibold text-zinc-600 flex items-center justify-end gap-8 py-4 border-b border-zinc-300">
                <h1 className="mr-auto text-xl">Lowry simplified</h1>

                { navContent }
            </nav>
        </div>
    </header>
  )
}

export default Header