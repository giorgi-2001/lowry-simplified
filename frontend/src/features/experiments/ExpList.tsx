import { Link } from "react-router-dom"
import { useDeleteExperimentMutation, useGetExperimentsQuery } from "./expApiSlice"
import { formatDate } from "../standards/StandardsList"

const ExpList = ({ projectId }: { projectId: string }) => {
    const { data } = useGetExperimentsQuery(projectId)
    const [deleteExperiment] = useDeleteExperimentMutation()


    const epxerimentList = data?.ids.map(id => {
        const exp = data.entities[id]
        return (
            <div key={exp.id} className="flex gap-2">
                <Link to={`/experiments/${projectId}/${exp.id}`}
                    className="grow flex justify-between py-2 px-4 rounded-sm border border-zinc-300 bg-zinc-200 hover:bg-zinc-300 cursor-pointer" 
                >
                    <p>{exp.name}</p>
                    <p>{formatDate(exp.created_at)}</p>
                </Link>
                <button 
                    onClick={() => deleteExperiment(String(exp.id))}
                    className="py-2 px-3 rounded-sm text-white bg-rose-500 hover:bg-rose-400 focus:bg-rose-300">
                    D
                </button>
            </div>
        )
    })

    if (epxerimentList?.length) {
        return epxerimentList
    } else {
        return <p>No Experiment yet...</p>
    }
}

export default ExpList