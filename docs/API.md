# StealthInterview API Documentation

## Base URL

```
http://localhost:8000
```

## Authentication

Authentication is disabled by default. Enable it in `config/config.yaml` by setting `api.auth_required: true`.

## Endpoints

### Health Check

```
GET /health
```

Check if the API and Ollama server are running.

**Response:**
```json
{
  "status": "healthy",
  "version": "0.1.0",
  "ollama_available": true
}
```

### Generate Answer

```
POST /generate
```

Generate an AI-powered answer to an interview question.

**Request Body:**
```json
{
  "question": "Tell me about yourself",
  "format": "behavioral",
  "answer_length": "medium",
  "technical_detail": "high",
  "resume_context": "Skills: Python, React. Experience: 3 years at Tech Corp."
}
```

**Response:**
```json
{
  "question": "Tell me about yourself",
  "answer": "I'm a software engineer with 3 years of experience...",
  "format": "behavioral",
  "tokens_used": 150,
  "duration_ms": 850.5
}
```

### Transcribe Audio

```
POST /transcribe
```

Transcribe base64-encoded audio to text using Whisper.

**Request Body:**
```json
{
  "audio_base64": "base64-encoded-audio-data",
  "language": "en"
}
```

**Response:**
```json
{
  "text": "Tell me about yourself",
  "confidence": 0.95,
  "language": "en",
  "duration": 3.2
}
```

### Parse Resume

```
POST /resume/parse?file_path=/path/to/resume.pdf
```

Parse a resume file and extract structured data.

**Response:**
```json
{
  "skills": ["python", "react", "aws"],
  "experience": [
    {
      "title": "Software Engineer",
      "details": ["Built web applications", "Led team of 5"]
    }
  ],
  "education": [
    {
      "title": "B.S. Computer Science",
      "details": ["University X, 2016-2020"]
    }
  ],
  "projects": [],
  "contact": {
    "email": "user@example.com",
    "phone": "+1-555-0123"
  }
}
```

### Start Mock Interview

```
POST /mock/start
```

Start a new mock interview session with questions from the selected bank.

**Request Body:**
```json
{
  "format": "behavioral",
  "difficulty": "medium",
  "num_questions": 5
}
```

**Response:**
```json
{
  "session_id": "uuid-here",
  "format": "behavioral",
  "difficulty": "medium",
  "num_questions": 5,
  "questions": [
    {
      "id": "beh_001",
      "question": "Tell me about yourself.",
      "category": "behavioral",
      "difficulty": "easy",
      "tags": ["introduction", "background"]
    }
  ]
}
```

### Get Configuration

```
GET /config
```

Get current API configuration.

### Interactive Documentation

- **Swagger UI:** `http://localhost:8000/docs`
- **ReDoc:** `http://localhost:8000/redoc`
- **OpenAPI Spec:** `http://localhost:8000/openapi.json`

## Error Responses

| Status | Description |
|--------|-------------|
| 400 | Bad Request |
| 404 | Not Found |
| 422 | Validation Error |
| 503 | Service Unavailable (component not initialized) |
| 500 | Internal Server Error |

## Rate Limiting

Default rate limit: 100 requests per minute (configurable).

## Examples

### cURL - Generate Answer

```bash
curl -X POST "http://localhost:8000/generate" \
  -H "Content-Type: application/json" \
  -d '{"question": "What is your greatest weakness?", "format": "behavioral"}'
```

### Python - Generate Answer

```python
import requests

response = requests.post(
    "http://localhost:8000/generate",
    json={"question": "Tell me about a challenge you faced", "format": "behavioral"},
)
print(response.json()["answer"])
```

### JavaScript - Generate Answer

```javascript
const response = await fetch("http://localhost:8000/generate", {
  method: "POST",
  headers: { "Content-Type": "application/json" },
  body: JSON.stringify({ question: "Why should we hire you?", format: "behavioral" }),
});
const data = await response.json();
console.log(data.answer);
```