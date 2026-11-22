import { useQuery } from '@tanstack/react-query'
import { api } from '../api/client'
import { tokenStore } from './token-store'
export const currentUserKey = ['current-user'] as const
export function useCurrentUser() { return useQuery({ queryKey: currentUserKey, queryFn: api.me, enabled: Boolean(tokenStore.get()), retry: false }) }
