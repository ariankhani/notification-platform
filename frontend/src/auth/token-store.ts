import type { TokenPair } from '../api/types'

const TOKEN_KEY = 'relay.auth.tokens'
export const tokenStore = {
  get(): TokenPair | null {
    const value = window.sessionStorage.getItem(TOKEN_KEY)
    if (!value) return null
    try { return JSON.parse(value) as TokenPair } catch { window.sessionStorage.removeItem(TOKEN_KEY); return null }
  },
  set(tokens: TokenPair) { window.sessionStorage.setItem(TOKEN_KEY, JSON.stringify(tokens)) },
  clear() { window.sessionStorage.removeItem(TOKEN_KEY) },
}
