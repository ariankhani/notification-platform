import { tokenStore } from '../auth/token-store'
import type { ApiErrorPayload, RegisterInput, TokenPair, User } from './types'

const API_BASE_URL = import.meta.env.VITE_API_URL ?? '/api'
export class ApiError extends Error {
  constructor(message: string, public readonly status: number, public readonly payload?: ApiErrorPayload) { super(message); this.name = 'ApiError' }
}
async function parseError(response: Response): Promise<ApiError> {
  let payload: ApiErrorPayload | undefined
  try { payload = await response.json() as ApiErrorPayload } catch { payload = undefined }
  const detail = payload?.detail
  const message = typeof detail === 'string' ? detail : Array.isArray(detail) ? detail[0]?.msg ?? 'The submitted data is invalid.' : 'Something went wrong. Please try again.'
  return new ApiError(message, response.status, payload)
}
async function refreshTokens(refreshToken: string): Promise<TokenPair | null> {
  const params = new URLSearchParams({ refresh_token: refreshToken })
  const response = await fetch(`${API_BASE_URL}/auth/refresh?${params.toString()}`, { method: 'POST' })
  if (!response.ok) return null
  const tokens = await response.json() as TokenPair
  tokenStore.set(tokens)
  return tokens
}
async function request<T>(path: string, init: RequestInit = {}, withAuth = true): Promise<T> {
  const headers = new Headers(init.headers)
  if (!(init.body instanceof FormData) && !headers.has('Content-Type')) headers.set('Content-Type', 'application/json')
  const tokens = tokenStore.get()
  if (withAuth && tokens) headers.set('Authorization', `Bearer ${tokens.access_token}`)
  const response = await fetch(`${API_BASE_URL}${path}`, { ...init, headers })
  if (response.status === 401 && withAuth && tokens?.refresh_token) {
    const refreshed = await refreshTokens(tokens.refresh_token)
    if (refreshed) {
      headers.set('Authorization', `Bearer ${refreshed.access_token}`)
      const retry = await fetch(`${API_BASE_URL}${path}`, { ...init, headers })
      if (!retry.ok) throw await parseError(retry)
      if (retry.status === 204) return undefined as T
      return retry.json() as Promise<T>
    }
    tokenStore.clear()
  }
  if (!response.ok) throw await parseError(response)
  if (response.status === 204) return undefined as T
  return response.json() as Promise<T>
}
export const api = {
  async login(username: string, password: string) {
    const body = new URLSearchParams({ username, password })
    const response = await fetch(`${API_BASE_URL}/auth/login`, { method: 'POST', headers: { 'Content-Type': 'application/x-www-form-urlencoded' }, body })
    if (!response.ok) throw await parseError(response)
    const tokens = await response.json() as TokenPair
    tokenStore.set(tokens)
    return tokens
  },
  register(input: RegisterInput) { return request<User>('/auth/register', { method: 'POST', body: JSON.stringify(input) }, false) },
  me() { return request<User>('/users/me') },
  async logout() { try { await request<void>('/auth/logout', { method: 'POST' }) } finally { tokenStore.clear() } },
}
