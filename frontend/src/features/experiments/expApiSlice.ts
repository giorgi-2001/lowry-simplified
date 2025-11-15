import { apiSlice } from "../../app/api/apiSlice"
import { createEntityAdapter } from "@reduxjs/toolkit"
import { Experiment } from "./types"


const experimentAdapter = createEntityAdapter({
    selectId: (experiment: Experiment) => experiment.id
})


const initialState = experimentAdapter.getInitialState()


type InitType = typeof initialState


export const experimentApiSlice = apiSlice.injectEndpoints({
    endpoints: builder => ({
        getExperiments: builder.query({
            query: (projectId: string) => `/experiments/?project_id=${projectId}`,

            transformResponse: (response: Experiment[]) => {
                return experimentAdapter.setAll(initialState, response)
            },

            providesTags: (res: InitType | undefined) => res ?
            [
                { type: "Experiment", id: "LIST" },
                ...res.ids.map((id: number )=> ({ type: "Experiment" as const , id }))
            ] : [
                { type: "Experiment", id: "LIST" }
            ]
        }),

        createExperiment: builder.mutation({
            query: (data: FormData) => ({
                url: "/experiments/",
                method: "POST",
                body: data
            }),
            
            invalidatesTags: (_res, _err) => [{ type: "Experiment", id: "LIST" }]
        }),

        deleteExperiment: builder.mutation({
            query: (id: string) => ({
                url: `/experiments/${id}`,
                method: "DELETE",
            }),

            invalidatesTags: (_res, _err, id) => [{ type: "Experiment", id }]
        })
    })
})


export const {
    useGetExperimentsQuery,
    useCreateExperimentMutation,
    useDeleteExperimentMutation
} = experimentApiSlice