# Todo App with AI Assistant - Complete Project Overview

## Table of Contents
- [Project Description](#project-description)
- [Technology Stack](#technology-stack)
- [Project Phases](#project-phases)
- [Architecture Overview](#architecture-overview)
- [Features](#features)
- [Deployment](#deployment)
- [Getting Started](#getting-started)

## Project Description

This is a comprehensive Todo application with AI-powered task management capabilities, built using a modern tech stack and following a phased development approach. The application combines traditional task management with advanced AI features, event-driven architecture, and cloud-native deployment strategies.

## Technology Stack

### Backend
- **Language**: Python 3.13+
- **Framework**: FastAPI
- **Database**: Neon PostgreSQL via SQLModel
- **Authentication**: JWT with python-jose
- **AI Integration**: OpenAI Agents SDK + Model Context Protocol (MCP)
- **Package Manager**: UV

### Frontend
- **Framework**: Next.js 16+ with App Router
- **Language**: TypeScript 5.x
- **Styling**: Tailwind CSS 4
- **Deployment**: Vercel

### Infrastructure & Architecture
- **Containerization**: Docker
- **Orchestration**: Kubernetes (Minikube for local)
- **Event Streaming**: Apache Kafka (Strimzi)
- **Microservices**: Dapr (Distributed Application Runtime)
- **Pub/Sub**: Dapr with Kafka backend

## Project Phases

### Phase I: Console Application
- Basic todo console application
- Implemented with Python standard library
- Core functionality: add, list, complete, delete tasks
- Data persistence using in-memory list

### Phase II: Backend API & Authentication
- RESTful API with FastAPI
- User authentication with JWT
- Database integration with Neon PostgreSQL
- SQLModel for ORM operations
- Secure password hashing with bcrypt

### Phase III: AI Chat Integration
- OpenAI Agents SDK integration
- Model Context Protocol (MCP) tools
- AI-powered task management via natural language
- Conversation history management
- MCP server implementation

### Phase IV: Cloud Native Deployment
- Docker containerization
- Kubernetes orchestration
- Helm charts for package management
- Multi-stage Docker builds
- Vercel deployment for frontend

### Phase V: Advanced Features & Event Architecture
- **Advanced Task Management**:
  - Task priorities (low/medium/high/urgent)
  - Due dates with reminders
  - Tags system (many-to-many relationships)
  - Recurring tasks (daily/weekly/monthly)
- **Event-Driven Architecture**:
  - Dapr Pub/Sub for event publishing
  - Apache Kafka for event streaming
  - Notification system with event consumers
  - Microservices with Dapr sidecars
- **Enhanced AI Capabilities**:
  - MCP tools for tags and notifications
  - Advanced task management via AI

## Architecture Overview

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   Frontend      │    │   Load Balancer  │    │   Backend API   │
│   (Next.js)     │◄──►│   (Ingress)      │◄──►│   (FastAPI)     │
│   Vercel        │    │                  │    │                 │
└─────────────────┘    └──────────────────┘    └─────────────────┘
                                                      │
                                                      ▼
                                          ┌─────────────────────┐
                                          │   Neon PostgreSQL   │
                                          │                     │
                                          └─────────────────────┘
                                                      │
                                                      ▼
                                    ┌─────────────────────────────┐
                                    │        Kafka Cluster        │
                                    │   (Event Streaming Layer)   │
                                    └─────────────────────────────┘
                                                      │
                    ┌─────────────────────────────────┼─────────────────────────────────┐
                    ▼                                 ▼                                 ▼
        ┌─────────────────────┐        ┌─────────────────────┐        ┌─────────────────────┐
        │ Notification Service│        │Recurring Task Service│        │   MCP Server        │
        │   (Dapr Consumer)   │        │   (Dapr Consumer)   │        │    (MCP Tools)      │
        └─────────────────────┘        └─────────────────────┘        └─────────────────────┘
```

## Features

### Core Features
- User registration and authentication
- Task CRUD operations
- Task status management (pending, completed)
- Secure JWT-based authentication

### Advanced Features (Phase V)
- **Task Priorities**: Low, Medium, High, Urgent priority levels
- **Due Dates & Reminders**: Customizable due dates with reminder notifications
- **Tagging System**: Organize tasks with custom tags
- **Recurring Tasks**: Daily, weekly, or monthly recurring tasks
- **Event-Driven Notifications**: Real-time notifications via event architecture
- **Advanced Search & Filter**: Search by title/description, filter by status/priority/tags

### AI Integration
- Natural language task creation and management
- AI-powered task suggestions
- Conversation-based task management
- MCP tools for seamless AI integration

### Microservices Architecture
- Decoupled services with Dapr
- Event-driven communication
- Scalable and resilient design
- Graceful degradation capabilities

## Deployment

### Backend (Hugging Face Spaces)
- Deployed on Hugging Face Spaces using Docker
- Runs on port 7860 (Hugging Face requirement)
- Connected to Neon PostgreSQL database
- Supports AI integration with OpenAI API

### Frontend (Vercel)
- Deployed on Vercel with Next.js static generation
- Connected to Hugging Face backend API
- Responsive design for all devices

## Getting Started

### Prerequisites
- Python 3.13+
- Node.js 22+ LTS
- Docker
- Kubernetes (for local development with Minikube)
- Neon PostgreSQL account
- OpenAI API key

### Local Development Setup

#### Backend (Phase V)
```bash
cd phase-5/backend
uv sync
uv run uvicorn main:app --reload --port 8000
```

#### Frontend
```bash
cd phase-5/frontend
npm install
npm run dev
```

### Environment Variables

#### Backend (.env)
```
DATABASE_URL=your_neon_postgres_url
JWT_SECRET_KEY=your_jwt_secret_key_min_32_chars
OPENAI_API_KEY=your_openai_api_key
FRONTEND_URL=http://localhost:3000
```

#### Frontend (.env.local)
```
NEXT_PUBLIC_API_URL=http://localhost:8000
NEXT_PUBLIC_OPENAI_DOMAIN_KEY=your_openai_domain_key
```

## Key Accomplishments

- **Complete Full-Stack Application**: From console app to cloud-native solution
- **Advanced AI Integration**: Natural language task management
- **Event-Driven Architecture**: Scalable microservices with Kafka and Dapr
- **Cloud-Native Deployment**: Containerized services with Kubernetes orchestration
- **Modern Tech Stack**: Latest versions of industry-standard technologies
- **Production-Ready**: Includes monitoring, logging, and observability features

## Conclusion

This project demonstrates a comprehensive journey from a simple console application to a sophisticated, AI-powered, event-driven, cloud-native task management system. It showcases modern development practices, advanced architecture patterns, and the integration of cutting-edge technologies like AI assistants and microservices.

The application is production-ready with proper security measures, scalable architecture, and robust deployment strategies across multiple platforms.