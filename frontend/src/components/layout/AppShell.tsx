import { useMemo, useState, type ReactNode } from 'react'
import { Link, NavLink, Outlet, useLocation } from 'react-router-dom'
import { appNotifications, assessments, learner } from '../../data/mockData'
import { session, signOut } from '../../data/live'
import { Activity, Award, Bell, BookOpen, BriefcaseBusiness, ChartNoAxesCombined, ChevronLeft, ChevronRight, FileText, GraduationCap, LayoutDashboard, Menu, Moon, Search, Settings, ShieldCheck, Sparkles, Sun, UserRound, Users, WandSparkles, X } from 'lucide-react'
import { Avatar, Badge, Drawer } from '../ui'

const learnerNavigation = [
  { label: 'Overview', to: '/app/dashboard', icon: LayoutDashboard },
  { label: 'My skills', to: '/app/skills', icon: Sparkles },
  { label: 'Career paths', to: '/app/careers', icon: BriefcaseBusiness },
  { label: 'Courses', to: '/app/courses', icon: BookOpen },
  { label: 'Assessments', to: '/app/assessments', icon: ChartNoAxesCombined },
  { label: 'Projects', to: '/app/projects', icon: Activity },
  { label: 'Certificates', to: '/app/certificates', icon: Award },
  { label: 'Resume insights', to: '/app/resume', icon: FileText },
  { label: 'Notifications', to: '/app/notifications', icon: Bell },
  { label: 'AI mentor', to: '/app/mentor', icon: WandSparkles },
]
const adminNavigation = [
  { label: 'Overview', to: '/admin', icon: LayoutDashboard },
  { label: 'Users', to: '/admin/users', icon: Users },
  { label: 'Learning analytics', to: '/admin/analytics', icon: ChartNoAxesCombined },
  { label: 'Review queue', to: '/admin/reviews', icon: ShieldCheck },
  { label: 'Certificates', to: '/admin/certificates', icon: Award },
  { label: 'Content studio', to: '/admin/content', icon: BookOpen },
]
const shortcuts = [...learnerNavigation, ...adminNavigation, { label: 'Profile & settings', to: '/app/profile', icon: UserRound }]

export function WorkspaceLayout({ admin = false, darkMode, onToggleTheme }: { admin?: boolean; darkMode: boolean; onToggleTheme: () => void }) {
  const [collapsed, setCollapsed] = useState(false)
  const [mobileOpen, setMobileOpen] = useState(false)
  const [search, setSearch] = useState('')
  const [alertsOpen, setAlertsOpen] = useState(false)
  const location = useLocation()
  const openAssessments = assessments.filter((a) => a.status === 'Ready' || a.status === 'In progress').length
  const navItems = admin ? adminNavigation : learnerNavigation
  const mobileNavigation = admin
    ? [{ to: '/admin', label: 'Home', icon: LayoutDashboard }, { to: '/admin/users', label: 'Users', icon: Users }, { to: '/admin/reviews', label: 'Reviews', icon: ShieldCheck }, { to: '/admin/content', label: 'Content', icon: BookOpen }]
    : [{ to: '/app/dashboard', label: 'Home', icon: LayoutDashboard }, { to: '/app/courses', label: 'Learn', icon: BookOpen }, { to: '/app/mentor', label: 'Mentor', icon: WandSparkles }, { to: '/app/profile', label: 'Profile', icon: UserRound }]
  const title = useMemo(() => {
    const path = location.pathname
    const matched = shortcuts.find((item) => path === item.to || (item.to !== '/app/dashboard' && item.to !== '/admin' && path.startsWith(`${item.to}/`)))
    if (path.includes('/careers/')) return 'Career profile'
    if (path.includes('/courses/') && path.includes('/lesson')) return 'Lesson workspace'
    if (path.includes('/courses/')) return 'Course overview'
    if (path.includes('/assessments/')) return 'Assessment'
    return matched?.label ?? (admin ? 'Admin overview' : 'Your learning hub')
  }, [location.pathname, admin])
  const results = search.trim() ? shortcuts.filter((item) => item.label.toLowerCase().includes(search.toLowerCase())).slice(0, 5) : []

  const navigation = <>
    <div className="sidebar-brand"><Link to="/" className="brand-lockup"><span className="brand-mark"><GraduationCap size={19} /></span>{(!collapsed || mobileOpen) && <span>skill<span>forge</span></span>}</Link>{admin && <Badge tone="violet">ADMIN</Badge>}</div>
    <div className="sidebar-section-label">{(!collapsed || mobileOpen) && <span>{admin ? 'WORKSPACE' : 'LEARN'}</span>}</div>
    <nav className="side-nav" aria-label={admin ? 'Admin navigation' : 'Learner navigation'}>{navItems.map(({ label, to, icon: Icon }) => <NavLink key={to} to={to} end={to === '/admin' || to === '/app/dashboard'} title={collapsed && !mobileOpen ? label : undefined} onClick={() => setMobileOpen(false)} className={({ isActive }) => `side-link ${isActive ? 'selected' : ''} ${admin ? 'admin-link' : ''}`}><Icon size={18} strokeWidth={1.8} />{(!collapsed || mobileOpen) && <span>{label}</span>}{label === 'Assessments' && !admin && (!collapsed || mobileOpen) && openAssessments > 0 && <span className="nav-count">{openAssessments}</span>}</NavLink>)}</nav>
    <div className="sidebar-bottom">{session.role === 'admin' && (!collapsed || mobileOpen) && <Link to={admin ? '/app/dashboard' : '/admin'} className="side-link" onClick={() => setMobileOpen(false)}><ShieldCheck size={18} /><span>{admin ? 'Learner view' : 'Admin console'}</span></Link>}<NavLink to="/app/profile" className={({ isActive }) => `side-link settings-link ${isActive ? 'selected' : ''}`}><Settings size={18} />{(!collapsed || mobileOpen) && <span>Settings</span>}</NavLink></div>
    <button className="collapse-toggle" onClick={() => setCollapsed((value) => !value)} aria-label={collapsed ? 'Expand sidebar' : 'Collapse sidebar'}>{collapsed ? <ChevronRight size={16} /> : <ChevronLeft size={16} />}</button>
  </>

  return <div className={`workspace ${admin ? 'workspace-admin' : ''} ${collapsed ? 'sidebar-collapsed' : ''}`}>
    <aside className="sidebar">{navigation}</aside>
    <div className="workspace-main">
      <header className="topbar"><button className="mobile-menu icon-button" aria-label="Open navigation" onClick={() => setMobileOpen(true)}><Menu size={20} /></button><div className="topbar-title"><span>{admin ? 'SKILLFORGE / ADMIN' : 'SKILLFORGE / LEARNING'}</span><strong>{title}</strong></div>
        <div className="topbar-actions"><div className="global-search"><Search size={16} /><input value={search} onChange={(event) => setSearch(event.target.value)} placeholder="Search your workspace" aria-label="Search your workspace" />{search && <button className="search-clear" onClick={() => setSearch('')} aria-label="Clear search"><X size={14} /></button>}{results.length > 0 && <div className="search-results">{results.map((item) => <Link key={`${item.to}-${item.label}`} to={item.to} onClick={() => setSearch('')}><item.icon size={15} />{item.label}<ChevronRight size={14} /></Link>)}</div>}</div>
          <button className="icon-button notification-trigger" aria-label="Notifications" onClick={() => setAlertsOpen(true)}><Bell size={18} />{appNotifications.some((n) => n.unread) && <i />}</button>
          <button className="icon-button theme-trigger" aria-label={darkMode ? 'Switch to light mode' : 'Switch to dark mode'} onClick={onToggleTheme}>{darkMode ? <Sun size={18} /> : <Moon size={18} />}</button>
          <Link className="user-trigger" to="/app/profile"><Avatar name={learner.name} size="sm" /><span>{learner.name}</span><ChevronRight size={14} /></Link><button className="ui-button ui-button-ghost ui-button-sm" onClick={signOut}>Log out</button>
        </div>
      </header>
      <main className="page-main"><Outlet /></main>
      <nav className="mobile-tabs" aria-label="Primary navigation">{mobileNavigation.map(({ to, label, icon: Icon }) => <NavLink key={to} to={to} end={to === '/admin'} className={({ isActive }) => `mobile-tab ${isActive ? 'selected' : ''}`}><Icon size={19} /><span>{label}</span></NavLink>)}</nav>
    </div>
    <Drawer open={mobileOpen} onClose={() => setMobileOpen(false)} title="Navigation"><div className="mobile-drawer-nav">{navigation}</div></Drawer>
    <Drawer open={alertsOpen} onClose={() => setAlertsOpen(false)} title="Notifications"><div className="alert-list">{appNotifications.slice(0, 4).map((n) => <div className={`alert-row ${n.unread ? 'unread' : ''}`} key={n.id}><span className="alert-glyph"><Award size={17} /></span><div><strong>{n.title}</strong><p>{n.description}</p></div></div>)}{appNotifications.length === 0 && <p>You’re all caught up.</p>}<Link to="/app/notifications" className="alert-link" onClick={() => setAlertsOpen(false)}>View all notifications <ChevronRight size={15} /></Link></div></Drawer>
  </div>
}

export function PublicLayout({ children }: { children: ReactNode }) {
  return <div className="public-shell"><header className="public-nav"><Link to="/" className="brand-lockup"><span className="brand-mark"><GraduationCap size={19} /></span><span>skill<span>forge</span></span></Link><nav><a href="/#how-it-works">How it works</a><a href="/#careers">Career paths</a><a href="/verify">Verify certificate</a></nav><div><Link className="public-login" to="/login">Log in</Link><Link className="public-signup" to="/register">Get started <ChevronRight size={15} /></Link></div></header>{children}<footer className="public-footer"><Link to="/" className="brand-lockup"><span className="brand-mark"><GraduationCap size={16} /></span><span>skill<span>forge</span></span></Link><span>Build skills that move your career forward.</span><div><Link to="/verify">Certificate verification</Link><a href="mailto:hello@skillforge.dev">Contact</a><span>© 2026 SkillForge</span></div></footer></div>
}
