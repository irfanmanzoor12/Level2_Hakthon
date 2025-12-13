export interface Task {
  id: number
  user_id: string
  title: string
  description: string | null
  completed: boolean
  due_date: string | null
  tags: string[]
  created_at: string
  updated_at: string
}

export interface TaskCreate {
  title: string
  description?: string
  due_date?: string | null
  tags?: string[]
}

export interface TaskUpdate {
  title?: string
  description?: string
  completed?: boolean
  due_date?: string | null
  tags?: string[]
}

export interface TasksResponse {
  tasks: Task[]
  total: number
  limit: number
  offset: number
}
