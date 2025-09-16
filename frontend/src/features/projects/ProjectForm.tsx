import { FormEvent, useState } from "react"
import { useCreateProjectMutation } from "./projectApiSlice"

const ProjectForm = () => {
    const [showForm, setShowForm] = useState(false)
    const [name, setName] = useState("")
    const [description, setDescription] = useState("")

    const [createProject] = useCreateProjectMutation()

    const handleSubmit = async (e: FormEvent<HTMLFormElement>) => {
        e.preventDefault()
        const projData = { name, description }
        try {
            await createProject(projData).unwrap()
            setShowForm(false)
        } catch (error) {
            console.log(error)
        }
    }

    const button = (
        <button onClick={() => setShowForm(true)} className="text-xl font-semibold text-white py-3 px-8 bg-indigo-400 border border-indigo-400 rounded-sm hover:bg-indigo-100 hover:text-indigo-700 transition-all duration-300">
            Create New Project
        </button>
    )

    const form = (
        <div className="fixed inset-0 bg-black/70 grid place-content-center">
            <form onSubmit={handleSubmit} className="w-fit min-w-96 sm:min-w-[450px] p-6 bg-white rounded-sm">
                <div className="flex gap-x-4 justify-between mb-4 pb-4 border-b border-zinc-300">
                    <h2 className="text-xl">Create New Project</h2>
                    <button onClick={() => setShowForm(false)} type="button" className="">
                        <span className="text-zinc-800">✖</span>
                    </button>
                </div>
                
                <div className="mb-4">
                    <label className="block mb-1 text-zinc-800 pl-1" htmlFor="project-name">Project Name:</label>
                    <input
                        required
                        className="block w-full px-3 py-2 border border-zinc-300 rounded-sm"
                        id="project-name"
                        type="text"
                        value={name}
                        onChange={e => setName(e.target.value)}
                    />
                </div>
                <div className="mb-4">
                    <label className="block mb-1 text-zinc-800 pl-1" htmlFor="project-description">Project Description:</label>
                    <input
                        required
                        className="block w-full px-3 py-2 border border-zinc-300 rounded-sm"
                        id="project-description"
                        type="text"
                        value={description}
                        onChange={e => setDescription(e.target.value)}
                    />
                </div>

                <div className="pt-4 mt-8 border-t border-zinc-300 flex gap-4 justify-end">
                    <button className="block px-4 py-2 rounded-sm bg-indigo-500 text-white hover:bg-indigo-400 focus:bg-indigo-300">
                        Add Project
                    </button>
                    <button onClick={() => setShowForm(false)} type="button" className="block px-4 py-2 rounded-sm bg-zinc-500 text-white hover:bg-zinc-400 focus:bg-zinc-300">
                        Cancel
                    </button>
                </div>
            </form>
        </div>
        
    )

    return <>
        {button}
        {showForm && form}
    </>
}

export default ProjectForm