export interface Message {
  id: string
  role: 'user' | 'assistant'
  content: string
  timestamp: Date
}

export interface ChatResponse {
  message: string
  actions_performed?: string[]
}

export interface ChatRequest {
  text: string
}
