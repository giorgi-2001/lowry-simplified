import { Outlet } from "react-router-dom"
import Header from "../components/Header"


const Layout = () => {

    const currentYear = new Date().getFullYear()

  return (
    <>
        <Header />
        <main className="grow py-8">
            <Outlet />
        </main>
        <footer>
            <div className="wrapper">
                <p className="text-center py-4 border-t border-zinc-300">
                    <span>&copy;Lowry Simplified, </span>
                    <span>{currentYear}</span>
                </p>
            </div>
        </footer>
    </>
  )
}

export default Layout