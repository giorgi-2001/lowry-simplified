import { useCreateStandardMutation } from "./standardApiSlice"
import { ChangeEvent, FormEvent, useRef, useState } from "react"


type StandardCreationFormPropsType = {
    refetch: () => void
}


const StandardCreationForm = (
    { refetch }: StandardCreationFormPropsType
) => {
    const [name, setName] = useState("")
    const [description, setDescription] = useState("")
    const [file, setFile] = useState<File | null>(null)
    const fileRef = useRef<HTMLInputElement>(null)

    const [error, setError] = useState("")

    const [ createStandard ] = useCreateStandardMutation()

    const canNotSubmit = (
        !description || !name || !file || !fileRef.current
    )

    const handleFileChange = (e: ChangeEvent<HTMLInputElement>) => {
        if (!e.target.files || !fileRef.current?.files) return 
        const file = e.target.files[0]
        setFile(file)
        console.log(file.name)
    }

    const handleSubmit = async (e: FormEvent<HTMLFormElement>) => {
        e.preventDefault()

        if (canNotSubmit) {
            setError("All fields are required!")
            return
        }

        if (name.length < 2 || description.length < 2) {
            setError("Name and description should be at least 2 characters long!")
            return
        }

        setError("")

        const data = { name, description, file }

        try {
            await createStandard(data).unwrap()
            setName("")
            setDescription("")
            fileRef.current.value = ""
            refetch()
        } catch (error: any) {
            setError(JSON.stringify(error.data.detail))
        }
    }


    return (
        <section>
            <form onSubmit={handleSubmit}>
                <div className="mb-6">
                    <label className="block mb-2" htmlFor="name">
                        Name
                    </label>
                    <input 
                        className="block w-full border border-zinc-300 py-1.5 px-2 rounded-sm"
                        id="name"
                        type="text"
                        placeholder="Enter standard name"
                        value={name}
                        onChange={(e) => setName(e.target.value)}
                    />
                </div>
                <div className="mb-6">
                    <label className="block mb-2" htmlFor="description">
                        Description
                    </label>
                    <input 
                        className="block w-full border border-zinc-300 py-1.5 px-2 rounded-sm"
                        id="description"
                        type="text"
                        placeholder="Enter description"
                        value={description}
                        onChange={(e) => setDescription(e.target.value)}
                    />
                </div>
                <div className="mb-6">
                    <label className={"block mb-2"} htmlFor="description">
                        Upload csv file
                    </label>
                    <input 
                        className="block border border-zinc-300 py-1.5 px-2 rounded-sm"
                        id="description"
                        type="file"
                        accept="text/csv"
                        multiple={false}
                        ref={fileRef}
                        onChange={handleFileChange}
                    />
                </div>
                <button 
                    disabled={canNotSubmit}
                    className="block px-6 py-1.5 rounded-sm
                 text-white font-bold bg-indigo-400 hover:bg-indigo-300 
                 focus:bg-indigo-200 disabled:bg-indigo-400 
                 disabled:opacity-50 disabled:cursor-not-allowed"
                >
                    Upload
                </button>
            </form>

            { error && 
                <p aria-live="assertive" className="py-1.5 px-4 mt-8
                 text-red-800 border border-red-800 bg-red-200 
                 text-center rounded-sm">
                    Error: {error}
                </p> 
            }

        </section>
  )
}

export default StandardCreationForm