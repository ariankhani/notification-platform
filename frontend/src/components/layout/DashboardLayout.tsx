import { useQueryClient } from '@tanstack/react-query'
import { Activity, Bell, ChevronDown, CircleGauge, LogOut, Menu, Network, Settings, SlidersHorizontal, X } from 'lucide-react'
import { useState } from 'react'
import { NavLink, Outlet, useNavigate } from 'react-router-dom'
import { api } from '../../api/client'
import { tokenStore } from '../../auth/token-store'
import { useCurrentUser } from '../../auth/useCurrentUser'
import { Brand } from '../Brand'

const navigation = [
  { to: '/app', label: 'Overview', icon: CircleGauge, end: true },
  { to: '/app/events', label: 'Events', icon: Activity },
  { to: '/app/notifications', label: 'Notifications', icon: Bell },
  { to: '/app/rules', label: 'Rules', icon: SlidersHorizontal },
  { to: '/app/deliveries', label: 'Deliveries', icon: Network },
]

export function DashboardLayout() {
  const [menuOpen, setMenuOpen] = useState(false); const user = useCurrentUser(); const navigate = useNavigate(); const queryClient = useQueryClient()
  async function logout() { await api.logout(); tokenStore.clear(); queryClient.clear(); navigate('/login', { replace: true }) }
  return (
    <div className="dashboard-layout" data-menu-open={menuOpen || undefined}>
      <aside className="dashboard-sidebar">
        <div className="sidebar-brand"><Brand to="/app" /></div>
        <button className="workspace-switcher" type="button"><span className="workspace-avatar">R</span><span><strong>Relay workspace</strong><small>Production</small></span><ChevronDown size={15} /></button>
        <nav className="dashboard-nav" aria-label="Dashboard navigation">{navigation.map(({ icon: Icon, ...item }) => <NavLink key={item.to} to={item.to} end={item.end} onClick={() => setMenuOpen(false)}><Icon size={17} />{item.label}</NavLink>)}</nav>
        <div className="sidebar-footer"><NavLink to="/app/settings"><Settings size={17} />Settings</NavLink><button type="button" onClick={logout}><LogOut size={17} />Sign out</button></div>
      </aside>
      <div className="dashboard-scrim" onClick={() => setMenuOpen(false)} />
      <section className="dashboard-content">
        <header className="dashboard-topbar"><button className="icon-button mobile-menu" type="button" onClick={() => setMenuOpen((open) => !open)} aria-label={menuOpen ? 'Close navigation' : 'Open navigation'}>{menuOpen ? <X size={20} /> : <Menu size={20} />}</button><span className="environment-badge"><i /> Production</span><div className="topbar-user"><span>{user.data ? `${user.data.name} ${user.data.last_name}` : 'Loading account…'}</span><span className="user-avatar">{user.data?.name?.[0]?.toUpperCase() ?? 'R'}</span></div></header>
        <div className="dashboard-page"><Outlet /></div>
      </section>
    </div>
  )
}
