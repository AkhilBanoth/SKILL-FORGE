import { useLocation } from 'react-router-dom'
import { CareerDetailPage, CareersPage, DashboardPage, SkillsPage } from './DashboardSkillsCareers'
import { CertificatesPage, CourseDetailPage, CoursesPage, ProfilePage, ProjectsPage } from './LearningPages'
import { AssessmentFlowPage, AssessmentResultsPage, AssessmentsPage, LessonPage, MentorPage, NotificationsPage, ProjectDetailPage, ResumePage } from './LiveLearning'
import './learner.css'

export function LearnerRouter() {
  const { pathname } = useLocation()
  if (pathname === '/app/dashboard' || pathname === '/app') return <DashboardPage />
  if (pathname === '/app/skills') return <SkillsPage />
  if (pathname === '/app/careers') return <CareersPage />
  if (pathname.startsWith('/app/careers/')) return <CareerDetailPage />
  if (pathname === '/app/courses') return <CoursesPage />
  if (/\/app\/courses\/[^/]+\/lesson/.test(pathname)) return <LessonPage />
  if (pathname.startsWith('/app/courses/')) return <CourseDetailPage />
  if (pathname === '/app/assessments') return <AssessmentsPage />
  if (pathname.endsWith('/results')) return <AssessmentResultsPage />
  if (pathname.endsWith('/take')) return <AssessmentFlowPage />
  if (pathname === '/app/projects') return <ProjectsPage />
  if (pathname.startsWith('/app/projects/')) return <ProjectDetailPage />
  if (pathname === '/app/certificates') return <CertificatesPage />
  if (pathname === '/app/resume') return <ResumePage />
  if (pathname === '/app/mentor') return <MentorPage />
  if (pathname === '/app/notifications') return <NotificationsPage />
  if (pathname === '/app/profile') return <ProfilePage />
  return <DashboardPage />
}
