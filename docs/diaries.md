# Thought Diary API

The Thought Diary API provides endpoints for managing personal thought diary entries with AI-powered sentiment analysis.

> **Postman Collection**: A ready-to-use Postman collection is available at [`thought_diary_api.postman_collection.json`](thought_diary_api.postman_collection.json).

## Overview

The API allows users to:
- Create thought diary entries
- View their entries with pagination
- Update existing entries
- Delete entries
- Get statistics about their entries
- View sentiment analysis of their entries (positive/negative thoughts and feelings)

All endpoints are protected with JWT authentication and require a valid access token.

## Authentication

All endpoints require a valid JWT token. Include the token in the `Authorization` header:

```
Authorization: Bearer <your_access_token>
```

See the [Authentication documentation](authentication.md) for details on obtaining tokens.

## Endpoints

### List All Thought Diaries

```
GET /diaries
```

Get all thought diaries for the current user with pagination.

**Query Parameters:**
- `page`: Page number (defaults to 1)
- `per_page`: Items per page (defaults to 10, maximum 50)

**Response:**
```json
{
  "items": [
    {
      "id": 1,
      "user_id": 1,
      "content": "My original thought diary content...",
      "analyzed_content": "My original <span class=\"positive\">thought</span> diary content...",
      "created_at": "2025-10-01T12:00:00Z",
      "updated_at": "2025-10-01T12:00:00Z"
    }
  ],
  "total": 15,
  "page": 1,
  "per_page": 10,
  "total_pages": 2
}
```

### Create Thought Diary

```
POST /diaries
```

Create a new thought diary entry with automatic sentiment analysis.

**Request Body:**
```json
{
  "content": "I felt both excitement and anxious after I got elected."
}
```

**Response:**
```json
{
  "id": 1,
  "user_id": 1,
  "content": "I felt both excitement and anxious after I got elected.",
  "analyzed_content": "I felt both <span class=\"positive\">excitement</span> and <span class=\"negative\">anxious</span> after I got elected.",
  "created_at": "2025-10-03T12:00:00Z",
  "updated_at": "2025-10-03T12:00:00Z"
}
```

### Get Specific Diary Entry

```
GET /diaries/{id}
```

Get a specific thought diary entry by ID.

**Response:**
```json
{
  "id": 1,
  "user_id": 1,
  "content": "I felt both excitement and anxious after I got elected.",
  "analyzed_content": "I felt both <span class=\"positive\">excitement</span> and <span class=\"negative\">anxious</span> after I got elected.",
  "created_at": "2025-10-03T12:00:00Z",
  "updated_at": "2025-10-03T12:00:00Z"
}
```

### Update Diary Entry

```
PUT /diaries/{id}
```

Update a specific thought diary entry. The content will be re-analyzed for sentiment.

**Request Body:**
```json
{
  "content": "I felt both excitement and confident after I got elected."
}
```

**Response:**
```json
{
  "id": 1,
  "user_id": 1,
  "content": "I felt both excitement and confident after I got elected.",
  "analyzed_content": "I felt both <span class=\"positive\">excitement</span> and <span class=\"positive\">confident</span> after I got elected.",
  "created_at": "2025-10-03T12:00:00Z",
  "updated_at": "2025-10-03T12:30:00Z"
}
```

### Delete Diary Entry

```
DELETE /diaries/{id}
```

Delete a specific thought diary entry.

**Response:**
```json
{
  "message": "Thought diary deleted successfully"
}
```

### Get Diary Statistics

```
GET /diaries/stats
```

Get statistics about the user's thought diaries.

**Response:**
```json
{
  "total_entries": 15,
  "entries_this_week": 5,
  "entries_this_month": 12,
  "average_length": 250,
  "sentiment_counts": {
    "positive": 7,
    "negative": 5,
    "neutral": 3
  },
  "last_entry_date": "2025-10-03T12:30:00Z"
}
```

## Sentiment Analysis

Each thought diary entry is processed with AI-powered sentiment analysis using the GitHub Models API. The analysis identifies positive and negative expressions in the text and wraps them with HTML span elements:

- Positive expressions: `<span class="positive">text</span>`
- Negative expressions: `<span class="negative">text</span>`

When displaying this content in a web application, you can apply CSS styling:

```css
span.positive {
    background-color: green;
    color: white;
}
span.negative {
    background-color: red;
    color: white;
}
```

See the [Sentiment Analysis documentation](sentiment_analysis.md) for more details on how the analysis works.

## Error Responses

The API returns appropriate HTTP status codes along with error messages:

- `400 Bad Request`: Invalid input data
- `401 Unauthorized`: Missing or invalid authentication token
- `403 Forbidden`: Trying to access another user's diary
- `404 Not Found`: Resource not found
- `500 Internal Server Error`: Server error