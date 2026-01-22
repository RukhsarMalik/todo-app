# Feature Specification: JWT Authentication

**Feature Branch**: `004-jwt-auth`
**Created**: 2026-01-18
**Status**: Draft
**Module**: Phase II - Module 3 of 5
**Input**: User description: "Module 3: Authentication - Better Auth + JWT for secure API endpoints"

## 1. Module Overview

| Attribute | Value |
|-----------|-------|
| **Module Name** | Authentication (JWT + Better Auth) |
| **Purpose** | Secure API endpoints with JWT token verification |
| **Dependencies** | Module 1 (Database), Module 2 (Backend API) |
| **Phase** | Phase II - Module 3 of 5 |

---

## 2. Scope of This Module

### What's INCLUDED in this module

- User registration (signup) endpoint
- User login endpoint with JWT token generation
- JWT verification middleware for FastAPI
- User table creation and management
- Protect all /api/{user_id}/tasks/* endpoints
- Validate URL user_id matches JWT token user_id
- User logout endpoint
- Password hashing and secure storage

### What's NOT INCLUDED (handled in other modules)

| Excluded Item | Target Module |
|---------------|---------------|
| Frontend authentication UI | Module 4: Frontend |
| Password reset flow | Out of scope for Phase II |
| OAuth providers (Google, GitHub) | Out of scope for Phase II |
| Email verification | Out of scope for Phase II |
| Refresh tokens | Out of scope (7-day expiry sufficient for MVP) |

---

## User Scenarios & Testing *(mandatory)*

### User Story 1 - User Signup (Priority: P1)

As a new user, I want to create an account so that I can access the todo application.

**Why this priority**: Foundation for all authenticated functionality. Users must be able to create accounts before they can use any protected features.

**Independent Test**: Can be fully tested by sending POST /api/auth/signup with valid credentials and verifying user creation and JWT token response.

**Acceptance Scenarios**:

1. **Given** a new user with valid email and password, **When** they submit signup request, **Then** an account is created and JWT token is returned.
2. **Given** a password less than 8 characters, **When** they submit signup, **Then** they receive a validation error with password requirements.
3. **Given** an email that already exists, **When** they submit signup, **Then** they receive a 400 error indicating email is taken.
4. **Given** an invalid email format, **When** they submit signup, **Then** they receive a validation error for email format.
5. **Given** successful signup, **When** response is returned, **Then** JWT token includes user_id claim for use with task endpoints.

---

### User Story 2 - User Login (Priority: P1)

As a returning user, I want to log in so that I can access my tasks.

**Why this priority**: Core authentication flow - users need to authenticate to access their data.

**Independent Test**: Can be fully tested by creating a user, then logging in with valid credentials and verifying JWT token response.

**Acceptance Scenarios**:

1. **Given** valid email and password, **When** user submits login, **Then** JWT token is returned with user information.
2. **Given** invalid password, **When** user submits login, **Then** 401 Unauthorized is returned.
3. **Given** non-existent email, **When** user submits login, **Then** 401 Unauthorized is returned (no information leak about user existence).
4. **Given** successful login, **When** JWT token is examined, **Then** it contains user_id, email, and expiration claims.
5. **Given** successful login, **When** token expiration is checked, **Then** it is set to 7 days from issuance.

---

### User Story 3 - JWT Verification Middleware (Priority: P1)

As a backend developer, I want all task endpoints protected so that only authenticated users can access their own tasks.

**Why this priority**: Security requirement - protects all Module 2 endpoints from unauthorized access.

**Independent Test**: Can be fully tested by attempting to access task endpoints with valid token, invalid token, missing token, and mismatched user_id.

**Acceptance Scenarios**:

1. **Given** a valid JWT token, **When** accessing /api/{user_id}/tasks, **Then** request proceeds if token.user_id matches URL user_id.
2. **Given** no Authorization header, **When** accessing task endpoints, **Then** 401 Unauthorized is returned.
3. **Given** an invalid/expired JWT token, **When** accessing task endpoints, **Then** 401 Unauthorized is returned.
4. **Given** a valid token for user_a, **When** accessing /api/user_b/tasks, **Then** 403 Forbidden is returned.
5. **Given** a valid token with matching user_id, **When** performing any CRUD operation, **Then** operation proceeds normally.

---

### User Story 4 - User Logout (Priority: P2)

As a logged-in user, I want to log out so that my session is ended.

**Why this priority**: Important for security but not blocking core functionality (client can simply discard token).

**Independent Test**: Can be fully tested by calling logout endpoint and verifying success response.

**Acceptance Scenarios**:

1. **Given** a logged-in user, **When** they call logout endpoint, **Then** success message is returned.
2. **Given** logout is called, **When** client receives response, **Then** client should discard stored JWT token.

---

### Edge Cases

- What happens when JWT token is expired? (Return 401 with "Token expired" message)
- What happens when Authorization header format is wrong? (Return 401 with "Invalid authorization format")
- What happens when user_id in URL contains special characters? (URL encoding handled, validated against token)
- What happens when password is exactly 8 characters? (Should succeed - minimum met)
- What happens when database connection fails during auth? (Return 500, log error, no sensitive info exposed)

---

## Requirements *(mandatory)*

### Functional Requirements

#### Authentication Endpoints

- **FR-001**: System MUST provide signup endpoint (POST /api/auth/signup) accepting email, password, and optional name
- **FR-002**: System MUST provide login endpoint (POST /api/auth/login) accepting email and password
- **FR-003**: System MUST provide logout endpoint (POST /api/auth/logout)
- **FR-004**: System MUST return JWT token on successful signup or login

#### Password Requirements

- **FR-005**: System MUST require password minimum 8 characters
- **FR-006**: System MUST hash passwords before storage (bcrypt recommended)
- **FR-007**: System MUST never return password in any response

#### JWT Token Requirements

- **FR-008**: JWT tokens MUST include user_id claim
- **FR-009**: JWT tokens MUST include email claim
- **FR-010**: JWT tokens MUST include expiration (exp) claim set to 7 days
- **FR-011**: JWT tokens MUST be signed with a secret key from environment variable

#### Middleware Requirements

- **FR-012**: System MUST verify JWT on all /api/{user_id}/tasks/* routes
- **FR-013**: System MUST extract user_id from verified JWT token
- **FR-014**: System MUST compare token.user_id with URL user_id parameter
- **FR-015**: System MUST return 401 if token is missing or invalid
- **FR-016**: System MUST return 403 if user_id mismatch (token vs URL)

#### User Data Requirements

- **FR-017**: System MUST create users table with id, email, password_hash, name, created_at
- **FR-018**: System MUST enforce unique email constraint
- **FR-019**: System MUST generate unique user_id for each user

#### Error Handling

- **FR-020**: System MUST return consistent JSON error format with detail field
- **FR-021**: System MUST NOT expose stack traces or sensitive information in errors
- **FR-022**: System MUST use 400 for validation errors, 401 for auth failures, 403 for access denied

### Key Entities

- **User**: Represents an authenticated user (id, email, password_hash, name, created_at)
- **JWT Token**: Represents authentication state (user_id, email, exp - not persisted, generated on demand)

---

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Users can complete signup in under 5 seconds
- **SC-002**: Users can complete login in under 3 seconds
- **SC-003**: JWT verification adds less than 50ms to request processing time
- **SC-004**: All 6 task endpoints (Module 2) reject unauthenticated requests with 401
- **SC-005**: All task endpoints reject mismatched user_id with 403
- **SC-006**: Password validation correctly rejects passwords under 8 characters
- **SC-007**: Duplicate email registration returns appropriate error
- **SC-008**: Invalid credentials return 401 without revealing which field is wrong
- **SC-009**: API documentation (/docs) shows authentication requirements for protected endpoints
- **SC-010**: Tokens remain valid for 7 days after issuance

---

## Dependencies & Prerequisites

### Required (from previous modules)

- Module 1: Database connection and session management (db.py)
- Module 2: Task routes ready for middleware injection (routes/tasks.py)
- Neon PostgreSQL database accessible

### Environment Variables

- DATABASE_URL (existing from Module 1)
- JWT_SECRET_KEY (new - minimum 32 characters)

---

## Integration Points

### Updates Module 2

- Add auth middleware to all task routes in routes/tasks.py
- Remove TODO comments for JWT verification
- Inject user from verified token into route handlers

### Prepares Module 4

- Backend auth fully functional
- Frontend will add UI for signup/login
- API client will store and inject JWT tokens

---

## Assumptions

1. JWT tokens are stored client-side (localStorage or cookie - Module 4 decision)
2. Token refresh not needed for MVP (7-day expiry sufficient)
3. Single authentication method (email/password) sufficient for MVP
4. User IDs are UUIDs or similar unique string identifiers
5. Name field is optional during signup
6. No email verification required for MVP
7. Logout is client-side only (no server-side token blacklist for MVP)

---

## Out of Scope (This Module)

- Frontend authentication UI (Module 4)
- Password reset flow
- Email verification
- OAuth providers (Google, GitHub, etc.)
- Refresh tokens
- Multi-factor authentication
- Session management beyond JWT
- Account deletion
- User profile updates

---

## Testing Checklist

- [ ] Signup creates user and returns token
- [ ] Signup rejects duplicate email with 400
- [ ] Signup rejects weak password with 400
- [ ] Login returns token for valid credentials
- [ ] Login returns 401 for invalid credentials
- [ ] Protected endpoints reject missing token with 401
- [ ] Protected endpoints reject invalid token with 401
- [ ] Protected endpoints reject expired token with 401
- [ ] Protected endpoints reject mismatched user_id with 403
- [ ] Protected endpoints allow valid token with matching user_id
- [ ] Logout returns success message
- [ ] Error responses use consistent JSON format
- [ ] API docs show authentication requirements
