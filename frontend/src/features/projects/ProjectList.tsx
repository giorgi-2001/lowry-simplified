import { useState } from "react"
import ProjectForm from "./ProjectForm"
import { useGetProjectsQuery } from "./projectApiSlice"
import { formatDate } from "../standards/StandardsList"
import { useNavigate } from "react-router-dom"


const ProjectList = () => {
    const [customError, setCustomError] = useState("")
    const { data, isError, error, isLoading } = useGetProjectsQuery(undefined)
    const navigate = useNavigate()

    let content

    if (isLoading) {
        content = <p>Loading...</p>
    } else if (isError) {
        setCustomError(JSON.stringify(error))
    } else if (data) {
        const { ids, entities: projects } = data
        content = ids.map(id => {
            const proj = projects[id]
            return (
                <article onClick={() => navigate(`/projects/${id}`)} className="cursor-pointer p-5 bg-zinc-100 border border-zinc-200 rounded-sm hover:bg-zinc-200 focus:bg-zinc-300" key={id}>
                    <h3 className="text-lg font-semibold">{proj.name}</h3>
                    <p className="py-2">{proj.description}</p>
                    <p className="text-sm text-zinc-700">{formatDate(proj.created_at)}</p>
                </article>
            )
        })
    }


    return (
        <main className="wrapper grid grid-flex gap-8">
            <ProjectForm />
            {content}
            {customError}
        </main>
    )
}

export default ProjectList