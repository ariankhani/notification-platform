import { useMutation, useQueryClient } from '@tanstack/react-query'
import { type FormEvent, useState } from 'react'
import { Link, useLocation, useNavigate } from 'react-router-dom'
import { ApiError, api } from '../api/client'
import { currentUserKey } from '../auth/useCurrentUser'
import { FormField } from '../components/FormField'

export function LoginPage() {
  const navigate = useNavigate(); const location = useLocation(); const queryClient = useQueryClient()
  const [username, setUsername] = useState(''); const [password, setPassword] = useState('')
  const mutation = useMutation({ mutationFn: () => api.login(username.trim(), password), onSuccess: async () => { await queryClient.invalidateQueries({ queryKey: currentUserKey }); navigate((location.state as { from?: string } | null)?.from ?? '/app', { replace: true }) } })
  function submit(event: FormEvent) { event.preventDefault(); if (username.trim() && password) mutation.mutate() }
  return <div className="auth-card"><div className="auth-heading"><p className="page-kicker">Welcome back</p><h1>Sign in to Relay</h1><p>Monitor events, rules and delivery attempts from one workspace.</p></div><form onSubmit={submit} className="auth-form" noValidate>{mutation.isError && <div className="form-alert" role="alert">{mutation.error instanceof ApiError ? mutation.error.message : 'Unable to sign in right now.'}</div>}<FormField id="username" label="Username" autoComplete="username" value={username} onChange={(event) => setUsername(event.target.value)} required /><FormField id="password" label="Password" type="password" autoComplete="current-password" value={password} onChange={(event) => setPassword(event.target.value)} required minLength={8} /><button className="button form-submit" type="submit" disabled={mutation.isPending || !username.trim() || !password}>{mutation.isPending ? 'Signing in…' : 'Sign in'}</button></form><p className="auth-switch">New to Relay? <Link to="/register">Create an account</Link></p></div>
}
