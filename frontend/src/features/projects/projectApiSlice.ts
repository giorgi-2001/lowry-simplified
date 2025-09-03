import { apiSlice } from "../../app/api/apiSlice"
import { createEntityAdapter } from "@reduxjs/toolkit"
import { Project, ProjectData } from "./types"


const projectAdapter = createEntityAdapter({
    selectId: (project: Project) => project.id
})


const initialState = projectAdapter.getInitialState()


type InitType = typeof initialState


export const projectApiSlice = apiSlice.injectEndpoints({
    endpoints: builder => ({
        getProjects: builder.query({
            query: () => "/projects/",

            transformResponse: (response: Project[]) => {
                return projectAdapter.setAll(initialState, response)
            },

            providesTags: (res: InitType | undefined) => res ?
            [
                { type: "Project", id: "LIST" },
                ...res.ids.map((id: string )=> ({ type: "Project" as const , id }))
            ] : [
                { type: "Project", id: "LIST" }
            ]
        }),

        createProject: builder.mutation({
            query: (data: ProjectData) => ({
                url: "/projects/",
                method: "POST",
                body: data
            }),
            
            invalidatesTags: (_res, _err) => [{ type: "Project", id: "LIST" }]
        }),

        deleteProject: builder.mutation({
            query: (id: number) => ({
                url: `/projects/${id}`,
                method: "DELETE",
            }),

            invalidatesTags: (_res, _err, id) => [{ type: "Project", id }]
        })
    })
})


export const {
    useGetProjectsQuery,
    useCreateProjectMutation,
    useDeleteProjectMutation
} = projectApiSlice