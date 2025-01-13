import { FormEvent, useState } from "react"
import { useDeleteStandardMutation } from "./standardApiSlice"
import { useNavigate } from "react-router-dom"


const StandardDeleteForm = ({ id }: { id: string | undefined }) => {
    if (!id) return null 

    const [dialog, setDialog] = useState(false)

    const [ deleteStandard ] = useDeleteStandardMutation()

    const navigate = useNavigate()

    const handleSubmit = async (e: FormEvent<HTMLFormElement>) => {
        e.preventDefault()
        try {
            await deleteStandard(parseInt(id)).unwrap()
            setDialog(false)
        } catch (error) {
            console.error(error)
        } finally {
            navigate("/standards")
        }
    }

    const content = dialog ? (
        <div className="bg-zinc-300/75 fixed inset-0 grid place-content-center">
            <div aria-live="assertive" className="p-6 bg-red-100 border border-red-800
            text-center text-red-800 rounded-sm w-fit">
                <p className="text-lg font-semibold">Are you sure you want to delete standard?</p>
                <p className="py-2 mb-4">This action can not be undone!</p>
                <div className="flex gap-6 justify-center">
                    <button className="block py-1.5 px-6 rounded-sm
                     bg-zinc-500 text-white font-semibold hover:bg-zinc-400
                      focus:bg-zinc-300" 
                      type="button" 
                      onClick={() => setDialog(false)}
                    >
                        No Cancel
                    </button>
                    <button className="block py-1.5 px-6 rounded-sm bg-red-500
                     text-white font-semibold hover:bg-red-400
                      focus:bg-red-300" 
                      type="submit"
                    >
                        Yes Delete
                    </button>
                </div>
            </div>
        </div>
    ) : null

    return (
        <form onSubmit={handleSubmit} className="mt-8 w-fit mx-auto relative">
            { content }

            <button 
                className="py-1.5 px-6 rounded-sm text-white font-semibold
                bg-red-400 hover:bg-red-300 focus:bg-red-200"
                type="button"
                onClick={() => setDialog(true)}
            >
                Delete Standard
            </button>
        </form>
    )
}

export default StandardDeleteForm