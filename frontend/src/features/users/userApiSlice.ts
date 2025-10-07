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
        }),

        requestPasswordReset: builder.mutation({
            query: (data: { email: string }) => ({
                url: "/users/password-reset",
                method: "POST",
                body: data
            }),

            invalidatesTags: ["User"]
        }),

        passwordResetConfirm: builder.mutation({
            query: (data: { token: string, password: string }) => ({
                url: "/users/password-reset-confirm",
                method: "POST",
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
    useUpdateUserMutation,
    useRequestPasswordResetMutation,
    usePasswordResetConfirmMutation
} = userApiSlice