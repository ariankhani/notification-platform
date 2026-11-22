import { useMutation } from '@tanstack/react-query'
import { type FormEvent, useState } from 'react'
import { Link, useNavigate } from 'react-router-dom'
import { ApiError, api } from '../api/client'
import type { RegisterInput } from '../api/types'
import { FormField } from '../components/FormField'

const emptyForm: RegisterInput = { username: '', email: '', name: '', last_name: '', password: '' }
export function RegisterPage() {
  const navigate = useNavigate(); const [form, setForm] = useState(emptyForm)
  const mutation = useMutation({ mutationFn: api.register, onSuccess: () => navigate('/login', { replace: true, state: { registered: true } }) })
  function update(field: keyof RegisterInput, value: string) { setForm((current) => ({ ...current, [field]: value })) }
  function submit(event: FormEvent) { event.preventDefault(); if (!Object.values(form).some((value) => !value.trim()) && form.password.length >= 8) mutation.mutate({ ...form, username: form.username.trim(), email: form.email.trim() }) }
  return <div className="auth-card auth-card-wide"><div className="auth-heading"><p className="page-kicker">Create your workspace</p><h1>Start building with Relay</h1><p>Your first account will become the owner of the workspace.</p></div><form onSubmit={submit} className="auth-form" noValidate>{mutation.isError && <div className="form-alert" role="alert">{mutation.error instanceof ApiError ? mutation.error.message : 'Unable to create your account.'}</div>}<div className="form-grid"><FormField id="name" label="First name" autoComplete="given-name" value={form.name} onChange={(e) => update('name', e.target.value)} required /><FormField id="last-name" label="Last name" autoComplete="family-name" value={form.last_name} onChange={(e) => update('last_name', e.target.value)} required /></div><FormField id="email" label="Work email" type="email" autoComplete="email" value={form.email} onChange={(e) => update('email', e.target.value)} required /><FormField id="username" label="Username" autoComplete="username" value={form.username} onChange={(e) => update('username', e.target.value)} required /><FormField id="password" label="Password" type="password" autoComplete="new-password" value={form.password} onChange={(e) => update('password', e.target.value)} required minLength={8} /><p className="field-help">Use at least 8 characters.</p><button className="button form-submit" type="submit" disabled={mutation.isPending}>{mutation.isPending ? 'Creating account…' : 'Create account'}</button></form><p className="auth-switch">Already have an account? <Link to="/login">Sign in</Link></p></div>
}
