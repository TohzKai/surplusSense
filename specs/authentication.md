# Authentication Specification

> **Phase 2 — Not part of final submitted MVP.** Multi-role authentication is Phase 2. The submitted MVP is the single-merchant decision cockpit in Streamlit.

## Overview

Three user roles: merchant, consumer, admin. All share the base User table with role-based access control.

## Registration

### Consumer Registration

1. Submit: email, password (min 8 chars), full_name
2. Email verification sent (optional for MVP — can defer)
3. Account created with role=consumer
4. Redirected to preference quiz (3 questions)

### Merchant Registration

1. Submit: email, password, full_name, business_name, address, sfa_license, cuisine_types, operating_hours
2. Account created with role=merchant, sfa_verified=FALSE
3. SFA license verification (automated check or manual review within 24h)
4. During verification: merchant can explore dashboard but cannot create listings
5. On verification: merchant receives notification, full access granted

### Admin Registration

- Seed via CLI/migration (no public registration)
- First admin created during deployment

### OAuth (Google, Apple)

1. User clicks "Sign in with Google/Apple"
2. OAuth flow → callback with provider + ID
3. If new user: create account, redirect to role selection (merchant or consumer)
4. If existing user: log in directly

## Authentication

### Login

- Email + password → validate against bcrypt hash
- On success: generate JWT access token (15min) + refresh token (7 days)
- Rate limit: 10 failed attempts per email per 15 minutes → temporary lockout

### Token Management

- Access token: JWT, 15-minute expiry, contains user_id and role
- Refresh token: Opaque, 7-day expiry, stored in HttpOnly cookie
- Refresh flow: POST /api/v1/auth/refresh with refresh token → new access token

### Session Security

- Bearer token in Authorization header for API calls
- No server-side session state (stateless JWT)
- Token blacklisting on logout (Redis or database flag, optional for MVP)

## Role-Based Access Control

| Endpoint Category | Consumer                     | Merchant                | Admin            |
| ----------------- | ---------------------------- | ----------------------- | ---------------- |
| /auth/\*          | Own profile only             | Own profile only        | All users        |
| /merchants/\*     | Read only                    | Own merchant CRUD       | All merchants    |
| /listings/\*      | Read + purchase              | Own listings CRUD       | All listings     |
| /orders/\*        | Own orders                   | Orders for own listings | All orders       |
| /reviews/\*       | Create own, read all         | Read all                | All reviews      |
| /ml/\*            | Predictions, recommendations | Predictions, analytics  | All ML endpoints |
| /admin/\*         | Denied                       | Denied                  | Full access      |

## Password Management

- Minimum 8 characters, no complexity requirements for MVP
- bcrypt hash with cost factor 12
- Password reset via email link (token-based, 1-hour expiry)
- No password reuse checking for MVP

## API Endpoints

| Method | Path                          | Description              |
| ------ | ----------------------------- | ------------------------ |
| POST   | /api/v1/auth/register         | Register new user        |
| POST   | /api/v1/auth/login            | Login, returns tokens    |
| POST   | /api/v1/auth/refresh          | Refresh access token     |
| POST   | /api/v1/auth/logout           | Invalidate refresh token |
| POST   | /api/v1/auth/forgot-password  | Request password reset   |
| POST   | /api/v1/auth/reset-password   | Reset with token         |
| GET    | /api/v1/auth/me               | Get current user profile |
| PATCH  | /api/v1/auth/me               | Update profile           |
| POST   | /api/v1/auth/oauth/{provider} | OAuth login/register     |
