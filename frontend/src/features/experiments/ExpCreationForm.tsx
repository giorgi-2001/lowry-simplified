import { ChangeEvent, FormEvent, useState } from "react"
import { useGetStandardsQuery } from "../standards/standardApiSlice"
import { useNavigate, useParams } from "react-router-dom"
import { useCreateExperimentMutation } from "./expApiSlice"

const ExpCreationForm = () => {
  const [name, setName] = useState("")
  const [description, setDescription] = useState("")
  const [standardId, setStandardId] = useState("")
  const [file, setFile] = useState<File | null>(null)
  const [error, setError] = useState("")

  const { projectId } = useParams()
  const navigate = useNavigate()

  const { data } = useGetStandardsQuery(undefined)
  const [createExperiment] = useCreateExperimentMutation()

  const canNotSubmit = ![name, description, standardId, file].every(Boolean)

  const handleFile = (e: ChangeEvent<HTMLInputElement>) => {
    if (e.target?.files) {
      setFile(e.target.files[0])
    }
  }

  const createExperimentData = (file: File) => {
    const formData = new FormData()
    formData.append("project_id", String(projectId))
    formData.append("standard_id", standardId)
    formData.append("name", name)
    formData.append("description", description)
    formData.append("file", file)
    return formData
  }

  const handleSubmit = async (e: FormEvent<HTMLFormElement>) => {
    e.preventDefault()
    if (canNotSubmit) return
    if (!file) return
    const data = createExperimentData(file)
    try {
      await createExperiment(data).unwrap()
      setName("")
      setDescription("")
      navigate(`/projects/${projectId}`)
    } catch (error) {
      setError(JSON.stringify(error))
    }
  }

  const standardOptions = data?.ids.map(id => {
    const std = data.entities[id]
    return (
      <option key={std.id} value={std.id}>{std.name}</option>
    )
  })

    
  return (
    <section className="w-fit max-w-3xl mx-auto bg-zinc-200 p-6 rounded-sm border border-zinc-300">
      <h2 className="text-xl font-semibold text-zinc-700 mb-8">Enter your experiment details and upload file:</h2>
      <form onSubmit={handleSubmit}>
        <div className="mb-6">
          <label className="block mb-1 font-semibold text-zinc-700" htmlFor="name">
            Experiment Name:
          </label>
          <input
            className="py-1 px-2 w-full border border-zinc-300 rounded-sm"
            type="text"
            id="name"
            value={name}
            onChange={e => setName(e.target.value)}
          />
        </div>
        <div className="mb-6">
          <label className="block mb-1 font-semibold text-zinc-700" htmlFor="description">
            Description:
          </label>
          <input
            className="py-1 px-2 w-full border border-zinc-300 rounded-sm"
            type="text"
            id="description"
            value={description}
            onChange={e => setDescription(e.target.value)}
          />
        </div>

        <div className="mb-6">
          <label className="block mb-1 font-semibold text-zinc-700" htmlFor="standard">
            Standard:
          </label>
          <select
            className="py-1 px-2 w-full border border-zinc-300 rounded-sm"
            id="standard"
            onChange={e => setStandardId(e.target.value)}
          >
            <option hidden></option>
            { standardOptions }
          </select>
        </div>

        <div className="mb-6">
          <label className="block mb-1 font-semibold text-zinc-700" htmlFor="file">
            Experiment Data (CSV):
          </label>
          <input
            className="py-1 px-2 w-full border bg-white border-zinc-300 rounded-sm"
            type="file"
            id="file"
            accept="text/csv"
            multiple={false}
            onChange={handleFile}
          /> 
        </div>

        <button
          disabled={canNotSubmit}
          className="text-white py-1 px-4 rounded-sm bg-indigo-500 hover:bg-indigo-400 focus:bg-idnigo-300 disabled:cursor-not-allowed disabled:bg-indigo-500 disabled:opacity-40"
        >
          Create
        </button>
        
      </form>
      { error && <p className="p-4">{error}</p>}
    </section>
  )
}

export default ExpCreationForm