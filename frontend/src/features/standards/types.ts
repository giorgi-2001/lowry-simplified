export interface Standard {
    id: number
    name: string
    description: string
    image: string
    correlation: number
    slope: number
    y_intercept: number
    created_at: string
    updated_at: string
}


export interface StandardData {
    "name": string
    "description": string
    "file": File
}