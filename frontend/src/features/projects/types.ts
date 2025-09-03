export interface ProjectData {
    name: string
    description: string
}

export interface Project extends ProjectData {
    id: string
    user_id: string
    created_at: string
}
