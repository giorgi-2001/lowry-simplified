import { useParams } from "react-router-dom"
import { useGetExperimentsQuery } from "./expApiSlice"
import { formatDate } from "../standards/StandardsList"

const ExpDetails = () => {
    const { projectId, experimentId } = useParams() as Record<string, string>
    const { data, refetch } = useGetExperimentsQuery(String(projectId))
    const exp = data?.entities[parseInt(experimentId)]

    if (!exp) return null

    return (
        <>
        <section className="w-full max-w-3xl mx-auto my-6 p-6 rounded-2xl bg-white shadow-md">
            <div className="flex items-center gap-2 mb-4">
                <h2 className="text-2xl justify-between font-semibold text-gray-800">
                    {exp.name}
                </h2>
                <button onClick={refetch} className="ml-auto font-semibold text-zinc-700 hover:text-zinc-500">
                    Refresh
                </button>
            </div>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                <div>
                    <p className="text-sm font-medium text-gray-500 uppercase">DESCRIPTION:</p>
                    <p className="text-gray-700">
                        {exp.description}
                    </p>
                </div>
                <div>
                    <p className="text-sm font-medium text-gray-500 uppercase">
                        CREATED AT:
                    </p>
                    <p className="text-gray-700">{formatDate(exp.created_at)}</p>
                </div>
            </div>
            
        </section>
        { exp?.image && exp?.csv &&
            <div className="w-full max-w-3xl mx-auto py-6">
                <img src={exp?.image} alt="experiment plot" />
                <a className="mt-6 cursor-pointer block rounded-sm py-2 text-center text-lg text-white bg-indigo-500 hover:bg-indigo-400 focus:bg-indigo-300"
                download={true} href={exp?.csv} target="_blank">
                    Download CSV
                </a>
            </div>
        }
        
        </>
    )
}

export default ExpDetails