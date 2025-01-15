import StandardCreationForm from "./StandardCreationForm"
import StandardsList from "./StandardsList"
import { useGetStandardsQuery } from "./standardApiSlice"

const StandardsPage = () => {

  const {
      isLoading, isSuccess, data, refetch
    } = useGetStandardsQuery(undefined)

  const refetchAfterTimeout = () => {
    setTimeout(refetch, 3000)
  }

  return (
    <div className="wrapper grid grid-cols-[2fr_1fr] gap-8">
      
      <StandardsList 
        isLoading={isLoading}
        isSuccess={isSuccess}
        data={data}
      />
    
      <StandardCreationForm refetch={refetchAfterTimeout} />
    </div>
  )
}

export default StandardsPage