// Connects the SkillForge UI to the FastAPI backend.
// After login, loadLive() fetches real data and fills the same exported datasets the pages already read.
import { activity, appNotifications, assessments, careers, certificates, courses, learner, learnerStats, projects, skills, weeklyLearning } from './mockData'

const BASE = import.meta.env.VITE_API_URL || '/api'
// eslint-disable-next-line @typescript-eslint/no-explicit-any
type J = any

export const token = { get: () => localStorage.getItem('sf_token'), set: (t: string) => localStorage.setItem('sf_token', t), clear: () => localStorage.removeItem('sf_token') }
export const session = { role: 'student' }
export const catalog: { id: number; name: string; category: string }[] = []

export async function api(path: string, body?: unknown, method = body ? 'POST' : 'GET'): Promise<J> {
  const headers: Record<string, string> = {}
  if (token.get()) headers.Authorization = `Bearer ${token.get()}`
  if (body) headers['Content-Type'] = 'application/json'
  const res = await fetch(BASE + path, { method, headers, body: body ? JSON.stringify(body) : undefined })
  if (res.status === 401 && token.get()) { token.clear(); location.assign('/login') }
  if (!res.ok) {
    let msg = res.statusText
    try { const j = await res.json(); msg = typeof j.detail === 'string' ? j.detail : j.detail?.map((d: J) => d.msg).join('; ') || msg } catch { /* keep status text */ }
    throw new Error(msg)
  }
  return res.status === 204 ? null : res.json()
}

export async function apiForm(path: string, form: FormData): Promise<J> {
  const res = await fetch(BASE + path, { method: 'POST', headers: token.get() ? { Authorization: `Bearer ${token.get()}` } : {}, body: form })
  if (res.status === 401 && token.get()) { token.clear(); location.assign('/login') }
  if (!res.ok) {
    let msg = res.statusText
    try { const j = await res.json(); msg = typeof j.detail === 'string' ? j.detail : j.detail?.map((d: J) => d.msg).join('; ') || msg } catch { /* keep status text */ }
    throw new Error(msg)
  }
  return res.json()
}


export async function signIn(email: string, password: string) {
  const response = await api('/auth/login', { email, password })

  if (!response?.access_token) {
    throw new Error('Login failed: access token missing')
  }

  token.set(response.access_token)

  // Clear data belonging to the previous account.
  fill(skills, [])
  fill(careers, [])
  fill(courses, [])
  fill(assessments, [])
  fill(projects, [])
  fill(certificates, [])
  fill(appNotifications, [])
  fill(activity, [])
  fill(learnerStats, [])
  fill(weeklyLearning, [])
  fill(catalog, [])

  Object.assign(learner, {
    name: 'Learner',
    email: '',
    role: 'SkillForge learner',
    joined: '',
    streak: 0,
    hours: 0,
  })

  try {
    const me = await api('/users/me')

    session.role = me.role
    Object.assign(learner, {
      name: me.full_name,
      email: me.email,
      role: 'SkillForge learner',
      joined: me.created_at
        ? new Date(me.created_at).toLocaleDateString('en', {
            month: 'long',
            year: 'numeric',
          })
        : '',
    })

    void loadLive().catch((error) => {
      console.error('Dashboard data loading failed:', error)
    })
  } catch (error) {
    token.clear()
    throw error
  }
}
export async function signUp(full_name: string, email: string, password: string) {
  await api('/auth/register', { full_name, email, password })
  await signIn(email, password)
}
export const signOut = () => { token.clear(); location.assign('/login') }

const safe = <T,>(p: Promise<T>, fallback: T): Promise<T> => p.catch(() => fallback)
const fill = <T,>(target: T[], items: T[]) => { target.splice(0, target.length, ...items) }
const COLORS = ['violet', 'coral', 'blue', 'green', 'amber', 'rose']
const levelOf = (p: number): 'Foundational' | 'Developing' | 'Proficient' | 'Advanced' => (p >= 80 ? 'Advanced' : p >= 60 ? 'Proficient' : p >= 40 ? 'Developing' : 'Foundational')
const fmt = (d?: string) => (d ? new Date(d).toLocaleDateString('en', { month: 'short', day: 'numeric', year: 'numeric' }) : '')

export async function loadLive() {
  const me = await api('/users/me')
  const [rawCatalog, mine, cs, recs, dash, certs, notes, assess, attempts, projs, subs, prog, crs]: J[] = await Promise.all([
    safe(api('/skills'), []), safe(api('/users/me/skills'), []), safe(api('/careers'), []), safe(api('/recommendations/careers'), { recommendations: [] }),
    safe(api('/analytics/my-dashboard'), null), safe(api('/certifications/my'), []), safe(api('/notifications/my'), []), safe(api('/assessments'), []),
    safe(api('/assessments/attempts'), []), safe(api('/projects'), []), safe(api('/project-submissions/my'), []), safe(api('/courses/progress'), []), safe(api('/courses'), []),
  ])
  fill(catalog, rawCatalog.map((s: J) => ({ id: s.id, name: s.name, category: s.category })))
  const skillById = new Map<number, J>(rawCatalog.map((s: J) => [s.id, s]))
  const levelBySkill = new Map<number, number>(mine.map((u: J) => [u.skill_id, u.level]))
  const topCareer = recs.recommendations?.[0]?.career_title

  session.role = me.role
  Object.assign(learner, { name: me.full_name, email: me.email, role: topCareer ? `Aspiring ${topCareer.toLowerCase()}` : 'SkillForge learner', joined: new Date(me.created_at).toLocaleDateString('en', { month: 'long', year: 'numeric' }), streak: 0, hours: 0 })

  fill(skills, mine.map((u: J, i: number) => ({ id: String(u.id), name: skillById.get(u.skill_id)?.name ?? `Skill ${u.skill_id}`, category: skillById.get(u.skill_id)?.category ?? 'General', proficiency: u.level, level: levelOf(u.level), trend: 0, color: COLORS[i % COLORS.length] })))

  const careerSkills: J[] = await Promise.all(cs.map((c: J) => safe(api(`/careers/${c.id}/skills`), [])))
  fill(careers, cs.map((c: J, i: number) => ({ id: String(c.id), title: c.title, family: 'Career path', match: Math.round(recs.recommendations?.find((r: J) => r.career_id === c.id)?.match_score ?? 0), salary: '—', demand: 'Open path', description: c.description ?? '', skills: careerSkills[i].map((s: J) => ({ name: skillById.get(s.skill_id)?.name ?? `Skill ${s.skill_id}`, required: s.weight, current: levelBySkill.get(s.skill_id) ?? 0 })) })))

  const modules: J[] = await Promise.all(crs.map(async (c: J) => {
    const ms: J[] = await safe(api(`/courses/${c.id}/modules`), [])
    return Promise.all(ms.sort((a, b) => a.order_index - b.order_index).map(async (m) => ({ title: m.title, lessons: await safe(api(`/modules/${m.id}/lessons`), []) })))
  }))
  careers.sort((a, b) => b.match - a.match)
  fill(courses, crs.map((c: J, i: number) => {
    const p = Array.isArray(prog) ? prog.find((x: J) => x.course_id === c.id) : null
    let n = 0
    const mods = modules[i].map((m: J) => ({ title: m.title, lessons: m.lessons.sort((a: J, b: J) => a.order_index - b.order_index).map((l: J) => ({ id: String(l.id), title: l.title, duration: `${l.duration_minutes} min`, complete: n++ < (p?.completed_lessons ?? 0), type: 'reading' as const })) }))
    return { id: String(c.id), title: c.title, category: skillById.get(c.skill_id)?.name ?? 'Course', level: c.level, duration: `${c.duration_hours}h`, lessons: n || p?.total_lessons || 0, progress: Math.round(p?.progress_percentage ?? 0), rating: 0, color: COLORS[i % COLORS.length], description: c.description ?? '', skills: [], modules: mods }
  }))

  const counts: J[] = await Promise.all(assess.map((a: J) => safe(api(`/assessments/${a.id}/questions`), [])))
  fill(assessments, assess.map((a: J, i: number) => {
    const at = attempts.filter((x: J) => x.assessment_id === a.id).pop()
    const pct = at && at.status === 'submitted' ? Math.round((at.score / at.max_score) * 100) : undefined
    return { id: String(a.id), title: a.title, skill: 'General', questions: counts[i].length, duration: '—', score: pct, status: pct === undefined ? (at ? 'In progress' : 'Ready') : pct >= 70 ? 'Passed' : 'Needs practice', date: fmt(at?.submitted_at ?? a.created_at) } as (typeof assessments)[number]
  }))

  fill(projects, projs.map((p: J) => {
    const s = subs.find((x: J) => x.project_id === p.id)
    return { id: String(p.id), title: p.title, category: 'Project', level: p.difficulty, duration: '—', skills: p.required_skills ? p.required_skills.split(',').map((x: string) => x.trim()) : [], description: p.description, status: s ? (s.status === 'approved' ? 'Approved' : 'In review') : 'Available', score: s?.score ?? undefined } as (typeof projects)[number]
  }))
  fill(certificates, certs.filter((c: J) => !c.is_revoked).map((c: J) => ({ id: String(c.id), title: c.title, issuer: 'SkillForge', date: fmt(c.issued_at), code: c.certificate_code, skills: [] })))
  fill(appNotifications, notes.map((n: J) => ({ id: String(n.id), title: n.title, description: n.message, date: new Date(n.created_at).toLocaleTimeString('en', { hour: 'numeric', minute: '2-digit' }), group: new Date(n.created_at).toDateString() === new Date().toDateString() ? 'Today' : 'Earlier', unread: !n.is_read, kind: 'mentor' as const })))

  fill(learnerStats, [
    { label: 'Courses completed', value: String(dash?.courses.completed_courses ?? 0), change: `${dash?.courses.in_progress_courses ?? 0} in progress` },
    { label: 'Average score', value: `${Math.round(dash?.assessments.average_score ?? 0)}%`, change: `${dash?.assessments.total_attempts ?? 0} attempts` },
    { label: 'Projects shipped', value: String(dash?.projects.total_submissions ?? 0), change: `${dash?.projects.reviewed_submissions ?? 0} reviewed` },
    { label: 'Certificates', value: String(certs.length), change: '' },
  ])
  fill(weeklyLearning, weeklyLearning.map((d) => ({ ...d, hours: 0 })))
  const feed = [
    ...attempts.filter((a: J) => a.status === 'submitted').map((a: J) => ({ at: a.submitted_at, kind: 'assessment' as const, title: `Completed “${assess.find((x: J) => x.id === a.assessment_id)?.title ?? 'an assessment'}”`, detail: `Score ${Math.round((a.score / a.max_score) * 100)}%` })),
    ...subs.map((x: J) => ({ at: x.submitted_at, kind: 'course' as const, title: `Submitted “${projs.find((p: J) => p.id === x.project_id)?.title ?? 'a project'}”`, detail: String(x.status).replace('_', ' ') })),
    ...certs.filter((c: J) => !c.is_revoked).map((c: J) => ({ at: c.issued_at, kind: 'certificate' as const, title: `Earned “${c.title}”`, detail: 'Certificate issued' })),
  ].sort((a, b) => +new Date(b.at) - +new Date(a.at)).slice(0, 6)
  fill(activity, feed.map((f, i) => ({ id: `act-${i}`, title: f.title, detail: f.detail, time: fmt(f.at), kind: f.kind })) as unknown as typeof activity)
}
