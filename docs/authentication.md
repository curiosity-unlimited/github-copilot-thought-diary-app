# Authentication System

This document describes the authentication system for the Thought Diary application.

## Overview

The authentication system uses JWT (JSON Web Token) for secure authentication and authorization. It provides endpoints for user registration, login, logout, token refresh, and profile retrieval.

## Features

- User registration with email validation and password strength enforcement
- Secure login with JWT token generation
- Token refresh for extending sessions
- Secure logout with token blocklisting
- Rate limiting for public endpoints to prevent abuse
- Profile retrieval for authenticated users

## Authentication Flow

1. User registers with email and password
2. User logs in and receives access and refresh tokens
3. Access token is used for API requests
4. When access token expires, refresh token is used to get a new access token
5. User logs out, invalidating the current tokens

## Environment Variables

The following environment variables control the authentication behavior:

- `JWT_SECRET_KEY`: Secret key for signing JWT tokens
- `JWT_ACCESS_TOKEN_EXPIRES_MINUTES`: Access token expiration time in minutes (default: 15)
- `JWT_REFRESH_TOKEN_EXPIRES_DAYS`: Refresh token expiration time in days (default: 30)
- `REDIS_URL`: Redis connection URL for production rate limiting and token blocklisting

## Rate Limiting

Public authentication endpoints have rate limits to prevent abuse:

- `/auth/register`: 3 requests per hour
- `/auth/login`: 5 requests per 15 minutes

## API Endpoints

### Register

- **URL**: `/auth/register`
- **Method**: `POST`
- **Rate Limit**: 3 per hour
- **Body**:
  ```json
  {
    "email": "user@example.com",
    "password": "SecurePassword123!"
  }
  ```
- **Success Response**: `201 Created`
  ```json
  {
    "message": "User created successfully",
    "user_id": 1
  }
  ```
- **Error Responses**:
  - `400 Bad Request`: Missing or invalid fields
  - `409 Conflict`: User already exists

### Login

- **URL**: `/auth/login`
- **Method**: `POST`
- **Rate Limit**: 5 per 15 minutes
- **Body**:
  ```json
  {
    "email": "user@example.com",
    "password": "SecurePassword123!"
  }
  ```
- **Success Response**: `200 OK`
  ```json
  {
    "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
    "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
    "user": {
      "id": 1,
      "email": "user@example.com"
    },
    "expires_in": 900
  }
  ```
- **Error Responses**:
  - `400 Bad Request`: Missing fields
  - `401 Unauthorized`: Invalid credentials

### Refresh Token

- **URL**: `/auth/refresh`
- **Method**: `POST`
- **Authentication**: Refresh JWT token required
- **Success Response**: `200 OK`
  ```json
  {
    "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
    "expires_in": 900
  }
  ```
- **Error Response**:
  - `401 Unauthorized`: Invalid or expired refresh token

### Logout

- **URL**: `/auth/logout`
- **Method**: `POST`
- **Authentication**: JWT token required
- **Success Response**: `200 OK`
  ```json
  {
    "message": "Successfully logged out"
  }
  ```
- **Error Response**:
  - `401 Unauthorized`: Invalid or expired token

### User Profile

- **URL**: `/auth/me`
- **Method**: `GET`
- **Authentication**: JWT token required
- **Success Response**: `200 OK`
  ```json
  {
    "id": 1,
    "email": "user@example.com",
    "created_at": "2023-04-01T12:00:00Z"
  }
  ```
- **Error Responses**:
  - `401 Unauthorized`: Not authenticated
  - `404 Not Found`: User not found