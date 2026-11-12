# SkillForge – Backend Project Report

## 1. Project Overview

SkillForge is an AI-powered learning, certification, and career-readiness platform. This repository contains the backend application, which provides REST APIs for user management, skills, careers, learning resources, assessments, projects, certifications, and AI-powered assistance.

## 2. Technology Stack

- **Backend Framework:** Python FastAPI
- **Database:** PostgreSQL with SQLAlchemy
- **Additional Database:** MongoDB
- **Authentication:** JWT Bearer authentication
- **AI Integration:** Google Gemini API
- **Testing:** Pytest

## 3. Backend Modules

- User registration, login, and profile management
- Role-based access control
- Skills and career management
- Skill-gap analysis and career readiness
- Courses, modules, lessons, and learning resources
- Assessments and project submissions
- Certifications and notifications
- Analytics and AI mentor services

## 4. Security

- JWT-based authentication
- Protected API endpoints
- Role-based authorization
- Environment-based configuration
- Production validation for secure JWT secrets and PostgreSQL configuration

## 5. Database

PostgreSQL stores the primary application data through SQLAlchemy models. MongoDB supports additional application data and services.

## 6. AI Capabilities

Google Gemini integration supports AI mentor responses, question generation, recommendations, and project assistance.

## 7. Testing

The backend includes automated Pytest coverage for authentication, users, skills, courses, assessments, projects, certifications, and AI services.

## 8. Deployment

The backend is designed to run as an independent FastAPI service. Configuration and credentials are supplied through environment variables. The API provides a health endpoint and interactive documentation at `/docs`.