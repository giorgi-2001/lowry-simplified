export interface UserLoginData {
    username: string
    password: string
}

export interface UserRegisterData extends UserLoginData {
    email: string
}


export interface UserResponse {
    id: number
    username: string
    email: string
    created_at: string
    updated_at: string
}