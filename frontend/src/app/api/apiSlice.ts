import { createApi, fetchBaseQuery, BaseQueryFn, FetchArgs, FetchBaseQueryError } from "@reduxjs/toolkit/query/react"
import { RootState } from "../store"
import { setCredentials, logout } from "../../features/auth/authSlice"


const baseQuery: BaseQueryFn<
    string | FetchArgs,
    unknown,
    FetchBaseQueryError
> = fetchBaseQuery({
    baseUrl: 'http://localhost:8000/api/v1',
    credentials: 'include',

    prepareHeaders: (headers: Headers, { getState }) => {
        const myState = getState() as RootState
        const token = myState.auth.token

        if (token) {
            headers.set('Authorization', `Bearer ${token}`)
        }
        return headers
    }
})


const baseQueryWithReauth: BaseQueryFn<
    string | FetchArgs,
    unknown,
    FetchBaseQueryError
> = async (
    args, api, extraOptions
) => {
        let result = await baseQuery(args, api, extraOptions)

        const error = result.error

        if (error && 'originalStatus' in error && error.originalStatus === 401) {

            const refreshResult = await baseQuery("/users/refresh", api, extraOptions)

            if (refreshResult.data) {
                const data: any = refreshResult.data
                api.dispatch(setCredentials(data.access_token))
                result = await baseQuery(args, api, extraOptions)
            } else {
                api.dispatch(logout())
            }
        }
        return result
    }


export const apiSlice = createApi({
    reducerPath: 'api',
    baseQuery: baseQueryWithReauth,
    endpoints: () => ({}),
    tagTypes: ['Standard']
})