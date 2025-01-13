import { useGetStandardsQuery } from "./standardApiSlice"
import { useParams } from "react-router-dom"
import { ReactNode } from "react"
import StandardDeleteForm from "./StandardDeleteForm"


const StandardDetails = () => {

    const { id } = useParams()

    const {
        isLoading, isSuccess, data,
    } = useGetStandardsQuery(undefined)

    let content: ReactNode 
    
    if (isLoading) {
        content = <p>Loaing...</p>
    } else if (isSuccess && typeof id == "string") {
        const standard = data.entities[parseInt(id)]
        const equetion = `y = ${standard.slope.toFixed(2)}x 
            + ${standard.y_intercept.toFixed(4)}`
        
        content = (
            <>
                <p className="text-center text-xl mb-4 text-zinc-700 font-semibold">
                    Correlation: {standard.correlation.toFixed(6)}
                </p>
                <p className="text-center text-4xl mb-12 text-indigo-700 font-bold">
                    {equetion}
                </p>
                <img 
                    className="w-[80%] mx-auto" 
                    src={standard.image} alt="plot" 
                />
            </>
        )
    }

  return (
    <section className="wrapper">
        { content }
        <StandardDeleteForm id={id} />
    </section>
  )
}

export default StandardDetails