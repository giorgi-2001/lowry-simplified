import { Link, useParams } from "react-router-dom"
import { useGetProjectsQuery } from "./projectApiSlice"
import DeleteProjectModal from "./DeleteProjectModal"
import ExpList from "../experiments/ExpList"
import { formatDate } from "../standards/StandardsList"
import { useParams } from "react-router-dom"
import { useGetProjectsQuery } from "./projectApiSlice"


const ProjectDetails = ({}) => {
    const { projectId } = useParams()
    const { data } = useGetProjectsQuery(undefined)
    const project = data?.entities[String(projectId)]

    if (!project) {
        console.log("No project was found")
        return null
    }


  return (
    (
      <>
      <section className="w-full max-w-3xl mx-auto mt-6 p-6 rounded-2xl bg-white shadow-md">
        <div className="flex items-center gap-2 mb-4">
          <h2 className="text-2xl justify-between font-semibold text-gray-800">
            {project.name}
          </h2>
          <DeleteProjectModal projectId={String(projectId)} />
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
        <ExpList projectId={String(projectId)} />
      </section>
      </>
    <section className="w-full max-w-3xl mx-auto my-6 p-6 rounded-2xl bg-white shadow-md">
      <h2 className="text-2xl font-semibold text-gray-800 mb-4">
        Project Metadata:
      </h2>
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <div>
          <p className="text-sm font-medium text-gray-500 uppercase">Name</p>
          <p className="text-lg font-semibold text-gray-900">
            {project.name}
          </p>
        </div>

        <div>
          <p className="text-sm font-medium text-gray-500 uppercase">
            Description
          </p>
          <p className="text-gray-700">{project.description}</p>
        </div>
      </div>
    </section>
  )
  )
}

export default ProjectDetails