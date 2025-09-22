import { useState } from "react"
import { Link, useParams } from "react-router-dom"
import { useGetProjectsQuery } from "./projectApiSlice"
import DeleteProjectModal from "./DeleteProjectModal"
import ExpList from "../experiments/ExpList"
import { formatDate } from "../standards/StandardsList"


const ProjectDetails = ({}) => {
    const { projectId } = useParams()
    const { data } = useGetProjectsQuery(undefined)
    const project = data?.entities[String(projectId)]

    const [modalOpen, setModalOpen] = useState(false)
    const [errorMessage, setErrorMessage] = useState("")

    if (!project) {
        console.log("No project was found")
        return null
    }

  return (
    (
      <>
      { errorMessage &&
        <p aria-live="assertive" className="w-full max-w-3xl mx-auto my-6 p-4 text-center font-semibold text-rose-700 border-2 border-rose-700 bg-rose-200 rounded-sm">
          {errorMessage}
        </p>
      }
      <section className="w-full max-w-3xl mx-auto mt-6 p-6 rounded-2xl bg-white shadow-md">
        <div className="flex items-center gap-2 mb-4">
          <h2 className="text-2xl justify-between font-semibold text-gray-800">
            {project.name}
          </h2>
          <DeleteProjectModal
            projectId={String(projectId)}
            modalOpen={modalOpen}
            setModalOpen={setModalOpen}
            setErrorMessage={setErrorMessage}
          />
        </div>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div>
            <p className="text-sm font-medium text-gray-500 uppercase">DESCRIPTION:</p>
            <p className="text-gray-700">
              {project.description}
            </p>
          </div>

          <div>
            <p className="text-sm font-medium text-gray-500 uppercase">
              CREATED AT:
            </p>
            <p className="text-gray-700">{formatDate(project.created_at)}</p>
          </div>
        </div>
      </section>
      <section className="w-full max-w-3xl mx-auto my-4 flex flex-col gap-2">
        <Link 
          className="block text-center py-2 mb-4 rounded-sm text-white text-lg bg-indigo-500 hover:bg-indigo-400 focus:bg-indigo-300 cursor-pointer"
          to={`/experiments/create/${String(projectId)}`}
        >
          Create new experiment
        </Link>
        <ExpList
          projectId={String(projectId)}
        />
      </section>
      </>
  )
  )
}

export default ProjectDetails