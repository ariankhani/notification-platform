import { Check, Terminal } from 'lucide-react'
import { Link } from 'react-router-dom'
import { Brand } from '../components/Brand'
import { NotificationStory } from '../components/NotificationStory'

export function LandingPage() {
  return (
    <main className="marketing-page">
      <nav className="nav shell" aria-label="Main navigation">
        <Brand />
        <div className="nav-links"><a href="#product">Product</a><a href="#developers">Developers</a><a href="#pricing">Pricing</a></div>
        <div className="nav-actions"><Link className="text-action" to="/login">Sign in</Link><Link className="button button-small" to="/register">Start building</Link></div>
      </nav>
      <section className="hero shell" id="top">
        <div className="hero-copy">
          <div className="eyebrow"><span className="live-dot" />Built for event-driven products</div>
          <h1>Every event.<br />The right message.</h1>
          <p className="hero-lede">One API for reliable product notifications. Route events, apply rules, and track every delivery without rebuilding the pipeline.</p>
          <div className="hero-actions"><Link className="button" to="/register">Start building</Link><a className="button button-quiet" href="/docs"><Terminal size={16} /> Read the API docs</a></div>
          <div className="hero-proof"><span><Check size={14} /> FastAPI-ready</span><span><Check size={14} /> Delivery logs included</span></div>
        </div>
        <div className="hero-visual" aria-label="An event moving through a notification dashboard and arriving on a phone"><NotificationStory /></div>
      </section>
      <section className="trust-strip shell" aria-label="Supported notification concepts"><span>Events</span><i /><span>Rules</span><i /><span>Queues</span><i /><span>Delivery attempts</span><i /><span>Webhooks</span></section>
    </main>
  )
}
