import { Outlet } from 'react-router-dom'
import { Brand } from '../Brand'
export function AuthLayout() {
  return <main className="auth-page"><div className="auth-brand"><Brand /></div><section className="auth-panel"><Outlet /></section><aside className="auth-aside" aria-hidden="true"><div className="auth-grid" /><div className="auth-message"><span>EVENT RECEIVED</span><strong>payment.received</strong><div><i /> Rule matched</div><div><i /> Push delivered</div></div></aside></main>
}
