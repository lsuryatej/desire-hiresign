# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added - Sprint 0
- Repository structure with monorepo layout
- Docker Compose infrastructure (PostgreSQL, Redis, MinIO, Adminer)
- FastAPI backend skeleton with health endpoint
- Alembic for database migrations
- GitHub Actions CI workflow
- Basic tests and linting configuration
- CONTRIBUTING.md and developer documentation
- **Design system with minimalist, low-strain UI guidelines**
- Theme tokens for colors, typography, spacing
- Component guidelines for swipe cards, forms, chat, filters
- Accessibility standards (WCAG AA compliance)
- Dark mode color palette (optional)

### Infrastructure
- PostgreSQL 15 database
- Redis 7 for caching and queues
- MinIO for S3-compatible object storage
- Adminer for database administration

### Backend
- FastAPI application setup
- SQLAlchemy ORM configuration
- User model with role-based access
- Database migration system
- Health check endpoint
- CORS middleware

### CI/CD
- GitHub Actions workflow for testing
- Linting with flake8 and black
- Coverage reporting with pytest

## [0.1.0] - 2024-XX-XX

### Added
- Initial project structure
