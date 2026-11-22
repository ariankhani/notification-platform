import { BellRing } from 'lucide-react'
import { Link } from 'react-router-dom'
export function Brand({ to = '/' }: { to?: string }) { return <Link className="wordmark" to={to} aria-label="Relay home"><span className="wordmark-mark"><BellRing size={16} strokeWidth={2.4} /></span>Relay</Link> }
