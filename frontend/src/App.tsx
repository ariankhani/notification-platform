import { Navigate, Route, Routes } from 'react-router-dom'
import { ProtectedRoute } from './auth/ProtectedRoute'
import { AuthLayout } from './components/layout/AuthLayout'
import { DashboardLayout } from './components/layout/DashboardLayout'
import { DashboardPage } from './pages/DashboardPage'
import { EventsPage } from './pages/EventsPage'
import { LandingPage } from './pages/LandingPage'
import { LoginPage } from './pages/LoginPage'
import { NotFoundPage } from './pages/NotFoundPage'
import { RegisterPage } from './pages/RegisterPage'

export default function App() {
  return (
    <Routes>
      <Route path="/" element={<LandingPage />} />
      <Route element={<AuthLayout />}>
        <Route path="/login" element={<LoginPage />} />
        <Route path="/register" element={<RegisterPage />} />
      </Route>
      <Route element={<ProtectedRoute />}>
        <Route path="/app" element={<DashboardLayout />}>
          <Route index element={<DashboardPage />} />
          <Route path="events" element={<EventsPage />} />
          <Route path="notifications" element={<ComingSoon title="Notifications" />} />
          <Route path="rules" element={<ComingSoon title="Rules" />} />
          <Route path="deliveries" element={<ComingSoon title="Deliveries" />} />
          <Route path="settings" element={<ComingSoon title="Settings" />} />
        </Route>
      </Route>
      <Route path="/dashboard" element={<Navigate to="/app" replace />} />
      <Route path="*" element={<NotFoundPage />} />
    </Routes>
  )
}

function ComingSoon({ title }: { title: string }) {
  return (
    <section className="page-section">
      <div className="page-heading"><div><p className="page-kicker">Workspace</p><h1>{title}</h1><p>This module will be connected when its API contract is available.</p></div></div>
      <div className="empty-state"><span className="empty-state-mark" aria-hidden="true" /><h2>{title} is ready for the next milestone</h2><p>The route, navigation, access control and responsive shell are already in place.</p></div>
    </section>
  )
}
