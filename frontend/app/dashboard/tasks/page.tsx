'use client'

import { useState, useEffect } from 'react'
import { api } from '@/lib/api'
import type { Task, TaskCreate } from '@/types/task'
import type { User } from '@/types/user'

export default function TasksPage() {
  const [tasks, setTasks] = useState<Task[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')
  const [user, setUser] = useState<User | null>(null)

  // New task form
  const [showForm, setShowForm] = useState(false)
  const [newTitle, setNewTitle] = useState('')
  const [newDescription, setNewDescription] = useState('')

  // Edit task
  const [editingTask, setEditingTask] = useState<Task | null>(null)
  const [editTitle, setEditTitle] = useState('')
  const [editDescription, setEditDescription] = useState('')

  useEffect(() => {
    const userStr = localStorage.getItem('user')
    if (userStr) {
      const userData = JSON.parse(userStr)
      setUser(userData)
      loadTasks(userData.id)
    }
  }, [])

  // Listen for task updates from chat widget
  useEffect(() => {
    const handleTaskUpdate = () => {
      if (user) {
        loadTasks(user.id)
      }
    }
    window.addEventListener('taskUpdated', handleTaskUpdate)
    return () => window.removeEventListener('taskUpdated', handleTaskUpdate)
  }, [user])

  const loadTasks = async (userId: string) => {
    try {
      const response = await api.getTasks(userId)
      setTasks(response.tasks)
    } catch (err) {
      setError('Failed to load tasks')
    } finally {
      setLoading(false)
    }
  }

  const handleCreateTask = async (e: React.FormEvent) => {
    e.preventDefault()
    if (!user) return

    try {
      const newTask = await api.createTask(user.id, {
        title: newTitle,
        description: newDescription,
      })
      setTasks([newTask, ...tasks])
      setNewTitle('')
      setNewDescription('')
      setShowForm(false)
    } catch (err) {
      setError('Failed to create task')
    }
  }

  const handleToggleComplete = async (task: Task) => {
    if (!user) return

    try {
      const updated = await api.toggleComplete(user.id, task.id)
      setTasks(tasks.map((t) => (t.id === task.id ? updated : t)))
    } catch (err) {
      setError('Failed to update task')
    }
  }

  const handleDeleteTask = async (taskId: number) => {
    if (!user) return

    try {
      await api.deleteTask(user.id, taskId)
      setTasks(tasks.filter((t) => t.id !== taskId))
    } catch (err) {
      setError('Failed to delete task')
    }
  }

  const startEdit = (task: Task) => {
    setEditingTask(task)
    setEditTitle(task.title)
    setEditDescription(task.description || '')
  }

  const handleUpdateTask = async (e: React.FormEvent) => {
    e.preventDefault()
    if (!user || !editingTask) return

    try {
      const updated = await api.updateTask(user.id, editingTask.id, {
        title: editTitle,
        description: editDescription,
      })
      setTasks(tasks.map((t) => (t.id === editingTask.id ? updated : t)))
      setEditingTask(null)
    } catch (err) {
      setError('Failed to update task')
    }
  }

  if (loading) {
    return (
      <div className="flex items-center justify-center">
        <p className="text-lg text-gray-600">Loading tasks...</p>
      </div>
    )
  }

  return (
    <div>
      <div className="mb-8 flex items-center justify-between">
        <h1 className="text-3xl font-bold text-gray-900">My Tasks</h1>
        <button
          onClick={() => setShowForm(!showForm)}
          className="rounded-md bg-indigo-600 px-4 py-2 text-sm font-semibold text-white hover:bg-indigo-500"
        >
          {showForm ? 'Cancel' : 'Add Task'}
        </button>
      </div>

      {error && (
        <div className="mb-4 rounded-md bg-red-50 p-4">
          <p className="text-sm text-red-800">{error}</p>
        </div>
      )}

      {showForm && (
        <form onSubmit={handleCreateTask} className="mb-8 rounded-lg bg-white p-6 shadow">
          <h2 className="mb-4 text-xl font-semibold text-gray-900">New Task</h2>
          <div className="space-y-4">
            <div>
              <label htmlFor="title" className="block text-sm font-medium text-gray-700">
                Title *
              </label>
              <input
                id="title"
                type="text"
                required
                maxLength={200}
                className="mt-1 block w-full rounded-md border-0 px-3 py-2 text-gray-900 ring-1 ring-inset ring-gray-300 focus:ring-2 focus:ring-indigo-600"
                value={newTitle}
                onChange={(e) => setNewTitle(e.target.value)}
              />
            </div>
            <div>
              <label htmlFor="description" className="block text-sm font-medium text-gray-700">
                Description
              </label>
              <textarea
                id="description"
                rows={3}
                className="mt-1 block w-full rounded-md border-0 px-3 py-2 text-gray-900 ring-1 ring-inset ring-gray-300 focus:ring-2 focus:ring-indigo-600"
                value={newDescription}
                onChange={(e) => setNewDescription(e.target.value)}
              />
            </div>
            <button
              type="submit"
              className="rounded-md bg-indigo-600 px-4 py-2 text-sm font-semibold text-white hover:bg-indigo-500"
            >
              Create Task
            </button>
          </div>
        </form>
      )}

      {tasks.length === 0 ? (
        <div className="rounded-lg bg-white p-8 text-center shadow">
          <p className="text-gray-600">No tasks yet. Create one to get started!</p>
        </div>
      ) : (
        <div className="space-y-4">
          {tasks.map((task) => (
            <div key={task.id} className="rounded-lg bg-white p-6 shadow">
              {editingTask?.id === task.id ? (
                <form onSubmit={handleUpdateTask} className="space-y-4">
                  <input
                    type="text"
                    required
                    maxLength={200}
                    className="block w-full rounded-md border-0 px-3 py-2 text-gray-900 ring-1 ring-inset ring-gray-300 focus:ring-2 focus:ring-indigo-600"
                    value={editTitle}
                    onChange={(e) => setEditTitle(e.target.value)}
                  />
                  <textarea
                    rows={3}
                    className="block w-full rounded-md border-0 px-3 py-2 text-gray-900 ring-1 ring-inset ring-gray-300 focus:ring-2 focus:ring-indigo-600"
                    value={editDescription}
                    onChange={(e) => setEditDescription(e.target.value)}
                  />
                  <div className="flex gap-2">
                    <button
                      type="submit"
                      className="rounded-md bg-indigo-600 px-3 py-1.5 text-sm font-semibold text-white hover:bg-indigo-500"
                    >
                      Save
                    </button>
                    <button
                      type="button"
                      onClick={() => setEditingTask(null)}
                      className="rounded-md bg-gray-200 px-3 py-1.5 text-sm font-semibold text-gray-900 hover:bg-gray-300"
                    >
                      Cancel
                    </button>
                  </div>
                </form>
              ) : (
                <>
                  <div className="flex items-start justify-between">
                    <div className="flex items-start gap-3">
                      <input
                        type="checkbox"
                        checked={task.completed}
                        onChange={() => handleToggleComplete(task)}
                        className="mt-1 h-5 w-5 rounded border-gray-300 text-indigo-600 focus:ring-indigo-600"
                      />
                      <div>
                        <h3
                          className={`text-lg font-semibold ${
                            task.completed ? 'text-gray-400 line-through' : 'text-gray-900'
                          }`}
                        >
                          {task.title}
                        </h3>
                        {task.description && (
                          <p className="mt-1 text-gray-600">{task.description}</p>
                        )}
                        {task.due_date && (
                          <p className="mt-2 text-sm text-orange-600 font-medium">
                            📅 Due: {new Date(task.due_date).toLocaleDateString()}
                          </p>
                        )}
                        {task.tags && task.tags.length > 0 && (
                          <div className="mt-2 flex flex-wrap gap-2">
                            {task.tags.map((tag, index) => (
                              <span
                                key={index}
                                className="inline-flex items-center rounded-full bg-indigo-100 px-2.5 py-0.5 text-xs font-medium text-indigo-800"
                              >
                                #{tag}
                              </span>
                            ))}
                          </div>
                        )}
                        <p className="mt-2 text-xs text-gray-400">
                          Created: {new Date(task.created_at).toLocaleDateString()}
                        </p>
                      </div>
                    </div>
                    <div className="flex gap-2">
                      <button
                        onClick={() => startEdit(task)}
                        className="rounded-md bg-gray-100 px-3 py-1.5 text-sm font-semibold text-gray-900 hover:bg-gray-200"
                      >
                        Edit
                      </button>
                      <button
                        onClick={() => handleDeleteTask(task.id)}
                        className="rounded-md bg-red-100 px-3 py-1.5 text-sm font-semibold text-red-900 hover:bg-red-200"
                      >
                        Delete
                      </button>
                    </div>
                  </div>
                </>
              )}
            </div>
          ))}
        </div>
      )}
    </div>
  )
}
