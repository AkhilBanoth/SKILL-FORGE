import { Component, lazy, Suspense, useEffect, useState, type ReactNode } from 'react'
import { BrowserRouter, Navigate, Route, Routes } from 'react-router-dom'
import { AlertTriangle, RefreshCw } from 'lucide-react'
import { PublicLayout, WorkspaceLayout } from './components/layout/AppShell'
import { Skeleton } from './components/ui'
import { ToastProvider } from './components/toast'
import { loadLive, session, token } from './data/live'
import './skillforge.css'
import './route-states.css'
import './shell-fixes.css'
import './overflow-fixes.css'

const LandingPage = lazy(async () => ({ default: (await import('./pages/public/PublicPages')).LandingPage }))
const LoginPage = lazy(async () => ({ default: (await import('./pages/public/PublicPages')).LoginPage }))
const RegisterPage = lazy(async () => ({ default: (await import('./pages/public/PublicPages')).RegisterPage }))
const CertificateVerifyPage = lazy(async () => ({ default: (await import('./pages/public/PublicPages')).CertificateVerifyPage }))
const LearnerRouter = lazy(async () => ({ default: (await import('./pages/learner/LearnerRouter')).LearnerRouter }))
const AdminRouter = lazy(async () => ({ default: (await import('./pages/admin/AdminPages')).AdminRouter }))

function App() {
  const [darkMode, setDarkMode] = useState(() => localStorage.getItem('skillforge-theme') === 'dark')

  useEffect(() => {
    document.documentElement.dataset.theme = darkMode ? 'dark' : 'light'
    localStorage.setItem('skillforge-theme', darkMode ? 'dark' : 'light')
  }, [darkMode])

  const [ready, setReady] = useState(!token.get())
  useEffect(() => { if (token.get()) loadLive().catch(() => token.clear()).finally(() => setReady(true)) }, [])
  if (!ready) return <RouteLoading />

  return (
    <BrowserRouter>
      <RouteErrorBoundary>
        <ToastProvider>
          <Routes>
            <Route path="/" element={<PublicLayout><Suspense fallback={<RouteLoading />}><LandingPage /></Suspense></PublicLayout>} />
            <Route path="/login" element={<Suspense fallback={<RouteLoading />}><LoginPage /></Suspense>} />
            <Route path="/register" element={<Suspense fallback={<RouteLoading />}><RegisterPage /></Suspense>} />
            <Route path="/verify" element={<PublicLayout><Suspense fallback={<RouteLoading />}><CertificateVerifyPage /></Suspense></PublicLayout>} />
            <Route path="/app" element={<Guard><WorkspaceLayout darkMode={darkMode} onToggleTheme={() => setDarkMode((value) => !value)} /></Guard>}>
              <Route index element={<Navigate to="dashboard" replace />} />
              <Route path="*" element={<Suspense fallback={<RouteLoading />}><LearnerRouter /></Suspense>} />
            </Route>
            <Route path="/admin" element={<Guard admin><WorkspaceLayout admin darkMode={darkMode} onToggleTheme={() => setDarkMode((value) => !value)} /></Guard>}>
              <Route index element={<Suspense fallback={<RouteLoading />}><AdminRouter /></Suspense>} />
              <Route path="*" element={<Suspense fallback={<RouteLoading />}><AdminRouter /></Suspense>} />
            </Route>
            <Route path="*" element={<Navigate to="/" replace />} />
          </Routes>
        </ToastProvider>
      </RouteErrorBoundary>
    </BrowserRouter>
  )
}

function Guard({ children, admin = false }: { children: ReactNode; admin?: boolean }) {
  if (!token.get()) return <Navigate to="/login" replace />
  if (admin && session.role !== 'admin') return <Navigate to="/app/dashboard" replace />
  return children
}

function RouteLoading() {
  return <main className="route-loading" aria-label="Loading page"><Skeleton className="loading-kicker" /><Skeleton className="loading-title" /><Skeleton className="loading-copy" /><div><Skeleton /><Skeleton /><Skeleton /></div></main>
}

class RouteErrorBoundary extends Component<{ children: ReactNode }, { failed: boolean }> {
  state = { failed: false }

  static getDerivedStateFromError() { return { failed: true } }

  render() {
    if (this.state.failed) return <main className="route-error"><span><AlertTriangle size={20} /></span><h1>This screen didn’t load</h1><p>Your progress is safe. Try loading this view again.</p><button className="ui-button ui-button-primary" onClick={() => this.setState({ failed: false })}><RefreshCw size={14} /> Try again</button></main>
    return this.props.children
  }
}

export default App
