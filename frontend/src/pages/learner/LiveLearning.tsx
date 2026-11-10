import { useEffect, useRef, useState, type ChangeEvent, type DragEvent, type FormEvent } from 'react'
import { Link, useLocation, useNavigate } from 'react-router-dom'
import { ArrowRight, Award, BookOpen, Check, CheckCircle2, ChevronLeft, ChevronRight, CircleHelp, Clock3, Code2, ExternalLink, FileText, GraduationCap, LockKeyhole, MoreHorizontal, Plus, Send, Sparkles, Target, Trash2, Upload, UserRound, WandSparkles, X, Flame } from 'lucide-react'
import { Badge, Button, Card, EmptyState, Input, Modal, Progress, Ring, Select, Skeleton, Textarea } from '../../components/ui'
import { useToast } from '../../components/toast-context'
import { api, apiForm, loadLive } from '../../data/live'
import { appNotifications, assessments, careers, courses, learner, projects, type AppNotification } from '../../data/mockData'

// eslint-disable-next-line @typescript-eslint/no-explicit-any
type J = any
const errMsg = (e: unknown) => (e instanceof Error ? e.message : 'Something went wrong')
const useRefresh = () => { const [, set] = useState(0); return () => set((n) => n + 1) }

/* ───────────── Lesson ───────────── */
export function LessonPage() {
  const { pathname } = useLocation(); const navigate = useNavigate(); const notify = useToast(); const refresh = useRefresh()
  const m = pathname.match(/\/app\/courses\/([^/]+)\/lesson\/?([^/]*)/)
  const course = courses.find((c) => c.id === m?.[1])
  const flat = course?.modules.flatMap((mod) => mod.lessons) ?? []
  const lessonId = m?.[2] || flat.find((l) => !l.complete)?.id || flat[0]?.id
  const index = flat.findIndex((l) => l.id === lessonId)
  const [lesson, setLesson] = useState<J>(null); const [resources, setResources] = useState<J[]>([]); const [quizzes, setQuizzes] = useState<J[]>([]); const [busy, setBusy] = useState(false)

  useEffect(() => {
    if (!lessonId) return
    let live = true
    setLesson(null)
    Promise.all([api(`/modules/lessons/${lessonId}`), api(`/lessons/${lessonId}/resources`).catch(() => []), api(`/lessons/${lessonId}/quizzes`).catch(() => [])])
      .then(([l, r, q]) => { if (live) { setLesson(l); setResources(r); setQuizzes(q) } })
      .catch((e) => notify(errMsg(e), 'error'))
    return () => { live = false }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [lessonId])

  if (!course || !lessonId) return <div className="learner-page"><EmptyState icon={<BookOpen size={18} />} title="Lesson not found" description="This course has no lessons yet." action={<Link className="ui-button ui-button-primary" to="/app/courses">Back to courses</Link>} /></div>

  const done = flat[index]?.complete
  const next = flat[index + 1]
  const complete = async () => {
    setBusy(true)
    try {
      const body = { completed_lessons: Math.max(index + 1, flat.filter((l) => l.complete).length) }
      await api(`/courses/${course.id}/progress`, { course_id: Number(course.id) }).catch(() => null)
      await api(`/courses/${course.id}/progress`, body, 'PUT')
      await loadLive(); refresh()
      notify('Lesson complete. Your progress has been updated.')
      navigate(next ? `/app/courses/${course.id}/lesson/${next.id}` : `/app/courses/${course.id}`)
    } catch (e) { notify(errMsg(e), 'error') } finally { setBusy(false) }
  }
  const paragraphs: string[] = (lesson?.content ?? '').split(/\n{2,}/).filter(Boolean)
  const modTitle = course.modules.find((mod) => mod.lessons.some((l) => l.id === lessonId))?.title

  return <div className="learner-page lesson-page animate-enter"><div className="lesson-breadcrumb"><Link to="/app/courses">Courses</Link><ChevronRight size={13} /><Link to={`/app/courses/${course.id}`}>{course.title}</Link><ChevronRight size={13} /><span>{lesson?.title ?? '…'}</span></div>
    <div className="lesson-workspace"><main className="lesson-content">
      {!lesson ? <><Skeleton /><Skeleton /><Skeleton /></> : <>
        <div className="lesson-kicker"><Badge tone="primary">{(modTitle ?? 'LESSON').toUpperCase()} · LESSON {index + 1}</Badge><span><Clock3 size={13} /> {lesson.duration_minutes} min</span></div>
        <h1>{lesson.title}</h1>
        <section className="lesson-reading">{paragraphs.length ? paragraphs.map((p, i) => <p key={i} className={i === 0 ? 'lesson-lead' : undefined}>{p}</p>) : <p>This lesson doesn’t have written content yet.</p>}</section>
        {quizzes.map((q) => <section className="lesson-panel" key={q.id}><div><div className="panel-icon violet-panel"><CircleHelp size={17} /></div><div><Badge tone="violet">QUIZ</Badge><h3>{q.title}</h3><p>{q.description || 'Check your understanding of this lesson.'} Passing score: {q.passing_score}%.</p></div></div></section>)}
      </>}
      <div className="lesson-navigation"><Link to={`/app/courses/${course.id}`} className="ui-button ui-button-outline"><ChevronLeft size={14} /> Course overview</Link><Button onClick={complete} loading={busy} disabled={!lesson}>{done ? (next ? 'Next lesson' : 'Finish') : 'Mark complete'} <Check size={14} /></Button></div>
    </main>
    <aside className="lesson-sidebar"><Card><div className="lesson-side-title"><span>COURSE LESSONS</span></div>{flat.map((l, i) => <Link key={l.id} to={`/app/courses/${course.id}/lesson/${l.id}`} className={`lesson-side-step ${l.complete ? 'complete' : ''}`}><span>{l.complete ? <Check size={12} /> : i + 1}</span>{l.title}</Link>)}<Progress value={course.progress} /><div className="lesson-side-progress">Course progress <strong>{course.progress}%</strong></div></Card>
      {resources.length > 0 && <Card className="lesson-resource-card"><strong>Resources</strong>{resources.map((r) => <a key={r.id} href={r.url} target="_blank" rel="noreferrer"><FileText size={14} /> {r.title} <ExternalLink size={12} /></a>)}</Card>}
      <Card className="ask-mentor-card"><div className="mentor-mini-icon"><WandSparkles size={17} /></div><strong>Have a question?</strong><p>Your AI mentor can help you work through the tricky bits.</p><Link to="/app/mentor">Ask your mentor <ChevronRight size={14} /></Link></Card></aside></div></div>
}

/* ───────────── Assessments ───────────── */
export function AssessmentsPage() {
  const notify = useToast(); const refresh = useRefresh(); const [filter, setFilter] = useState('All statuses'); const [open, setOpen] = useState(false); const [busy, setBusy] = useState(false)
  const list = assessments.filter((a) => filter === 'All statuses' || a.status === filter)
  const scored = assessments.filter((a) => a.score !== undefined)
  const avg = scored.length ? Math.round(scored.reduce((s, a) => s + (a.score ?? 0), 0) / scored.length) : 0
  const count = (s: string) => assessments.filter((a) => a.status === s).length

  const create = async (event: FormEvent<HTMLFormElement>) => {
    event.preventDefault(); const f = new FormData(event.currentTarget)
    const topic = String(f.get('topic')).trim(); const difficulty = String(f.get('difficulty')); const n = Number(f.get('count'))
    setBusy(true)
    try {
      const gen = await api(`/ai/generate-questions?topic=${encodeURIComponent(topic)}&difficulty=${difficulty}&number_of_questions=${n}`)
      const a = await api('/assessments', { title: `${topic} · ${difficulty}`, description: `AI-generated ${difficulty} assessment on ${topic}`, max_score: gen.questions.length })
      for (const q of gen.questions) await api(`/assessments/${a.id}/questions`, { question_text: q.question, question_type: 'mcq', option_a: q.options.A, option_b: q.options.B, option_c: q.options.C, option_d: q.options.D, correct_answer: q.correct_answer, marks: 1 })
      await loadLive(); refresh(); setOpen(false); notify('Your assessment is ready.')
    } catch (e) { notify(errMsg(e), 'error') } finally { setBusy(false) }
  }

  return <div className="learner-page animate-enter"><div className="page-heading"><div><div className="eyebrow">PUT YOUR SKILLS TO THE TEST</div><h1>Assessments</h1><p>Short, practical checks that help you understand what you know and what to practice next.</p></div><div className="assessment-overview"><Ring value={avg} size={55} stroke={5} label={`${avg}%`} /><span><strong>Average score</strong><small>across {scored.length} assessments</small></span></div></div>
    <div className="assessment-summary-grid"><Card><span className="assessment-summary-icon green-summary"><CheckCircle2 size={17} /></span><div><strong>{count('Passed')}</strong><small>Passed</small></div></Card><Card><span className="assessment-summary-icon amber-summary"><Clock3 size={17} /></span><div><strong>{count('In progress')}</strong><small>In progress</small></div></Card><Card><span className="assessment-summary-icon violet-summary"><Target size={17} /></span><div><strong>{count('Ready')}</strong><small>Available</small></div></Card></div>
    <Card className="assessments-table-card"><div className="card-heading"><div><h2>Your assessments</h2><span>Review results or continue where you left off</span></div><div style={{ display: 'flex', gap: 8 }}><select className="compact-select" aria-label="Filter assessments" value={filter} onChange={(e) => setFilter(e.target.value)}><option>All statuses</option><option>Ready</option><option>Passed</option><option>Needs practice</option><option>In progress</option></select><Button size="sm" icon={<Sparkles size={14} />} onClick={() => setOpen(true)}>Generate with AI</Button></div></div>
      {list.length === 0 ? <EmptyState icon={<Target size={18} />} title="No assessments yet" description="Generate a practice assessment on any topic and take it right away." action={<Button onClick={() => setOpen(true)}>Generate assessment</Button>} /> :
        <div className="assessment-list">{list.map((a) => <div className="assessment-row" key={a.id}><span className={`assessment-row-icon assessment-${a.status.replace(/\s+/g, '-').toLowerCase()}`}><Target size={17} /></span><div className="assessment-info"><strong>{a.title}</strong><span>{a.questions} questions</span></div><Badge tone={a.status === 'Passed' ? 'success' : a.status === 'In progress' ? 'warning' : a.status === 'Needs practice' ? 'danger' : 'neutral'}>{a.status}</Badge><span className="assessment-score">{a.score !== undefined ? `${a.score}%` : a.date}</span>
          {a.score !== undefined && <Link className="ui-button ui-button-ghost ui-button-sm" to={`/app/assessments/${a.id}/results`}>Review result <ChevronRight size={13} /></Link>}
          {a.score === undefined || a.status === 'Needs practice' ? <Link className="ui-button ui-button-outline ui-button-sm" to={`/app/assessments/${a.id}/take`}>{a.status === 'In progress' ? 'Continue' : a.status === 'Needs practice' ? 'Retake' : 'Start'} <ArrowRight size={13} /></Link> : null}</div>)}</div>}
    </Card>
    <Modal open={open} onClose={() => !busy && setOpen(false)} title="Generate an assessment" size="sm"><form className="project-form" onSubmit={create}><Input label="Topic" name="topic" placeholder="e.g. Python basics, REST APIs" required maxLength={200} /><Select label="Difficulty" name="difficulty" defaultValue="medium"><option value="easy">Easy</option><option value="medium">Medium</option><option value="hard">Hard</option></Select><Input label="Number of questions" name="count" type="number" min={1} max={20} defaultValue={5} required /><Button type="submit" loading={busy}>{busy ? 'Generating…' : 'Create assessment'} <Sparkles size={14} /></Button></form></Modal>
  </div>
}

export function AssessmentFlowPage() {
  const { pathname } = useLocation(); const id = pathname.match(/assessments\/([^/]+)\/take/)?.[1]; const navigate = useNavigate(); const notify = useToast()
  const [qs, setQs] = useState<J[] | null>(null); const [attempt, setAttempt] = useState<J>(null); const [saved, setSaved] = useState<Record<number, string>>({}); const [answers, setAnswers] = useState<Record<number, string>>({})
  const [step, setStep] = useState(0); const [review, setReview] = useState(false); const [busy, setBusy] = useState(false); const title = assessments.find((a) => a.id === id)?.title ?? 'Assessment'

  useEffect(() => {
    let live = true
    ;(async () => {
      try {
        const [questions, at] = await Promise.all([api(`/assessments/${id}/questions`), api(`/assessments/${id}/attempt`, { assessment_id: Number(id) })])
        const prev: J[] = await api(`/assessments/attempts/${at.id}/answers`).catch(() => [])
        if (!live) return
        const map = Object.fromEntries(prev.map((p) => [p.question_id, p.selected_answer]))
        setQs(questions.filter((q: J) => q.is_active)); setAttempt(at); setSaved(map); setAnswers(map)
      } catch (e) { if (live) { notify(errMsg(e), 'error'); navigate('/app/assessments') } }
    })()
    return () => { live = false }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [id])

  if (!qs) return <div className="assessment-flow-page"><Skeleton /><Skeleton /><Skeleton /></div>
  if (qs.length === 0) return <div className="assessment-flow-page"><EmptyState icon={<Target size={18} />} title="No questions yet" description="This assessment doesn’t have any questions." action={<Link className="ui-button ui-button-primary" to="/app/assessments">Back to assessments</Link>} /></div>

  const q = qs[step]; const answered = Object.keys(answers).length
  const options = (['A', 'B', 'C', 'D'] as const).map((k) => ({ key: k, text: q[`option_${k.toLowerCase()}`] as string | null })).filter((o) => o.text)
  const submit = async () => {
    setBusy(true)
    try {
      for (const [qid, ans] of Object.entries(answers)) if (saved[Number(qid)] === undefined) await api(`/assessments/attempts/${attempt.id}/answers`, { question_id: Number(qid), selected_answer: ans })
      await api(`/assessments/attempts/${attempt.id}/submit`, {})
      await loadLive(); navigate(`/app/assessments/${id}/results`)
    } catch (e) { notify(errMsg(e), 'error') } finally { setBusy(false) }
  }
  const locked = (qid: number) => saved[qid] !== undefined
  return <div className="assessment-flow-page animate-enter"><div className="assessment-flow-header"><Link to="/app/assessments" className="back-link"><ChevronLeft size={14} /> Exit assessment</Link></div>
    <div className="assessment-flow-title"><Badge tone="primary">{title.toUpperCase()}</Badge><h1>{review ? 'Review your answers' : 'Show what you know'}</h1><p>{review ? 'Take a final look before submitting your assessment.' : 'One question at a time. Take a breath and trust your practice.'}</p></div>
    <div className="assessment-progress-line"><div><span>Question {step + 1} of {qs.length}</span><strong>{Math.round(((step + 1) / qs.length) * 100)}%</strong></div><Progress value={((step + 1) / qs.length) * 100} /></div>
    <div className="assessment-take-layout"><aside className="question-nav"><strong>QUESTION MAP</strong><div>{qs.map((item, i) => <button key={item.id} className={`${step === i ? 'current' : ''} ${answers[item.id] ? 'answered' : ''}`} onClick={() => { setStep(i); setReview(false) }}>{answers[item.id] ? <Check size={13} /> : i + 1}</button>)}</div><p>{answered} of {qs.length} answered</p><span className="question-nav-legend"><i /> Current <i /> Answered</span></aside>
      <Card className="question-card"><div className="question-meta"><span>{q.question_type.toUpperCase()}</span><span>QUESTION {step + 1}</span></div><h2>{q.question_text}</h2>
        <div className="answer-options">{options.map((o) => <button key={o.key} disabled={locked(q.id)} className={`answer-option ${answers[q.id] === o.key ? 'selected' : ''}`} onClick={() => setAnswers((a) => ({ ...a, [q.id]: o.key }))}><span>{o.key}</span>{o.text}{answers[q.id] === o.key && <CheckCircle2 size={17} />}</button>)}</div>
        <div className="question-card-footer"><Button variant="ghost" disabled={step === 0} onClick={() => { setStep((v) => v - 1); setReview(false) }}><ChevronLeft size={15} /> Previous</Button>
          {step < qs.length - 1 ? <Button onClick={() => setStep((v) => v + 1)}>Next question <ChevronRight size={15} /></Button> : review ? <Button loading={busy} disabled={answered === 0} onClick={submit}>Submit assessment <Check size={15} /></Button> : <Button variant="outline" onClick={() => setReview(true)}>Review answers <ChevronRight size={14} /></Button>}</div></Card></div></div>
}

export function AssessmentResultsPage() {
  const { pathname } = useLocation(); const id = pathname.match(/assessments\/([^/]+)\/results/)?.[1]; const navigate = useNavigate(); const notify = useToast()
  const [data, setData] = useState<{ attempt: J; rows: { q: J; a: J }[] } | null>(null)
  useEffect(() => {
    let live = true
    ;(async () => {
      try {
        const attempts: J[] = await api('/assessments/attempts')
        const attempt = attempts.filter((a) => String(a.assessment_id) === id && a.status === 'submitted').pop()
        if (!attempt) throw new Error('No submitted attempt found for this assessment')
        const [answers, questions]: [J[], J[]] = await Promise.all([api(`/assessments/attempts/${attempt.id}/answers`), api(`/assessments/${id}/questions`)])
        if (live) setData({ attempt, rows: questions.map((q) => ({ q, a: answers.find((x) => x.question_id === q.id) })) })
      } catch (e) { if (live) { notify(errMsg(e), 'error'); navigate('/app/assessments') } }
    })()
    return () => { live = false }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [id])
  if (!data) return <div className="learner-page"><Skeleton /><Skeleton /></div>
  const { attempt, rows } = data; const score = Math.round((attempt.score / attempt.max_score) * 100); const pass = score >= 70; const title = assessments.find((a) => a.id === id)?.title ?? 'Your assessment'
  const correct = rows.filter((r) => r.a?.is_correct).length
  return <div className="learner-page results-page animate-enter"><div className="results-celebration"><span><Award size={23} /></span><Badge tone="success">ASSESSMENT COMPLETE</Badge><h1>{pass ? 'You passed. Nicely done.' : 'Good work getting started.'}</h1><p>{title} · results are ready.</p><div className="results-score"><Ring value={score} size={143} stroke={11} color={pass ? 'success' : 'amber'} label={`${score}%`} sublabel="YOUR SCORE" /><div><Badge tone={pass ? 'success' : 'warning'}>{pass ? 'PASSING SCORE' : 'KEEP PRACTICING'}</Badge><strong>{pass ? `Strong work, ${learner.name.split(' ')[0]}.` : 'You are building useful knowledge.'}</strong><small>{correct} of {rows.length} correct · {attempt.score}/{attempt.max_score} points</small></div></div></div>
    <div className="results-grid"><Card className="result-breakdown"><div className="card-heading"><div><h2>Question breakdown</h2><span>See what you got right and what to revisit</span></div></div>{rows.map(({ q, a }, i) => { const ok = !!a?.is_correct; return <div className="result-skill-row" key={q.id}><div><span className={ok ? 'result-check correct' : 'result-check needs-work'}>{ok ? <Check size={12} /> : <Target size={12} />}</span><strong>{i + 1}. {q.question_text}</strong><Badge tone={ok ? 'success' : 'warning'}>{ok ? 'Correct' : a ? 'Practice' : 'Skipped'}</Badge></div><small>Your answer: {a?.selected_answer ?? '—'}{!ok && <> · Correct: {q.correct_answer}</>}</small></div> })}</Card>
      <Card className="results-feedback"><div className="feedback-strength"><span><CheckCircle2 size={16} /></span><div><strong>Strengths</strong><p>{correct > 0 ? `You answered ${correct} question${correct === 1 ? '' : 's'} correctly.` : 'Every attempt gives you a clearer picture.'}</p></div></div><div className="feedback-focus"><span><Target size={16} /></span><div><strong>Next focus</strong><p>{rows.length - correct > 0 ? 'Review the questions marked Practice, then retake the assessment.' : 'Great — try a harder assessment next.'}</p></div></div><Link to="/app/courses" className="ui-button ui-button-primary">Practice your next skill <ChevronRight size={14} /></Link><Link className="results-back-link" to="/app/assessments">Back to assessments</Link></Card></div></div>
}

/* ───────────── Project detail ───────────── */
export function ProjectDetailPage() {
  const { pathname } = useLocation(); const id = pathname.match(/\/app\/projects\/([^/]+)/)?.[1]; const notify = useToast(); const refresh = useRefresh()
  const project = projects.find((p) => p.id === id)
  const [detail, setDetail] = useState<J>(null); const [sub, setSub] = useState<J>(null); const [checked, setChecked] = useState<string[]>([]); const [busy, setBusy] = useState(false)
  useEffect(() => {
    if (!id) return
    api(`/projects/${id}`).then(setDetail).catch(() => null)
    api('/project-submissions/my').then((s: J[]) => setSub(s.filter((x) => String(x.project_id) === id).pop() ?? null)).catch(() => null)
  }, [id])
  if (!project) return <div className="learner-page"><EmptyState icon={<Code2 size={18} />} title="Project not found" description="It may have been removed." action={<Link className="ui-button ui-button-primary" to="/app/projects">Back to projects</Link>} /></div>
  const requirements: string[] = (detail?.instructions ?? '').split('\n').map((x: string) => x.replace(/^[-*\d.\s]+/, '').trim()).filter(Boolean)
  const submitted = !!sub
  const onSubmit = async (event: FormEvent<HTMLFormElement>) => {
    event.preventDefault(); const f = new FormData(event.currentTarget); const repo = String(f.get('repo') ?? '').trim(); const demo = String(f.get('demo') ?? '').trim()
    setBusy(true)
    try {
      const s = await api('/project-submissions', { project_id: Number(id), repository_url: repo || null, demo_url: demo || null, description: String(f.get('description') ?? '') || null })
      setSub(s); await loadLive(); refresh(); notify('Project submitted for review. We’ll let you know when feedback is ready.')
    } catch (e) { notify(errMsg(e), 'error') } finally { setBusy(false) }
  }
  const tone = sub?.status === 'approved' ? 'success' : sub?.status === 'rejected' ? 'danger' : 'warning'
  return <div className="learner-page animate-enter"><Link to="/app/projects" className="back-link"><ChevronLeft size={14} /> Projects</Link><div className="project-detail-header"><div className="project-detail-art"><span><Code2 size={24} /></span><small>{project.category.toUpperCase()}</small></div><div><div className="project-card-tags"><Badge tone="primary">{project.level}</Badge></div><h1>{project.title}</h1><p>{project.description}</p><div className="course-skills">{project.skills.map((s) => <span key={s}>{s}</span>)}</div></div></div>
    <div className="project-detail-grid"><main>
      {requirements.length > 0 && <Card className="project-requirements"><div className="card-heading"><div><div className="eyebrow">YOUR CHECKLIST</div><h2>Project requirements</h2></div><Badge tone={checked.length === requirements.length ? 'success' : 'neutral'}>{checked.length}/{requirements.length} complete</Badge></div><p>Check off each requirement as your project takes shape.</p>{requirements.map((r) => <label className="requirement-row" key={r}><input type="checkbox" checked={checked.includes(r) || submitted} onChange={(e) => setChecked((items) => e.target.checked ? [...items, r] : items.filter((i) => i !== r))} /><span>{r}</span></label>)}</Card>}
      <Card className="project-submit-card"><div className="eyebrow">SHARE YOUR WORK</div><h2>{submitted ? 'Submission received' : 'Submit your project'}</h2>
        {submitted ? <div className="submission-confirm"><CheckCircle2 size={20} /><div><strong>Status: <Badge tone={tone}>{String(sub.status).replace('_', ' ')}</Badge>{sub.score != null && <> · Score {sub.score}/100</>}</strong><p>{sub.feedback || 'Your project is in the review queue. Feedback will appear here and in your notifications.'}</p>{sub.repository_url && <a href={sub.repository_url} target="_blank" rel="noreferrer">Repository <ExternalLink size={12} /></a>}</div></div>
          : <form className="project-form" onSubmit={onSubmit}><Input label="Repository URL" name="repo" type="url" placeholder="https://github.com/you/project" required /><Input label="Live demo URL" name="demo" type="url" placeholder="https://your-project.com" /><Textarea label="Project notes" name="description" placeholder="What did you learn? What decisions are you most proud of?" rows={4} required /><Button type="submit" loading={busy}>Submit for review <ArrowRight size={14} /></Button></form>}</Card></main>
      <aside className="project-review-aside"><Card><div className="reviewer-heading"><span><UserRound size={16} /></span><div><strong>Expert review</strong><small>Feedback from a reviewer</small></div></div><p>Your submission is reviewed against the brief and the skills you’re building.</p></Card><Card className="similar-project"><span className="similar-icon"><GraduationCap size={16} /></span><strong>Projects build evidence</strong><p>Approved work can be shared with your certificates and career profile.</p><Link to="/app/certificates">View credentials <ChevronRight size={14} /></Link></Card></aside></div></div>
}

/* ───────────── Resume ───────────── */
export function ResumePage() {
  const [file, setFile] = useState<File | null>(null); const [result, setResult] = useState<J>(null); const [busy, setBusy] = useState(false); const [dragging, setDragging] = useState(false); const inputRef = useRef<HTMLInputElement>(null); const notify = useToast()
  const pick = (f: File | undefined) => { if (!f) return; if (!/\.(pdf|docx)$/i.test(f.name)) return notify('Choose a PDF or DOCX resume.', 'error'); if (f.size > 5 * 1024 * 1024) return notify('Resume must be 5 MB or smaller.', 'error'); setFile(f); setResult(null) }
  const analyze = async () => { if (!file) return; setBusy(true); try { const fd = new FormData(); fd.append('file', file); setResult(await apiForm('/resume/upload', fd)); await loadLive() } catch (e) { notify(errMsg(e), 'error') } finally { setBusy(false) } }
  const top = result?.career_recommendations?.[0]
  return <div className="learner-page animate-enter"><div className="page-heading"><div><div className="eyebrow">MAKE YOUR EXPERIENCE COUNT</div><h1>Resume insights</h1><p>Turn your experience into a clear story of skills, impact, and potential.</p></div><Badge tone="violet"><Sparkles size={12} /> Skill detection</Badge></div>
    {!file ? <div className={`resume-upload-zone ${dragging ? 'dragging' : ''}`} onDragOver={(e: DragEvent) => { e.preventDefault(); setDragging(true) }} onDragLeave={() => setDragging(false)} onDrop={(e: DragEvent<HTMLDivElement>) => { e.preventDefault(); setDragging(false); pick(e.dataTransfer.files[0]) }}><input ref={inputRef} type="file" accept=".pdf,.docx" onChange={(e: ChangeEvent<HTMLInputElement>) => pick(e.target.files?.[0])} /><span className="resume-upload-icon"><Upload size={23} /></span><h2>Bring your experience into focus.</h2><p>Drop your resume here, or browse your files. We’ll detect the skills inside and match them to careers.</p><Button onClick={() => inputRef.current?.click()}>Choose a file <Upload size={14} /></Button><small>PDF or DOCX · Up to 5 MB · Your resume stays private</small></div>
      : <div className="resume-analysis"><div className="resume-file-row"><span><FileText size={17} /></span><div><strong>{file.name}</strong><small>{(file.size / 1024).toFixed(0)} KB · {result ? 'Analyzed' : 'Ready to analyze'}</small></div><button className="icon-button" aria-label="Remove resume" onClick={() => { setFile(null); setResult(null) }}><Trash2 size={15} /></button>{!result && <Button loading={busy} onClick={analyze}><Sparkles size={14} /> Analyze resume</Button>}</div>
        {result ? <><div className="resume-analysis-heading"><div><Badge tone="success"><CheckCircle2 size={12} /> ANALYSIS COMPLETE</Badge><h2>{result.detected_skill_count ? `We found ${result.detected_skill_count} skills.` : 'We couldn’t match any known skills.'}</h2>{top && <p>Your strongest career match is {top.career_title}.</p>}</div>{top && <Ring value={Math.round(top.match_score)} size={91} stroke={8} color="success" label={`${Math.round(top.match_score)}%`} sublabel="ROLE MATCH" />}</div>
          <div className="resume-analysis-grid"><Card><div className="card-heading"><div><h3>Skills we found</h3><span>Matched against the SkillForge catalog</span></div><Badge tone="success">{result.detected_skill_count} found</Badge></div><div className="extracted-skills">{result.detected_skills.map((s: J) => <span key={s.skill_id}><Check size={12} />{s.skill_name}</span>)}</div></Card>
            <Card><div className="card-heading"><div><h3>Career matches</h3><span>Based on your skills</span></div></div>{(result.career_recommendations ?? []).slice(0, 4).map((c: J, i: number) => <div className="resume-suggestion" key={c.career_id}><span>{String(i + 1).padStart(2, '0')}</span><p><strong>{c.career_title}</strong> · {Math.round(c.match_score)}% match</p></div>)}<Link to="/app/careers" className="ui-button ui-button-outline ui-button-sm">Explore careers</Link></Card></div><div className="resume-privacy"><LockKeyhole size={14} /> Your resume is private and visible only to you.</div></>
          : <div className="resume-waiting-state"><div className="resume-skeleton"><span /><span /><span /><span /></div><div><strong>Ready when you are</strong><p>We’ll extract skills from your resume and match them to career paths.</p></div></div>}</div>}</div>
}

/* ───────────── Mentor ───────────── */
type Msg = { id: string; role: 'assistant' | 'user'; content: string }
function renderMessage(content: string) { return content.split(/(\*\*[^*]+\*\*)/g).map((part, i) => part.startsWith('**') ? <strong key={i}>{part.slice(2, -2)}</strong> : part.split('\n').map((line, j, a) => <span key={`${i}-${j}`}>{line}{j < a.length - 1 && <br />}</span>)) }
export function MentorPage() {
  const first = learner.name.split(' ')[0]
  const [messages, setMessages] = useState<Msg[]>([{ id: 'welcome', role: 'assistant', content: `Hi ${first}. Ask me about your learning plan, skill gaps, or any project or career question.` }])
  const [value, setValue] = useState(''); const [typing, setTyping] = useState(false); const [contextOpen, setContextOpen] = useState(true); const [guide, setGuide] = useState<J>(null); const [guideBusy, setGuideBusy] = useState(false); const endRef = useRef<HTMLDivElement>(null); const notify = useToast()
  useEffect(() => { endRef.current?.scrollIntoView({ behavior: 'smooth', block: 'end' }) }, [messages, typing])
  const send = async (text = value) => {
    const q = text.trim(); if (!q || typing) return
    setMessages((m) => [...m, { id: `u${m.length}`, role: 'user', content: q }]); setValue(''); setTyping(true)
    try { const r = await api('/project-agent/ask', { question: q }); setMessages((m) => [...m, { id: `a${m.length}`, role: 'assistant', content: r.answer }]) }
    catch (e) { setMessages((m) => [...m, { id: `a${m.length}`, role: 'assistant', content: `I couldn’t answer that just now (${errMsg(e)}). Please try again.` }]) }
    finally { setTyping(false) }
  }
  const loadGuide = async () => { setGuideBusy(true); try { setGuide(await api('/ai-mentor/learning-guidance')) } catch (e) { notify(errMsg(e), 'error') } finally { setGuideBusy(false) } }
  const topCareer = careers[0]
  return <div className={`mentor-page animate-enter ${contextOpen ? '' : 'mentor-context-hidden'}`}><header className="mentor-header"><div className="mentor-title-icon"><WandSparkles size={18} /></div><div><strong>Your AI mentor</strong><span><i /> Here to help you move forward</span></div><div className="mentor-header-actions"><Badge tone="violet">PERSONALIZED TO YOU</Badge><button className="icon-button mentor-context-toggle" aria-label="Toggle learning guidance" onClick={() => setContextOpen((o) => !o)}><MoreHorizontal size={18} /></button></div></header>
    <div className="mentor-body"><main className="mentor-chat"><div className="mentor-chat-date">TODAY · {new Date().toLocaleDateString('en', { weekday: 'long', month: 'long', day: 'numeric' }).toUpperCase()}</div>
      {messages.map((m) => <div className={`chat-message ${m.role}`} key={m.id}><span className={m.role === 'assistant' ? 'chat-avatar ai-chat-avatar' : 'chat-avatar'}>{m.role === 'assistant' ? <Sparkles size={15} /> : first.slice(0, 2).toUpperCase()}</span><div className="chat-message-content"><div className="chat-message-name">{m.role === 'assistant' ? 'SkillForge mentor' : 'You'}</div><div className="chat-bubble">{renderMessage(m.content)}</div>{m.role === 'assistant' && m.id !== 'welcome' && <div className="chat-actions"><button onClick={() => navigator.clipboard?.writeText(m.content)}>Copy</button></div>}</div></div>)}
      {typing && <div className="chat-message assistant"><span className="chat-avatar ai-chat-avatar"><Sparkles size={15} /></span><div className="chat-message-content"><div className="chat-message-name">SkillForge mentor <small>thinking</small></div><div className="chat-bubble typing-bubble"><i /><i /><i /></div></div></div>}<div ref={endRef} /></main>
      <aside className="mentor-guidance"><div className="guidance-header"><div><div className="eyebrow">YOUR LEARNING CONTEXT</div><h2>In your corner</h2></div><button className="icon-button" aria-label="Close guidance panel" onClick={() => setContextOpen(false)}><X size={16} /></button></div>
        {topCareer && <Card className="mentor-goal-card"><span className="goal-icon"><Target size={16} /></span><div><small>TOP CAREER MATCH</small><strong>{topCareer.title}</strong><span>{topCareer.match}% current match</span></div><Link to={`/app/careers/${topCareer.id}`}><ChevronRight size={14} /></Link></Card>}
        <Card className="mentor-focus-card"><div className="eyebrow">PERSONAL LEARNING PLAN</div>{guide ? <><p style={{ whiteSpace: 'pre-wrap' }}>{guide.guidance}</p><small>{guide.summary.skill_gaps_found} skill gaps · {guide.summary.incomplete_courses} courses in progress · {guide.summary.weak_assessments} to retake</small></> : <><p>Get a plan based on your real skills, courses, and assessment results.</p><Button size="sm" loading={guideBusy} onClick={loadGuide}>Generate my plan <Sparkles size={13} /></Button></>}</Card>
        <Card className="mentor-streak-card"><Flame size={17} /><div><strong>Keep going</strong><span>Small steps are adding up.</span></div></Card></aside></div>
    <div className="mentor-composer-wrap"><div className="prompt-chips">{['What should I improve first?', 'Show my learning plan', 'Explain my skill gaps'].map((p) => <button key={p} onClick={() => send(p)}>{p}</button>)}</div>
      <div className="mentor-composer"><textarea value={value} onChange={(e) => setValue(e.target.value)} onKeyDown={(e) => { if (e.key === 'Enter' && !e.shiftKey) { e.preventDefault(); send() } }} placeholder="Ask about your learning, career, or next step…" rows={1} aria-label="Message your AI mentor" maxLength={2000} /><div className="composer-actions"><span>AI guidance grounded in your learning journey</span><div><button className="icon-button" aria-label="Attach" tabIndex={-1}><Plus size={17} /></button><button className="send-message" disabled={!value.trim() || typing} aria-label="Send message" onClick={() => send()}><Send size={15} /></button></div></div></div></div></div>
}

/* ───────────── Notifications ───────────── */
export function NotificationsPage() {
  const refresh = useRefresh(); const notify = useToast(); const items: AppNotification[] = appNotifications
  const reload = async () => { await loadLive(); refresh() }
  const markRead = async (id: string) => { try { await api(`/notifications/${id}/read`, { is_read: true }, 'PATCH'); await reload() } catch (e) { notify(errMsg(e), 'error') } }
  const markAll = async () => { try { await Promise.all(items.filter((i) => i.unread).map((i) => api(`/notifications/${i.id}/read`, { is_read: true }, 'PATCH'))); await reload() } catch (e) { notify(errMsg(e), 'error') } }
  const remove = async (id: string) => { try { await api(`/notifications/${id}`, undefined, 'DELETE'); await reload(); notify('Notification removed') } catch (e) { notify(errMsg(e), 'error') } }
  const unread = items.filter((i) => i.unread).length; const groups = [...new Set(items.map((i) => i.group))]
  return <div className="learner-page animate-enter"><div className="page-heading"><div><div className="eyebrow">YOUR LEARNING, IN THE LOOP</div><h1>Notifications {unread > 0 && <span className="unread-count">{unread}</span>}</h1><p>Updates about your learning, achievements, and next steps.</p></div><Button variant="outline" disabled={!unread} onClick={markAll}><Check size={14} /> Mark all as read</Button></div>
    <div className="notification-groups">{groups.map((g) => <section key={g}><div className="notification-group-title"><h2>{g}</h2><span>{items.filter((i) => i.group === g).length}</span></div><Card className="notification-group-card">{items.filter((i) => i.group === g).map((i) => <article className={`notification-item ${i.unread ? 'unread' : ''}`} key={i.id}><span className="notification-item-icon notification-mentor"><Award size={17} /></span><div className="notification-item-copy"><div><strong>{i.title}</strong>{i.unread && <i />}</div><p>{i.description}</p><time>{i.date}</time></div><div className="notification-actions">{i.unread && <button onClick={() => markRead(i.id)}>Mark read</button>}<button className="icon-button" aria-label={`Delete notification: ${i.title}`} onClick={() => remove(i.id)}><Trash2 size={14} /></button></div></article>)}</Card></section>)}</div>
    {items.length === 0 && <EmptyState icon={<CheckCircle2 size={18} />} title="You’re all caught up" description="New course updates and achievements will show up here." />}</div>
}

