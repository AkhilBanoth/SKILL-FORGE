import { useCallback, useEffect, useMemo, useState, type FormEvent } from 'react'
import { Link, useLocation } from 'react-router-dom'
import { Bar, BarChart, CartesianGrid, Cell, Pie, PieChart, ResponsiveContainer, Tooltip, XAxis, YAxis } from 'recharts'
import { Activity, ArrowRight, ArrowUpRight, Award, BookOpen, Check, CheckCircle2, ChevronRight, ClipboardCheck, Clock3, FileText, Search, ShieldCheck, Sparkles, Target, Users, X } from 'lucide-react'
import { Avatar, Badge, Button, Card, DataTable, EmptyState, Input, Modal, Progress, Select, Skeleton, StatCard, Textarea } from '../../components/ui'
import { useToast } from '../../components/toast-context'
import { api, session } from '../../data/live'
import './admin.css'

// eslint-disable-next-line @typescript-eslint/no-explicit-any
type J = any
const errMsg = (e: unknown) => (e instanceof Error ? e.message : 'Something went wrong')
const fmt = (d?: string) => (d ? new Date(d).toLocaleDateString('en', { month: 'short', day: 'numeric', year: 'numeric' }) : '—')
const TIP = { background: 'var(--surface)', border: '1px solid var(--border)', borderRadius: 8, fontSize: 12 }

/** Loads a set of endpoints once; each failed call resolves to its fallback. */
function useLoad<T extends Record<string, unknown>>(paths: { [K in keyof T]: [string, T[K]] }) {
  const [data, setData] = useState<T | null>(null); const [error, setError] = useState('')
  const load = useCallback(async () => {
    try {
      const keys = Object.keys(paths) as (keyof T)[]
      const out = await Promise.all(keys.map((k) => api(paths[k][0]).catch((e: Error) => { if (/Admin access/i.test(e.message)) throw e; return paths[k][1] })))
      setData(Object.fromEntries(keys.map((k, i) => [k, out[i]])) as T); setError('')
    } catch (e) { setError(errMsg(e)) }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [])
  useEffect(() => { load() }, [load])
  return { data, error, reload: load }
}
const Loading = () => <div className="admin-page"><Skeleton /><Skeleton /><Skeleton /></div>
const Denied = ({ msg }: { msg: string }) => <div className="admin-page"><EmptyState icon={<ShieldCheck size={18} />} title="Admin access required" description={msg} action={<Link className="ui-button ui-button-primary" to="/app/dashboard">Back to learner view</Link>} /></div>

export function AdminRouter() {
  const { pathname } = useLocation()
  if (session.role !== 'admin') return <Denied msg="Your account doesn’t have admin permissions." />
  if (pathname === '/admin' || pathname === '/admin/') return <AdminOverviewPage />
  if (pathname === '/admin/users') return <AdminUsersPage />
  if (pathname === '/admin/analytics') return <AdminAnalyticsPage />
  if (pathname === '/admin/reviews') return <AdminReviewsPage />
  if (pathname === '/admin/certificates') return <AdminCertificatesPage />
  if (pathname === '/admin/content') return <ContentStudioPage />
  return <AdminOverviewPage />
}

const base = { stats: ['/admin/dashboard/stats', null] as [string, J], users: ['/admin/users', []] as [string, J], progress: ['/admin/learning-progress', null] as [string, J], subs: ['/admin/project-submissions', null] as [string, J], courses: ['/courses', []] as [string, J], projects: ['/projects', []] as [string, J] }

export function AdminOverviewPage() {
  const { data, error } = useLoad<Record<keyof typeof base, J>>(base)
  if (error) return <Denied msg={error} />
  if (!data) return <Loading />
  const { stats, users, progress, subs, courses, projects } = data
  const uname = (id: number) => users.find((u: J) => u.id === id)?.full_name ?? `User ${id}`
  const ptitle = (id: number) => projects.find((p: J) => p.id === id)?.title ?? `Project ${id}`
  const pending: J[] = (subs?.submissions ?? []).filter((s: J) => ['submitted', 'pending'].includes(String(s.status).toLowerCase()))
  const perCourse = courses.map((c: J) => { const recs = (progress?.records ?? []).filter((r: J) => r.course_id === c.id); return { id: c.id, name: c.title, learners: recs.length, avg: recs.length ? Math.round(recs.reduce((s: number, r: J) => s + r.progress_percentage, 0) / recs.length) : 0 } })
  const top = [...perCourse].sort((a, b) => b.learners - a.learners).slice(0, 3)
  return <div className="admin-page animate-enter"><div className="page-heading"><div><div className="eyebrow">SKILLFORGE OPERATIONS</div><h1>Admin overview</h1><p>A clear view of learner momentum, platform health, and work needing review.</p></div><Badge tone="violet"><ShieldCheck size={12} /> ADMIN WORKSPACE</Badge></div>
    <div className="admin-kpi-grid"><StatCard label="Total users" value={String(stats?.total_users ?? 0)} change={`${stats?.active_users ?? 0} active`} icon={<Users size={18} />} tone="primary" /><StatCard label="Courses" value={String(stats?.total_courses ?? 0)} icon={<BookOpen size={18} />} tone="violet" /><StatCard label="Assessments" value={String(stats?.total_assessments ?? 0)} icon={<Target size={18} />} tone="green" /><StatCard label="Projects" value={String(stats?.total_projects ?? 0)} change={`${subs?.total_submissions ?? 0} ${subs?.total_submissions === 1 ? 'submission' : 'submissions'}`} icon={<Award size={18} />} tone="amber" /></div>
    <div className="admin-overview-grid"><Card className="admin-chart-card"><div className="card-heading"><div><div className="eyebrow">PLATFORM ENGAGEMENT</div><h2>Average progress by course</h2></div></div>
      {perCourse.length ? <div className="admin-activity-chart"><ResponsiveContainer width="100%" height="100%"><BarChart data={perCourse} margin={{ top: 10, right: 5, bottom: 0, left: -20 }}><CartesianGrid vertical={false} stroke="var(--border)" strokeDasharray="3 5" /><XAxis dataKey="name" axisLine={false} tickLine={false} tick={{ fill: '#8791a4', fontSize: 12 }} /><YAxis domain={[0, 100]} axisLine={false} tickLine={false} tick={{ fill: '#8791a4', fontSize: 12 }} /><Tooltip cursor={{ fill: 'rgba(98,87,228,0.06)' }} contentStyle={TIP} formatter={(v) => [`${v}%`, 'Avg progress']} /><Bar dataKey="avg" fill="#6257e4" radius={[5, 5, 0, 0]} barSize={28} /></BarChart></ResponsiveContainer></div> : <EmptyState icon={<BookOpen size={16} />} title="No courses yet" description="Create a course in the content studio." />}</Card>
      <Card className="admin-review-card"><div className="card-heading"><div><div className="eyebrow">NEEDS YOUR EYE</div><h2>Review queue</h2></div><Badge tone="warning">{pending.length} waiting</Badge></div><div className="admin-review-list">{pending.slice(0, 3).map((s) => <div className="admin-review-row" key={s.id}><Avatar name={uname(s.user_id)} size="sm" /><div><strong>{ptitle(s.project_id)}</strong><span>{uname(s.user_id)} · {fmt(s.submitted_at)}</span></div><Link to="/admin/reviews" aria-label="Review submission"><ChevronRight size={15} /></Link></div>)}{pending.length === 0 && <p>Nothing waiting. 🎉</p>}</div><Link to="/admin/reviews" className="admin-card-link">Open review queue <ArrowRight size={13} /></Link></Card></div>
    <div className="admin-lower-grid"><Card className="admin-course-performance"><div className="card-heading"><div><div className="eyebrow">LEARNING QUALITY</div><h2>Top courses</h2></div><Link to="/admin/content" className="text-link small-link">Manage content <ArrowUpRight size={13} /></Link></div><div className="top-course-list">{top.map((c, i) => <div key={c.id}><span className={`top-course-number top-number-${i}`}>0{i + 1}</span><div><strong>{c.name}</strong><small>{c.learners} learners</small></div><div className="top-course-completion"><Progress value={c.avg} /><b>{c.avg}%</b></div></div>)}{top.length === 0 && <p>No course activity yet.</p>}</div></Card>
      <Card className="admin-health-card"><div className="eyebrow">PLATFORM HEALTH</div><h2>At a glance</h2><div className="health-metric"><span><i className="health-dot" /> Completed courses</span><strong>{progress?.completed_courses ?? 0}</strong></div><div className="health-metric"><span><i className="health-dot" /> In progress</span><strong>{progress?.in_progress_courses ?? 0}</strong></div><div className="health-metric"><span><i className={`health-dot ${pending.length ? 'amber-health' : ''}`} /> Pending reviews</span><strong>{pending.length}</strong></div><Link to="/admin/analytics">See all analytics <ArrowRight size={13} /></Link></Card></div></div>
}

export function AdminUsersPage() {
  const notify = useToast(); const { data, error, reload } = useLoad<{ users: J[] }>({ users: ['/admin/users', []] }); const [role, setRole] = useState('All roles'); const [q, setQ] = useState('')
  if (error) return <Denied msg={error} />
  if (!data) return <Loading />
  const users: J[] = data.users
  const filtered = users.filter((u) => (role === 'All roles' || u.role === role) && `${u.full_name} ${u.email}`.toLowerCase().includes(q.toLowerCase()))
  const toggle = async (u: J) => { try { await api(`/admin/users/${u.id}/status?is_active=${!u.is_active}`, undefined, 'PATCH'); await reload(); notify(`${u.full_name} ${u.is_active ? 'deactivated' : 'activated'}`) } catch (e) { notify(errMsg(e), 'error') } }
  const columns = [
    { key: 'full_name' as const, label: 'User', render: (u: J) => <span className="admin-user-cell"><Avatar name={u.full_name} size="sm" /><span><strong>{u.full_name}</strong><small>{u.email}</small></span></span> },
    { key: 'role' as const, label: 'Role', render: (u: J) => <Badge tone={u.role === 'admin' ? 'violet' : 'neutral'}>{u.role}</Badge> },
    { key: 'created_at' as const, label: 'Joined', render: (u: J) => <>{fmt(u.created_at)}</> },
    { key: 'is_active' as const, label: 'Status', sortable: false, render: (u: J) => <button className={`status-toggle ${u.is_active ? 'on' : ''}`} role="switch" aria-checked={u.is_active} aria-label={`${u.is_active ? 'Deactivate' : 'Activate'} ${u.full_name}`} onClick={() => toggle(u)}><i /></button> },
  ]
  return <div className="admin-page animate-enter"><div className="page-heading"><div><div className="eyebrow">PEOPLE AND PERMISSIONS</div><h1>Users</h1><p>Manage access across SkillForge.</p></div></div>
    <div className="admin-user-stats"><Card><Users size={16} /><span><strong>{users.length}</strong><small>Total users</small></span></Card><Card><i className="active-status-dot" /><span><strong>{users.filter((u) => u.is_active).length}</strong><small>Active</small></span></Card><Card><ShieldCheck size={16} /><span><strong>{users.filter((u) => u.role === 'admin').length}</strong><small>Admins</small></span></Card></div>
    <Card className="admin-table-card"><div className="admin-table-heading"><div><h2>All users</h2><span>{filtered.length} people</span></div><div style={{ display: 'flex', gap: 8 }}><label className="inline-search"><Search size={14} /><input value={q} onChange={(e) => setQ(e.target.value)} placeholder="Search users" aria-label="Search users" /></label><select className="compact-select" value={role} onChange={(e) => setRole(e.target.value)} aria-label="Filter by role"><option>All roles</option><option value="student">student</option><option value="admin">admin</option></select></div></div><DataTable rows={filtered.map((u) => ({ ...u }))} columns={columns} pageSize={8} /></Card></div>
}

export function AdminAnalyticsPage() {
  const { data, error } = useLoad<Record<'stats' | 'progress' | 'courses', J>>({ stats: ['/admin/dashboard/stats', null], progress: ['/admin/learning-progress', null], courses: ['/courses', []] })
  if (error) return <Denied msg={error} />
  if (!data) return <Loading />
  const { stats, progress, courses } = data; const recs: J[] = progress?.records ?? []
  const mix = [{ name: 'Completed', value: progress?.completed_courses ?? 0, color: '#10b981' }, { name: 'In progress', value: progress?.in_progress_courses ?? 0, color: '#6257e4' }]
  const total = mix.reduce((s, m) => s + m.value, 0)
  const perCourse = courses.map((c: J) => { const r = recs.filter((x) => x.course_id === c.id); return { name: c.title, learners: r.length, avg: r.length ? Math.round(r.reduce((s, x) => s + x.progress_percentage, 0) / r.length) : 0 } })
  return <div className="admin-page animate-enter"><div className="page-heading"><div><div className="eyebrow">MEASURE WHAT MATTERS</div><h1>Learning analytics</h1><p>See where people are making progress and where the platform can help more.</p></div></div>
    <div className="admin-kpi-grid"><StatCard label="Progress records" value={String(progress?.total_progress_records ?? 0)} icon={<Clock3 size={18} />} tone="primary" /><StatCard label="Avg. course progress" value={`${Math.round(progress?.average_progress_percentage ?? 0)}%`} icon={<Activity size={18} />} tone="violet" /><StatCard label="Completed courses" value={String(progress?.completed_courses ?? 0)} icon={<CheckCircle2 size={18} />} tone="green" /><StatCard label="Active users" value={`${stats?.active_users ?? 0}/${stats?.total_users ?? 0}`} icon={<Users size={18} />} tone="amber" /></div>
    <div className="analytics-chart-grid"><Card className="admin-chart-card"><div className="card-heading"><div><div className="eyebrow">COURSE PERFORMANCE</div><h2>Learners and progress by course</h2></div></div>{perCourse.length ? <div className="analytics-area-chart"><ResponsiveContainer width="100%" height="100%"><BarChart data={perCourse} margin={{ top: 12, right: 5, bottom: 0, left: -20 }}><CartesianGrid vertical={false} stroke="var(--border)" strokeDasharray="3 5" /><XAxis dataKey="name" axisLine={false} tickLine={false} tick={{ fill: '#8791a4', fontSize: 12 }} /><YAxis axisLine={false} tickLine={false} tick={{ fill: '#8791a4', fontSize: 12 }} /><Tooltip cursor={{ fill: 'rgba(98,87,228,0.06)' }} contentStyle={TIP} /><Bar dataKey="learners" name="Learners" fill="#6257e4" radius={[5, 5, 0, 0]} barSize={22} /><Bar dataKey="avg" name="Avg progress %" fill="#f5b13d" radius={[5, 5, 0, 0]} barSize={22} /></BarChart></ResponsiveContainer></div> : <EmptyState icon={<BookOpen size={16} />} title="No data yet" description="Charts appear once learners start courses." />}</Card>
      <Card className="completion-mix-card"><div className="eyebrow">COURSE PROGRESS</div><h2>Learning status mix</h2>{total ? <><div className="completion-donut"><ResponsiveContainer width="100%" height="100%"><PieChart><Pie data={mix} dataKey="value" nameKey="name" innerRadius={56} outerRadius={77} paddingAngle={3} stroke="none">{mix.map((m) => <Cell key={m.name} fill={m.color} />)}</Pie><Tooltip cursor={{ fill: 'rgba(98,87,228,0.06)' }} contentStyle={TIP} /></PieChart></ResponsiveContainer><div><strong>{Math.round(progress?.average_progress_percentage ?? 0)}%</strong><span>avg. progress</span></div></div><div className="completion-legend">{mix.map((m) => <div key={m.name}><span><i style={{ background: m.color }} />{m.name}</span><strong>{m.value}</strong></div>)}</div></> : <p>No progress recorded yet.</p>}</Card></div></div>
}

export function AdminReviewsPage() {
  const notify = useToast(); const { data, error, reload } = useLoad<Record<'subs' | 'users' | 'projects', J>>({ subs: ['/admin/project-submissions', null], users: ['/admin/users', []], projects: ['/projects', []] })
  const [selected, setSelected] = useState<J>(null); const [score, setScore] = useState(85); const [feedback, setFeedback] = useState(''); const [status, setStatus] = useState('approved'); const [busy, setBusy] = useState(false); const [showAll, setShowAll] = useState(false)
  if (error) return <Denied msg={error} />
  if (!data) return <Loading />
  const uname = (id: number) => data.users.find((u: J) => u.id === id)?.full_name ?? `User ${id}`
  const ptitle = (id: number) => data.projects.find((p: J) => p.id === id)?.title ?? `Project ${id}`
  const all: J[] = data.subs?.submissions ?? []
  const list = showAll ? all : all.filter((s) => ['submitted', 'pending'].includes(String(s.status).toLowerCase()))
  const submit = async (e: FormEvent<HTMLFormElement>) => { e.preventDefault(); setBusy(true); try { await api(`/project-submissions/${selected.id}/review`, { status, score, feedback }, 'PUT'); notify('Review submitted. Learner will be notified.'); setSelected(null); setFeedback(''); setScore(85); await reload() } catch (err) { notify(errMsg(err), 'error') } finally { setBusy(false) } }
  return <div className="admin-page animate-enter"><div className="page-heading"><div><div className="eyebrow">LEARNER WORK, EXPERT EYES</div><h1>Project review queue</h1><p>Give learners clear, specific feedback they can use in their next iteration.</p></div><div style={{ display: 'flex', gap: 8, alignItems: 'center' }}><Badge tone="warning"><Clock3 size={12} /> {data.subs?.pending_reviews ?? 0} awaiting review</Badge><Button variant="outline" size="sm" onClick={() => setShowAll((v) => !v)}>{showAll ? 'Show pending only' : 'Show all submissions'}</Button></div></div>
    {list.length ? <div className="review-queue-list">{list.map((s, i) => <Card className="review-queue-card" key={s.id}><div className="review-queue-number">{String(i + 1).padStart(2, '0')}</div><Avatar name={uname(s.user_id)} size="md" /><div className="review-queue-main"><div><Badge tone={s.status === 'approved' ? 'success' : s.status === 'rejected' ? 'danger' : 'primary'}>{String(s.status).replace('_', ' ')}</Badge><span>Submitted {fmt(s.submitted_at)}</span></div><h2>{ptitle(s.project_id)}</h2><p>{uname(s.user_id)}{s.score != null && ` · Score ${s.score}`}</p></div><Button variant="outline" onClick={() => { setSelected(s); setScore(s.score ?? 85); setFeedback(s.feedback ?? ''); setStatus(s.status === 'rejected' || s.status === 'revision_required' ? s.status : 'approved') }}>{['submitted', 'pending'].includes(String(s.status).toLowerCase()) ? 'Review submission' : 'Update review'} <ArrowRight size={14} /></Button></Card>)}</div> : <EmptyState icon={<CheckCircle2 size={18} />} title="Your review queue is clear" description="New project submissions will appear here when learners are ready for feedback." />}
    <Modal open={!!selected} onClose={() => setSelected(null)} title="Review project submission" size="lg">{selected && <form className="review-modal-content" onSubmit={submit}><div className="review-modal-learner"><Avatar name={uname(selected.user_id)} /><div><strong>{uname(selected.user_id)}</strong><span>{ptitle(selected.project_id)} · Submitted {fmt(selected.submitted_at)}</span></div><Badge tone="warning">{String(selected.status).toUpperCase().replace('_', ' ')}</Badge></div>
      <div className="review-submission-preview"><div className="submission-preview-art"><FileText size={25} /><span>SUBMISSION</span></div><div><h3>{ptitle(selected.project_id)}</h3><p>{selected.description || 'No notes provided.'}</p>{selected.repository_url && <a className="text-link" href={selected.repository_url} target="_blank" rel="noreferrer">Repository <ArrowUpRight size={13} /></a>}{selected.demo_url && <> · <a className="text-link" href={selected.demo_url} target="_blank" rel="noreferrer">Live demo <ArrowUpRight size={13} /></a></>}</div></div>
      <Select label="Decision" value={status} onChange={(e) => setStatus(e.target.value)}><option value="approved">Approve</option><option value="revision_required">Request revision</option><option value="rejected">Reject</option></Select>
      <label className="review-score-control"><span>Project score <strong>{score}/100</strong></span><input type="range" min="0" max="100" value={score} onChange={(e) => setScore(Number(e.target.value))} /><span className="score-scale"><small>Needs more work</small><small>Exceptional</small></span></label>
      <Textarea label="Feedback for the learner" value={feedback} onChange={(e) => setFeedback(e.target.value)} placeholder="Call out one thing they did well and one specific next step…" rows={5} required />
      <div className="modal-actions"><Button variant="ghost" type="button" onClick={() => setSelected(null)}>Cancel</Button><Button type="submit" loading={busy} disabled={!feedback.trim()}>Send review <Check size={14} /></Button></div></form>}</Modal></div>
}

export function AdminCertificatesPage() {
  const notify = useToast(); const { data, error, reload } = useLoad<Record<'certs' | 'users', J>>({ certs: ['/certifications/', []], users: ['/admin/users', []] })
  const [target, setTarget] = useState<J>(null); const [issue, setIssue] = useState(false); const [busy, setBusy] = useState(false)
  if (error) return <Denied msg={error} />
  if (!data) return <Loading />
  const certs: J[] = data.certs; const users: J[] = data.users; const uname = (id: number) => users.find((u) => u.id === id)?.full_name ?? `User ${id}`
  const rows = certs.map((c) => ({ ...c, holder: uname(c.user_id), status: c.is_revoked ? 'Revoked' : 'Active' }))
  const revoke = async () => { try { await api(`/certifications/${target.id}/revoke`, undefined, 'PATCH'); notify(`${target.title} has been revoked`, 'error'); setTarget(null); await reload() } catch (e) { notify(errMsg(e), 'error') } }
  const create = async (e: FormEvent<HTMLFormElement>) => { e.preventDefault(); const f = new FormData(e.currentTarget); setBusy(true); try { await api('/certifications/', { user_id: Number(f.get('user_id')), title: String(f.get('title')), description: String(f.get('description') || '') || null }); notify('Certificate issued'); setIssue(false); await reload() } catch (err) { notify(errMsg(err), 'error') } finally { setBusy(false) } }
  const columns = [
    { key: 'title' as const, label: 'Certificate', render: (r: J) => <span className="admin-certificate-cell"><span><Award size={15} /></span><strong>{r.title}</strong></span> },
    { key: 'holder' as const, label: 'Issued to' },
    { key: 'issued_at' as const, label: 'Issued', render: (r: J) => <>{fmt(r.issued_at)}</> },
    { key: 'certificate_code' as const, label: 'Verification code' },
    { key: 'status' as const, label: 'Status', render: (r: J) => <Badge tone={r.status === 'Active' ? 'success' : 'danger'}>{r.status}</Badge> },
    { key: 'id' as const, label: 'Actions', sortable: false, render: (r: J) => r.status === 'Active' ? <button className="revoke-link" onClick={() => setTarget(r)}>Revoke</button> : <span className="revoked-label">Revoked</span> },
  ]
  return <div className="admin-page animate-enter"><div className="page-heading"><div><div className="eyebrow">CREDENTIAL INTEGRITY</div><h1>Certificate management</h1><p>Review issued credentials and protect the integrity of every achievement.</p></div><Button icon={<Award size={15} />} onClick={() => setIssue(true)}>Issue certificate</Button></div>
    <div className="certificate-admin-stats"><Card><Award size={17} /><div><strong>{rows.filter((r) => r.status === 'Active').length}</strong><span>Active certificates</span></div></Card><Card><ShieldCheck size={17} /><div><strong>{rows.filter((r) => r.status === 'Revoked').length}</strong><span>Revoked</span></div></Card><Card><Activity size={17} /><div><strong>{rows.length}</strong><span>Total issued</span></div></Card></div>
    <Card className="admin-table-card"><div className="admin-table-heading"><div><h2>Issued credentials</h2><span>Search and filter certificate records</span></div></div><DataTable rows={rows} columns={columns} pageSize={8} /></Card>
    <Modal open={!!target} onClose={() => setTarget(null)} title="Revoke certificate" size="sm">{target && <div className="revoke-confirm"><span><X size={20} /></span><h3>Revoke this credential?</h3><p><strong>{target.title}</strong> issued to {uname(target.user_id)} will no longer verify as active.</p><div className="modal-actions"><Button variant="ghost" onClick={() => setTarget(null)}>Keep certificate</Button><Button variant="danger" onClick={revoke}>Revoke credential</Button></div></div>}</Modal>
    <Modal open={issue} onClose={() => setIssue(false)} title="Issue certificate" size="sm"><form className="modal-form" onSubmit={create}><Select label="Learner" name="user_id" required defaultValue=""><option value="" disabled>Select a user</option>{users.map((u) => <option key={u.id} value={u.id}>{u.full_name} ({u.email})</option>)}</Select><Input label="Title" name="title" required minLength={2} maxLength={200} placeholder="e.g. Frontend Foundations" /><Textarea label="Description" name="description" rows={3} /><div className="modal-actions"><Button variant="ghost" type="button" onClick={() => setIssue(false)}>Cancel</Button><Button type="submit" loading={busy}>Issue <Check size={14} /></Button></div></form></Modal></div>
}

const contentTypes = ['Course', 'Module', 'Lesson', 'Career', 'Skill', 'Career skill', 'Project'] as const
type CT = (typeof contentTypes)[number]
export function ContentStudioPage() {
  const notify = useToast(); const { data, error, reload } = useLoad<Record<'courses' | 'careers' | 'skills' | 'projects', J[]>>({ courses: ['/courses', []], careers: ['/careers', []], skills: ['/skills', []], projects: ['/projects', []] })
  const [type, setType] = useState<CT>('Course'); const [search, setSearch] = useState(''); const [busy, setBusy] = useState(false); const [saved, setSaved] = useState(false)
  const [courseId, setCourseId] = useState(''); const [modules, setModules] = useState<J[]>([])
  useEffect(() => { if (type === 'Lesson' && courseId) api(`/courses/${courseId}/modules`).then(setModules).catch(() => setModules([])) }, [type, courseId])
  const items = useMemo(() => {
    if (!data) return [] as string[]
    const src = type === 'Course' ? data.courses : type === 'Career' || type === 'Career skill' ? data.careers : type === 'Skill' ? data.skills : type === 'Project' ? data.projects : data.courses
    return src.map((x: J) => x.title ?? x.name).filter((t: string) => t.toLowerCase().includes(search.toLowerCase()))
  }, [data, type, search])
  if (error) return <Denied msg={error} />
  if (!data) return <Loading />
  const num = (f: FormData, k: string) => Number(f.get(k))
  const submit = async (event: FormEvent<HTMLFormElement>) => {
    event.preventDefault(); const form = event.currentTarget; const f = new FormData(form); const s = (k: string) => String(f.get(k) ?? '').trim()
    setBusy(true)
    try {
      if (type === 'Course') await api('/courses', { title: s('title'), description: s('description') || null, skill_id: s('skill_id') ? num(f, 'skill_id') : null, level: s('level'), duration_hours: num(f, 'duration') })
      else if (type === 'Module') await api(`/courses/${s('course_id')}/modules`, { title: s('title'), description: s('description') || null, order_index: num(f, 'order') })
      else if (type === 'Lesson') await api(`/modules/${s('module_id')}/lessons`, { title: s('title'), content: s('description') || null, order_index: num(f, 'order'), duration_minutes: num(f, 'duration') })
      else if (type === 'Career') await api('/careers', { title: s('title'), description: s('description') || null })
      else if (type === 'Skill') await api('/skills', { name: s('title'), category: s('category'), description: s('description') || null })
      else if (type === 'Career skill') await api(`/careers/${s('career_id')}/skills`, { skill_id: num(f, 'skill_id'), weight: num(f, 'weight') })
      else await api('/projects', { title: s('title'), description: s('description'), difficulty: s('level'), required_skills: s('skills') || null, instructions: s('instructions') || null })
      form.reset(); setSaved(true); notify(`${type} saved`); await reload()
    } catch (e) { notify(errMsg(e), 'error') } finally { setBusy(false) }
  }
  const course = <Select label="Parent course" name="course_id" required defaultValue="" onChange={(e) => setCourseId(e.target.value)}><option value="" disabled>Select a course</option>{data.courses.map((c: J) => <option key={c.id} value={c.id}>{c.title}</option>)}</Select>
  const skillSel = (req: boolean) => <Select label="Skill" name="skill_id" required={req} defaultValue=""><option value="">{req ? 'Select a skill' : 'No specific skill'}</option>{data.skills.map((k: J) => <option key={k.id} value={k.id}>{k.name}</option>)}</Select>
  const levels = <Select label="Level" name="level" defaultValue="Beginner"><option>Beginner</option><option>Intermediate</option><option>Advanced</option></Select>
  const hasDescription = type !== 'Career skill'
  return <div className="admin-page animate-enter"><div className="page-heading"><div><div className="eyebrow">BUILD THE LEARNING EXPERIENCE</div><h1>Content studio</h1><p>Create and maintain the courses, skills, and career paths learners rely on.</p></div></div>
    <div className="content-studio-layout"><aside className="content-nav"><strong>CONTENT LIBRARY</strong>{contentTypes.map((t) => <button key={t} className={type === t ? 'selected' : ''} onClick={() => { setType(t); setSaved(false) }}>{t === 'Course' || t === 'Module' || t === 'Project' ? <BookOpen size={15} /> : t === 'Lesson' ? <FileText size={15} /> : t === 'Skill' || t === 'Career skill' ? <Sparkles size={15} /> : <Target size={15} />}{t}{t === 'Course' && <span>{data.courses.length}</span>}{t === 'Career' && <span>{data.careers.length}</span>}{t === 'Skill' && <span>{data.skills.length}</span>}{t === 'Project' && <span>{data.projects.length}</span>}</button>)}</aside>
      <main className="content-editor"><Card className="content-form-card"><div className="content-form-heading"><span className="content-edit-icon"><ClipboardCheck size={15} /></span><div><Badge tone="primary">NEW {type.toUpperCase()}</Badge><h2>Create {type === 'Career skill' ? 'a career skill requirement' : `a ${type.toLowerCase()}`}</h2><p>{type === 'Career skill' ? 'Link a skill to a career with an importance weight (1–100).' : 'Build a practical, well-structured learning experience.'}</p></div></div>
        <form className="content-form" key={type} onSubmit={submit}>
          {type === 'Module' && course}
          {type === 'Lesson' && <>{course}<Select label="Module" name="module_id" required defaultValue=""><option value="" disabled>{courseId ? 'Select a module' : 'Choose a course first'}</option>{modules.map((m) => <option key={m.id} value={m.id}>{m.title}</option>)}</Select></>}
          {type === 'Career skill' && <><Select label="Career" name="career_id" required defaultValue=""><option value="" disabled>Select a career</option>{data.careers.map((c: J) => <option key={c.id} value={c.id}>{c.title}</option>)}</Select>{skillSel(true)}<Input label="Weight (1–100)" name="weight" type="number" min={1} max={100} defaultValue={70} required /></>}
          {type !== 'Career skill' && <Input label={type === 'Skill' ? 'Skill name' : `${type} title`} name="title" required minLength={2} placeholder={`Name this ${type.toLowerCase()}`} />}
          {type === 'Course' && <><div className="content-form-row">{levels}<Input label="Duration (hours)" name="duration" type="number" min={0.5} step={0.5} defaultValue={4} required /></div>{skillSel(false)}</>}
          {type === 'Module' && <Input label="Order" name="order" type="number" min={1} defaultValue={1} required />}
          {type === 'Lesson' && <div className="content-form-row"><Input label="Order" name="order" type="number" min={1} defaultValue={1} required /><Input label="Duration (minutes)" name="duration" type="number" min={1} defaultValue={15} required /></div>}
          {type === 'Skill' && <Input label="Category" name="category" required minLength={2} placeholder="e.g. Engineering" />}
          {type === 'Project' && <><div className="content-form-row">{levels}<Input label="Required skills (comma separated)" name="skills" /></div></>}
          {hasDescription && <Textarea label={type === 'Lesson' ? 'Lesson content' : 'Description'} name="description" rows={type === 'Lesson' ? 8 : 4} required={type === 'Project'} placeholder={type === 'Lesson' ? 'Write the lesson text. Separate paragraphs with a blank line.' : 'Describe what learners will be able to do.'} />}
          {type === 'Project' && <Textarea label="Instructions / requirements (one per line)" name="instructions" rows={4} />}
          <div className="content-editor-footer"><span>{saved ? <><CheckCircle2 size={13} /> Saved</> : 'Saved content is immediately available to learners.'}</span><div><Button type="submit" loading={busy}>Save {type.toLowerCase()} <Check size={14} /></Button></div></div></form></Card>
        <Card className="content-list-card"><div className="card-heading"><div><h2>Existing {type === 'Career skill' ? 'careers' : `${type.toLowerCase()}s`}</h2><span>{items.length} in your library</span></div><label className="inline-search"><Search size={14} /><input value={search} onChange={(e) => setSearch(e.target.value)} placeholder="Find content" aria-label="Search content" /></label></div>{items.length ? <div className="content-recent-list">{items.map((t: string, i: number) => <div key={`${t}-${i}`}><span className="content-recent-icon"><FileText size={15} /></span><span><strong>{t}</strong></span><Badge tone="success">Live</Badge></div>)}</div> : <EmptyState icon={<Search size={16} />} title="Nothing here yet" description="Create your first one with the form." />}</Card></main></div></div>
}
