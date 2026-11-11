import { useState, type FormEvent } from 'react'
import { Link, useNavigate } from 'react-router-dom'
import { api, session, signIn, signUp } from '../../data/live'
import { Area, AreaChart, ResponsiveContainer, Tooltip as ChartTooltip } from 'recharts'
import { ArrowRight, ArrowUpRight, BadgeCheck, BrainCircuit, CheckCircle2, CirclePlay, ClipboardCheck, Code2, Compass, FileBadge, GraduationCap, LockKeyhole, ShieldCheck, Sparkles, Target, TrendingUp, WandSparkles } from 'lucide-react'
import { Badge, Button, Input } from '../../components/ui'

const momentum = [{ score: 26 }, { score: 32 }, { score: 29 }, { score: 42 }, { score: 48 }, { score: 43 }, { score: 58 }, { score: 68 }, { score: 62 }, { score: 78 }, { score: 84 }]
const features = [
  { icon: Target, title: 'Find your skill gaps', copy: 'See exactly what your next role asks for, and where your strongest opportunities are.' },
  { icon: BrainCircuit, title: 'Learn with an AI mentor', copy: 'Get thoughtful guidance, project feedback, and a plan that adapts as you grow.' },
  { icon: ClipboardCheck, title: 'Prove what you know', copy: 'Practice with role-aligned assessments that measure skills, not just recall.' },
  { icon: FileBadge, title: 'Earn trusted credentials', copy: 'Turn completed learning into shareable certificates employers can verify.' },
]

export function LandingPage() {
  return <main className="landing-page">
    <section className="landing-hero">
      <div className="hero-copy animate-enter"><div className="hero-eyebrow"><span className="eyebrow-dot" /> THE CAREER GROWTH PLATFORM</div><h1>SkillForge for your <em>next chapter.</em></h1><p className="hero-subtitle">A clearer path from where you are to where you want to be. Build real skills, earn proof, and move forward with confidence.</p><div className="hero-actions"><Link to="/register" className="ui-button ui-button-primary ui-button-lg">Start building <ArrowRight size={17} /></Link><a href="#how-it-works" className="hero-watch"><span><CirclePlay size={19} /></span>See how it works</a></div><div className="hero-proof"><div className="proof-avatars"><span>AK</span><span>JM</span><span>RT</span><span>+</span></div><div><strong>Built around your goals</strong><small>Learning that leads somewhere.</small></div><span className="proof-divider" /><div className="proof-stars">â˜…â˜…â˜…â˜…â˜…<small>4.9 / learner rating</small></div></div></div>
      <div className="hero-visual animate-enter" aria-label="SkillForge learner dashboard preview"><div className="hero-orbit orbit-one" /><div className="hero-orbit orbit-two" /><div className="preview-window"><div className="preview-top"><div className="preview-brand"><span><GraduationCap size={14} /></span> skillforge</div><div className="preview-dots"><i /><i /><i /></div></div><div className="preview-body"><div className="preview-welcome"><div><small>MONDAY, OCTOBER 12</small><strong>Your next move is taking shape.</strong></div><span className="preview-avatar">JL</span></div><div className="preview-metrics"><div><span>Career readiness</span><strong>78<small>/100</small></strong><div className="mini-meter"><i /></div><small className="positive-change"><TrendingUp size={11} /> +12 this month</small></div><div className="preview-streak"><span><span className="streak-emoji">âœ¦</span> 12 day streak</span><b>You're on a roll.</b><div className="preview-days"><i /><i /><i /><i /><i /><i /><i /></div></div></div><div className="preview-chart-head"><div><small>YOUR LEARNING MOMENTUM</small><strong>Steady progress, real skills</strong></div><Badge tone="success">+18%</Badge></div><div className="preview-chart"><ResponsiveContainer width="100%" height="100%"><AreaChart data={momentum}><defs><linearGradient id="momentumFill" x1="0" y1="0" x2="0" y2="1"><stop offset="0%" stopColor="#4f46e5" stopOpacity={0.2} /><stop offset="100%" stopColor="#4f46e5" stopOpacity={0} /></linearGradient></defs><Area type="monotone" dataKey="score" stroke="#4f46e5" strokeWidth={2.5} fill="url(#momentumFill)" /><ChartTooltip contentStyle={{ borderRadius: 9, border: '1px solid #e2e8f0', fontSize: 13 }} /></AreaChart></ResponsiveContainer></div><div className="preview-course"><span className="course-cover"><Code2 size={18} /></span><div><small>CONTINUE LEARNING</small><strong>Frontend engineering</strong><span>Module 4 Â· Component systems</span></div><span className="preview-course-percent">68%</span></div></div></div><div className="float-badge float-badge-top"><span><BadgeCheck size={16} /></span><div><strong>New certificate</strong><small>UX Foundations</small></div></div><div className="float-badge float-badge-bottom"><div className="float-spark"><Sparkles size={15} /></div><div><small>CAREER MATCH</small><strong>Product designer <b>86%</b></strong></div><ArrowUpRight size={15} /></div></div>
    </section>
    <section className="trust-strip"><span>MADE FOR YOUR MOMENTUM</span><div><strong>Built for learners</strong><i /><strong>Trusted by teams</strong><i /><strong>Focused on real skills</strong><i /><strong>Ready for what's next</strong></div></section>
    <section className="features-section" id="careers"><div className="section-heading"><div><div className="eyebrow">A BETTER WAY TO GROW</div><h2>Make every learning hour count.</h2></div><p>Not another course library. A connected system that turns your effort into career progress.</p></div><div className="feature-grid">{features.map(({ icon: Icon, title, copy }, index) => <article className="feature-item" key={title}><div className={`feature-icon feature-${index}`}><Icon size={20} /></div><h3>{title}</h3><p>{copy}</p><span className="feature-arrow"><ArrowUpRight size={16} /></span></article>)}</div></section>
    <section className="how-section" id="how-it-works"><div className="how-copy"><div className="eyebrow">YOUR PATH, MADE CLEAR</div><h2>Small steps.<br /><em>Big direction.</em></h2><p>Know what matters, focus your time, and build evidence of your skills as you go.</p><Link to="/register" className="text-link">Find your starting point <ArrowRight size={15} /></Link></div><div className="how-steps"><article><span>01</span><div className="step-icon"><Compass size={18} /></div><div><h3>Choose your direction</h3><p>Explore roles and get a personal skill-gap snapshot.</p></div></article><article><span>02</span><div className="step-icon violet"><WandSparkles size={18} /></div><div><h3>Build skills that matter</h3><p>Follow a focused roadmap with courses, projects, and your AI mentor.</p></div></article><article><span>03</span><div className="step-icon amber"><ShieldCheck size={18} /></div><div><h3>Show what you can do</h3><p>Earn verified credentials and share work youâ€™re proud of.</p></div></article></div></section>
    <section className="stats-band"><div><strong>42k<span>+</span></strong><small>skills developed</small></div><i /><div><strong>18k</strong><small>career moves supported</small></div><i /><div><strong>96<span>%</span></strong><small>feel more confident</small></div><i /><div className="stats-note"><TrendingUp size={17} /><span>Progress you can see.<br />Momentum you can feel.</span></div></section>
    <section className="final-cta"><div className="cta-art"><div className="cta-ring ring-a" /><div className="cta-ring ring-b" /><div className="cta-spark"><GraduationCap size={27} /></div><span className="cta-star star-a">âœ¦</span><span className="cta-star star-b">âœ§</span></div><div><div className="eyebrow">YOUR NEXT CHAPTER IS YOURS</div><h2>Ready to make your<br />next move?</h2><p>Start with one skill. Build from there.</p><Link className="ui-button ui-button-primary" to="/register">Create your free account <ArrowRight size={16} /></Link></div><div className="cta-note"><span>01</span><strong>One clear next step<br />can change your direction.</strong><small>Letâ€™s find yours together.</small></div></section>
  </main>
}

function AuthArt({ register = false }: { register?: boolean }) {
  return (
    <aside className="auth-art">
      <div className="auth-art-noise" />
      <Link to="/" className="auth-art-brand">
        <span className="brand-mark"><GraduationCap size={19} /></span>
        skill<span>forge</span>
      </Link>
      <div className="auth-art-content">
        <div className="art-symbol">
          <div className="art-symbol-core"><Sparkles size={24} /></div>
          <i /><i /><i />
        </div>
        <div className="eyebrow">{register ? 'START WITH A SINGLE STEP' : 'YOUR WORK HAS MOMENTUM'}</div>
        <h2>{register ? 'Good things start with a plan.' : "Look how far you've already come."}</h2>
        <p>{register ? 'Build a learning path around the career you want, not just the courses you can find.' : 'Your skills are adding up. Keep building the proof that makes your next move possible.'}</p>
        <div className="auth-quote">
          <span>&ldquo;</span>
          <div>
            <strong>{register ? 'Progress looks good on you.' : 'I finally know what to focus on.'}</strong>
            <small>{register ? 'Your next chapter is yours to shape.' : 'Maya R. | Product design learner'}</small>
          </div>
        </div>
      </div>
      <div className="auth-art-foot">
        <span>LEARN WITH INTENTION</span><i />
        <span>GROW WITH CONFIDENCE</span><i />
        <span>MOVE WITH PROOF</span>
      </div>
    </aside>
  )
}

export function LoginPage() {
  const navigate = useNavigate()
  const [error, setError] = useState('')
  const [busy, setBusy] = useState(false)
  const [role, setRole] = useState<'learner' | 'admin'>('learner')

  const onSubmit = (event: FormEvent<HTMLFormElement>) => {
    event.preventDefault()
    const data = new FormData(event.currentTarget)
    const email = String(data.get('email') ?? '').trim()
    const password = String(data.get('password') ?? '')

    if (!email || !password) {
      setError('Enter your email and password to continue.')
      return
    }
    if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)) {
      setError('Enter a valid email address.')
      return
    }

    setError('')
    setBusy(true)
    signIn(email, password, role)
      .then(() => navigate(session.role === 'admin' ? '/admin' : '/app/dashboard'))
      .catch((e: Error) => setError(e.message))
      .finally(() => setBusy(false))
  }

  return <main className="auth-page">
    <section className="auth-form-side">
      <div className="auth-mobile-brand">
        <Link to="/" className="brand-lockup">
          <span className="brand-mark"><GraduationCap size={18} /></span>
          <span>skill<span>forge</span></span>
        </Link>
      </div>
      <div className="auth-form-wrap">
        <div className="auth-heading">
          <Badge tone="primary"><Sparkles size={12} /> WELCOME BACK</Badge>
          <h1>Your next step<br />is waiting.</h1>
          <p>Sign in to pick up right where you left off.</p>
        </div>
        <div className="login-role-tabs" role="group" aria-label="Choose login role">
          <button type="button" className={role === 'learner' ? 'login-role-tab active' : 'login-role-tab'} aria-pressed={role === 'learner'} onClick={() => { setRole('learner'); setError('') }}>
            <GraduationCap size={17} /> Learner Login
          </button>
          <button type="button" className={role === 'admin' ? 'login-role-tab active' : 'login-role-tab'} aria-pressed={role === 'admin'} onClick={() => { setRole('admin'); setError('') }}>
            <ShieldCheck size={17} /> Admin Login
          </button>
        </div>
        <form className="auth-form" onSubmit={onSubmit} noValidate>
          <Input label="Email address" name="email" type="email" placeholder="you@example.com" autoComplete="email" required />
          <Input label="Password" name="password" type="password" placeholder="Enter your password" autoComplete="current-password" required />
          <div className="form-options">
            <label className="check-label"><input type="checkbox" defaultChecked /> Keep me signed in</label>
          </div>
          {error && <div className="form-alert" role="alert">{error}</div>}
          <Button type="submit" size="lg" className="auth-submit" loading={busy}>
            Sign in as {role === 'admin' ? 'Admin' : 'Learner'} <ArrowRight size={16} />
          </Button>
          <p className="auth-switch">New to SkillForge? <Link to="/register">Create an account <ArrowUpRight size={13} /></Link></p>
        </form>
      </div>
      <p className="auth-legal">By continuing, you agree to our <a href="#terms">Terms</a> and <a href="#privacy">Privacy Policy</a>.</p>
    </section>
    <AuthArt />
  </main>
}
export function RegisterPage() {
  const navigate = useNavigate(); const [error, setError] = useState('')
  const onSubmit = (event: FormEvent<HTMLFormElement>) => { event.preventDefault(); const data = new FormData(event.currentTarget); const name = String(data.get('name') ?? '').trim(); const email = String(data.get('email') ?? '').trim(); const password = String(data.get('password') ?? ''); if (!name || !email) { setError('Add your name and a valid email address to continue.'); return }; if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)) { setError('Enter a valid email address.'); return }; if (password.length < 8) { setError('Choose a password with at least 8 characters.'); return }; if (data.get('consent') !== 'on') { setError('Accept the terms to create your account.'); return }; setError(''); signUp(name, email, password).then(() => navigate(session.role === 'admin' ? '/admin' : '/app/dashboard')).catch((e: Error) => setError(e.message)) }
  return (
    <main className="auth-page">
      <section className="auth-form-side">
        <div className="auth-mobile-brand">
          <Link to="/" className="brand-lockup">
            <span className="brand-mark"><GraduationCap size={18} /></span>
            <span>skill<span>forge</span></span>
          </Link>
        </div>
        <div className="auth-form-wrap">
          <div className="auth-heading">
            <Badge tone="primary"><Sparkles size={12} /> BUILD YOUR MOMENTUM</Badge>
            <h1>Make room for<br />what's next.</h1>
            <p>Your personalized path to a career you're excited about starts here.</p>
          </div>
          <form className="auth-form" onSubmit={onSubmit} noValidate>
            <Input label="Your name" name="name" placeholder="Jordan Lee" autoComplete="name" required />
            <Input label="Work or personal email" name="email" type="email" placeholder="you@example.com" autoComplete="email" required />
            <Input label="Create a password" name="password" type="password" placeholder="At least 8 characters" autoComplete="new-password" required hint="Use 8 or more characters." />
            {error && <div className="form-alert" role="alert">{error}</div>}
            <label className="check-label consent-check"><input type="checkbox" name="consent" required /> I agree to the <a href="#terms">Terms of Service</a> and <a href="#privacy">Privacy Policy</a>.</label>
            <Button type="submit" size="lg" className="auth-submit">Create your account <ArrowRight size={16} /></Button>
            <p className="auth-switch">Already have an account? <Link to="/login">Sign in <ArrowUpRight size={13} /></Link></p>
          </form>
        </div>
        <p className="auth-legal">Your learning data stays yours. Always.</p>
      </section>
      <AuthArt register />
    </main>
  )
}

export function CertificateVerifyPage() {
  const [code, setCode] = useState(''); const [result, setResult] = useState<'idle' | 'valid' | 'invalid'>('idle'); const [cert, setCert] = useState<{ title: string; issued_at: string; certificate_code: string } | null>(null); const [reason, setReason] = useState(''); const [busy, setBusy] = useState(false)
  const verify = async (event: FormEvent<HTMLFormElement>) => { event.preventDefault(); setBusy(true); try { const c = await api(`/certifications/verify/${encodeURIComponent(code.trim())}`); setCert(c); setResult('valid') } catch (e) { setReason(e instanceof Error ? e.message : ''); setResult('invalid') } finally { setBusy(false) } }
  return <main className="verify-page"><div className="verify-card"><div className="verify-emblem"><ShieldCheck size={24} /></div><Badge tone="primary">CREDENTIAL CHECK</Badge><h1>Verify a certificate</h1><p>Confirm the authenticity of a SkillForge credential with its unique verification code.</p><form onSubmit={verify} className="verify-form"><Input label="Verification code" name="code" placeholder="Paste the certificate code" value={code} onChange={(event) => { setCode(event.target.value); setResult('idle') }} autoCapitalize="characters" required /><Button type="submit" size="lg" className="verify-submit" loading={busy}>Verify credential <ArrowRight size={16} /></Button></form>{result === 'valid' && <div className="verify-result valid-result" role="status"><span><CheckCircle2 size={20} /></span><div><strong>Certificate verified</strong><p>This credential is authentic and active.</p><div className="verified-person"><div><b>{cert?.title}</b><small>Issued {cert ? new Date(cert.issued_at).toLocaleDateString('en', { month: 'short', day: 'numeric', year: 'numeric' }) : ''}</small></div></div><div className="verified-code">ID <strong>{cert?.certificate_code}</strong></div></div></div>}{result === 'invalid' && <div className="verify-result invalid-result" role="alert"><span><ShieldCheck size={20} /></span><div><strong>We couldnâ€™t verify this code</strong><p>{reason || 'Check for typos or contact the certificate holder for an updated link.'}</p></div></div>}<div className="verify-trust"><LockKeyhole size={13} /> Secure verification Â· No account required</div></div><div className="verify-footer"><GraduationCap size={15} /> SkillForge credentials are issued for verified learning achievements.</div></main>
}

