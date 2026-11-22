import { Activity, Bell, Clock3, TriangleAlert } from 'lucide-react'
const stats = [
  { label: 'Events today', value: '—', detail: 'Waiting for events API', icon: Activity },
  { label: 'Delivered', value: '—', detail: 'No delivery data yet', icon: Bell },
  { label: 'Median latency', value: '—', detail: 'Calculated after delivery', icon: Clock3 },
  { label: 'Failed', value: '—', detail: 'No delivery data yet', icon: TriangleAlert },
]
export function DashboardPage() {
  return <section className="page-section"><div className="page-heading dashboard-welcome"><div><p className="page-kicker">Production workspace</p><h1>Overview</h1><p>Monitor notification traffic and delivery health.</p></div><button className="button button-small" type="button" disabled>Send test event</button></div><div className="stat-grid">{stats.map(({ icon: Icon, ...stat }) => <article className="stat-card" key={stat.label}><span className="stat-icon"><Icon size={18} /></span><p>{stat.label}</p><strong>{stat.value}</strong><small>{stat.detail}</small></article>)}</div><div className="dashboard-grid"><article className="content-card traffic-card"><div className="card-heading"><div><h2>Delivery activity</h2><p>Last 24 hours</p></div><span className="data-state">Awaiting API</span></div><div className="chart-empty"><span /><p>Delivery metrics will appear after the worker API is connected.</p></div></article><article className="content-card quickstart-card"><div className="card-heading"><div><h2>Quick start</h2><p>Connect your first application</p></div></div><ol className="setup-list"><li data-complete><span>1</span><div><strong>Create your account</strong><p>Your dashboard access is ready.</p></div></li><li><span>2</span><div><strong>Create a project</strong><p>Requires the projects API.</p></div></li><li><span>3</span><div><strong>Send your first event</strong><p>Use an environment API key.</p></div></li></ol></article></div></section>
}
