import { Link } from 'react-router-dom'
import { Brand } from '../components/Brand'
export function NotFoundPage() { return <main className="not-found-page"><Brand /><div><p className="page-kicker">404</p><h1>That page does not exist.</h1><p>The address may be incorrect or the page may have moved.</p><Link className="button" to="/">Return home</Link></div></main> }
