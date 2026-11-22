import { Navigate, Outlet, useLocation } from 'react-router-dom'
import { tokenStore } from './token-store'
export function ProtectedRoute() { const location = useLocation(); return tokenStore.get() ? <Outlet /> : <Navigate to="/login" replace state={{ from: location.pathname }} /> }
