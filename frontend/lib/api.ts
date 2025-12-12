import type {
  User,
  AuthResponse,
  LoginRequest,
  RegisterRequest
} from '@/types/user'
import type {
  Task,
  TaskCreate,
  TaskUpdate,
  TasksResponse
} from '@/types/task'

const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'

class ApiClient {
  private getAuthHeader(): HeadersInit {
    const token = localStorage.getItem('token')
    if (!token) {
      return {}
    }
    return {
      'Authorization': `Bearer ${token}`
    }
  }

  private async request<T>(
    endpoint: string,
    options: RequestInit = {}
  ): Promise<T> {
    const url = `${API_URL}${endpoint}`

    const response = await fetch(url, {
      ...options,
      headers: {
        'Content-Type': 'application/json',
        ...this.getAuthHeader(),
        ...options.headers,
      },
    })

    if (!response.ok) {
      const error = await response.json().catch(() => ({
        detail: 'An error occurred'
      }))
      throw new Error(error.detail || `HTTP ${response.status}`)
    }

    // Handle 204 No Content (empty response)
    if (response.status === 204) {
      return undefined as T
    }

    return response.json()
  }

  // Auth endpoints
  async register(data: RegisterRequest): Promise<AuthResponse> {
    const response = await this.request<AuthResponse>('/api/auth/register', {
      method: 'POST',
      body: JSON.stringify(data),
    })

    // Store token and user
    localStorage.setItem('token', response.token)
    localStorage.setItem('user', JSON.stringify(response.user))

    return response
  }

  async login(data: LoginRequest): Promise<AuthResponse> {
    const response = await this.request<AuthResponse>('/api/auth/login', {
      method: 'POST',
      body: JSON.stringify(data),
    })

    // Store token and user
    localStorage.setItem('token', response.token)
    localStorage.setItem('user', JSON.stringify(response.user))

    return response
  }

  logout(): void {
    localStorage.removeItem('token')
    localStorage.removeItem('user')
  }

  // Task endpoints
  async getTasks(userId: string): Promise<TasksResponse> {
    return this.request<TasksResponse>(`/api/${userId}/tasks/`)
  }

  async getTask(userId: string, taskId: number): Promise<Task> {
    return this.request<Task>(`/api/${userId}/tasks/${taskId}`)
  }

  async createTask(userId: string, data: TaskCreate): Promise<Task> {
    return this.request<Task>(`/api/${userId}/tasks/`, {
      method: 'POST',
      body: JSON.stringify(data),
    })
  }

  async updateTask(
    userId: string,
    taskId: number,
    data: TaskUpdate
  ): Promise<Task> {
    return this.request<Task>(`/api/${userId}/tasks/${taskId}`, {
      method: 'PUT',
      body: JSON.stringify(data),
    })
  }

  async toggleComplete(userId: string, taskId: number): Promise<Task> {
    return this.request<Task>(
      `/api/${userId}/tasks/${taskId}/complete`,
      {
        method: 'PATCH',
      }
    )
  }

  async deleteTask(userId: string, taskId: number): Promise<void> {
    await this.request<void>(`/api/${userId}/tasks/${taskId}`, {
      method: 'DELETE',
    })
  }
}

export const api = new ApiClient()
