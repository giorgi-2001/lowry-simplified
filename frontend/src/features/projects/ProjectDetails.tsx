import { useParams } from "react-router-dom"
import { useGetProjectsQuery } from "./projectApiSlice"

const ProjectDetails = ({}) => {
    const { projectId } = useParams()
    const { data } = useGetProjectsQuery(undefined)
    console.log(projectId)
    const project = data?.entities[String(projectId)]

    if (!project) {
        console.log("No project was found")
        return null
    }


  return (
    (
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