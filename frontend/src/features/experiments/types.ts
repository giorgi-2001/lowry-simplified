export interface ExperimentData {
    project_id: string
    standard_id: number
    name: string
    description: string
}

export interface Experiment extends ExperimentData {
    id: number,
    image: string | null
    csv: string | null
    created_at: string
}