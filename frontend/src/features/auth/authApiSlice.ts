import { apiSlice } from "../../app/api/apiSlice"
import { setCredentials } from "./authSlice"
import { UserLoginData } from "./types"


const authApiSlice = apiSlice.injectEndpoints({
    endpoints: builder => ({
        login: builder.mutation({
            query: (userLoginData: UserLoginData) => ({
                url: "/users/login",
                method: "POST",
                body: userLoginData
            }),

            onQueryStarted: async (_arg, {queryFulfilled, dispatch}) => {
                try {
                    const result = await queryFulfilled
                    const token: string = result.data["access_token"]
                    dispatch(setCredentials(token))
                } catch (error) {
                    console.log(error)
                }
            }
        }),

        refresh: builder.mutation({
            query: () => ({
                url: "/users/refresh",
                method: "get"
            }),

            onQueryStarted: async (_, {queryFulfilled, dispatch}) => {
                try {
                    const result = await queryFulfilled
                    const token: string = result.data["access_token"]
                    dispatch(setCredentials(token))
                } catch (error) {
                    console.log(error)
                }
            }
        }),

        logout: builder.mutation({
            query: () => ({
                url: "users/logout",
                method: "POST"
            })
        })
    })
})


export const {
    useLoginMutation, 
    useRefreshMutation,
    useLogoutMutation
} = authApiSlice 