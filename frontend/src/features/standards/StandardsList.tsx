import { ReactNode } from "react"
import { EntityState } from "@reduxjs/toolkit"
import { Standard } from "./types"
import { Link } from "react-router-dom"
import { format } from "date-fns"


export const formatDate = (isoString: string): string => {
  const date = new Date(isoString)
  return format(date, "MMMM dd, yyyy")
}


type StandardsListPropType = {
  isLoading: boolean
  isSuccess: boolean
  data: EntityState<Standard, number> | undefined
}


const StandardsList = (
  { isLoading, isSuccess, data }: StandardsListPropType
) => {

  let content: ReactNode 

  if (isLoading) {
    content = <p>Loaing...</p>
  } else if (isSuccess && data?.ids.length) {
    const { ids, entities } = data

    content = ids.map(id => {
      const standard = entities[id]

      return (
        <div 
          className="mb-4 p-6 rounded-sm bg-zinc-100 border border-zinc-200"
          key={id}
        >
          <h2 className="text-2xl font-bold mb-3">
            {standard.name}
          </h2>
          <p>{standard.description}</p>
          <div className="flex justify-between items-baseline mt-3">
            <Link 
              className="font-semibold text-indigo-800 hover:underline"
              to={`/standards/${standard.id}`}
            >
              View full standard
            </Link>
            <p className="text-sm">{formatDate(standard.created_at)}</p>
          </div>
        </div>
      )
    })
  } else if (isSuccess && !data?.ids.length) {
    content = <p>No Standards Yet...</p>
  }

  return (
    <section className="max-h-[70vh] pr-8 overflow-y-scroll">
      { content }
    </section>
  )
}

export default StandardsList