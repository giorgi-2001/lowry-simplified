import { apiSlice } from "../../app/api/apiSlice"
import { createEntityAdapter } from "@reduxjs/toolkit"
import { Standard, StandardData } from "./types"


const standardAdapter = createEntityAdapter({
    selectId: (standard: Standard) => standard.id
})


const initialState = standardAdapter.getInitialState()


type InitType = typeof initialState


export const standardApiSlice = apiSlice.injectEndpoints({
    endpoints: builder => ({
        getStandards: builder.query({
            query: () => "/standards/my-standards",

            transformResponse: (response: Standard[]) => {
                return standardAdapter.setAll(initialState, response)
            },

            providesTags: (res: InitType | undefined) => res ?
            [
                { type: "Standard", id: "LIST" },
                ...res.ids.map((id: number )=> ({ type: "Standard" as const , id }))
            ] : [
                { type: "Standard", id: "LIST" }
            ]
        }),

        createStandard: builder.mutation({
            query: (data: StandardData) => {
                const formData = new FormData()
                formData.append("name", data.name)
                formData.append("description", data.description)
                formData.append("file", data.file)

                return {
                    url: "/standards/",
                    method: "POST",
                    body: formData
                }
            }
        }),

        deleteStandard: builder.mutation({
            query: (id: number) => ({
                url: `/standards/${id}`,
                method: "DELETE",
            }),

            invalidatesTags: (_res, _err, id) => [{ type: "Standard", id }]
        })
    })
})


export const {
    useGetStandardsQuery,
    useCreateStandardMutation,
    useDeleteStandardMutation
} = standardApiSlice