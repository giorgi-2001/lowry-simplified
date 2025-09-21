import { useState } from "react"
import { useDeleteProjectMutation } from "./projectApiSlice"
import { useNavigate } from "react-router-dom"

const DeleteProjectModal = ({ projectId }: { projectId: string}) => {
    const [modalOpen, setModalOpen] = useState(false)
    const navigate = useNavigate()
    const [deleteProject] = useDeleteProjectMutation()

    const handleDelete = async () => {
        try {
            await deleteProject(projectId).unwrap()
            navigate("/")
        } catch (error) {
            console.log(error)
        }
    }

    const modal = (
        <div className="fixed bg-black/70 inset-0 grid place-content-center">
            <div className="bg-white p-6 rounded-sm max-w-[450px]">
                <h2 className="text-3xl text-zinc-600 font-bold">Are you sure you want to delete the project?</h2>
                <p className="py-6">
                    This action will permanently remove the project and all assosoated Experiments. If you proceed with this action you won't be able to undo it.
                </p>
                <div className="flex items-center justify-end gap-4 pt-4 border-t border-zinc-300">
                    <button
                    className="px-4 py-2 bg-zinc-500 hover:bg-zinc-400 focus:bg-zinc-300 rounded-sm text-white text-inherit"
                    onClick={() => setModalOpen(false)}>
                        Cancel
                    </button>
                    <button
                    onClick={handleDelete}
                    className="px-4 py-2 bg-rose-500 hover:bg-rose-400 focus:bg-rose-300 rounded-sm text-white text-inherit"
                    >
                        Delete
                    </button>
                </div>
            </div>
        </div>
    )

  return (
    <>
        <button
        className="ml-auto bg-zinc-200 px-4 py-1 border border-zinc-400 rounded-sm"
        onClick={() => setModalOpen(true)}>
            Delete
        </button>
        { modalOpen && modal }
    </>
  )
}

export default DeleteProjectModal