import { apiSlice } from "../../app/api/apiSlice"
import { UserRegisterData, UserLoginData } from "../auth/types"


export const userApiSlice = apiSlice.injectEndpoints({
    endpoints: builder => ({
        getUser: builder.query({
            query: () => "/users/me",

            providesTags: ["User"]
        }),

        registerUser: builder.mutation({
            query: (data: UserRegisterData) => ({
                url: "/users/register",
                method: "POST",
                body: data
            })
        }),

        deleteUser: builder.mutation({
            query: () => ({
                url: "/users/",
                method: "DELETE"
            })
        }),

        updateUser: builder.mutation({
            query: (data: UserLoginData) => ({
                url: "/users/",
                method: "PATCH",
                body: data
            }),

            invalidatesTags: ["User"]
        })
    })
})


export const {
    useGetUserQuery,
    useRegisterUserMutation,
    useDeleteUserMutation,
    useUpdateUserMutation
} = userApiSlice