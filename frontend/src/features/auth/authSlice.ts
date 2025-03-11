import { createSlice } from "@reduxjs/toolkit"
import { RootState } from "../../app/store"


type AuthStateType = {
    token: string
}

const initialState: AuthStateType = {
    token: ''
}

const authSlice = createSlice({
    name: 'auth',
    initialState,
    reducers: {
        setCredentials: (state, action) => {
            state.token = action.payload
        },

        logout: (state) => {
            state.token = ''
        },
    }
})


export const { setCredentials, logout } = authSlice.actions

export default authSlice.reducer

export const selectToken = (state: RootState) => state.auth.token 