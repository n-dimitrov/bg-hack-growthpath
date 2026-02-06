# LLM Integration Guide

## Configuration

Edit `backend/.env` with your Bosch LLM Farm API key:

```env
LLM_FARM_BASE_URL=https://aoai-farm.bosch-temp.com/api/google/v1
LLM_FARM_API_KEY=your-api-key-here
LLM_DEFAULT_MODEL=claude-sonnet-4-5@20250929
LLM_DEFAULT_MAX_TOKENS=4096
```

## API Endpoints

### 1. Health Check
```bash
curl http://localhost:8000/api/llm/health
```

### 2. Chat Completion
```bash
curl -X POST "http://localhost:8000/api/llm/chat" \
  -H "Content-Type: application/json" \
  -d '{
    "user_content": "What is Python?"
  }'
```

### 3. Chat with System Prompt
```bash
curl -X POST "http://localhost:8000/api/llm/chat" \
  -H "Content-Type: application/json" \
  -d '{
    "user_content": "Explain FastAPI",
    "system_content": "You are a Python expert. Be concise."
  }'
```

### 4. Use Different Model
```bash
curl -X POST "http://localhost:8000/api/llm/chat" \
  -H "Content-Type: application/json" \
  -d '{
    "user_content": "Hello",
    "model": "claude-haiku-4-5@20251001"
  }'
```

### 5. Custom Max Tokens
```bash
curl -X POST "http://localhost:8000/api/llm/chat" \
  -H "Content-Type: application/json" \
  -d '{
    "user_content": "Write a detailed explanation",
    "max_tokens": 8000
  }'
```

### 6. Skill Recommendations
```bash
curl -X POST "http://localhost:8000/api/llm/skills/recommend" \
  -H "Content-Type: application/json" \
  -d '{
    "current_skills": ["Python", "FastAPI"],
    "target_role": "Senior Backend Engineer",
    "experience_level": "mid-level"
  }'
```

### 7. Skill Gap Analysis
```bash
curl -X POST "http://localhost:8000/api/llm/skills/gap-analysis" \
  -H "Content-Type: application/json" \
  -d '{
    "user_skills": [{"name": "Python", "proficiency": 3}],
    "required_skills": [{"name": "Python", "proficiency": 4}]
  }'
```

## Request Parameters

| Parameter | Required | Default | Description |
|-----------|----------|---------|-------------|
| `user_content` | Yes | - | Your message or prompt |
| `system_content` | No | - | System prompt to guide the model |
| `model` | No | `claude-sonnet-4-5@20250929` | Model to use |
| `max_tokens` | No | `4096` | Maximum response length (1-8192) |

## How It Works

**Full Endpoint:**
```
https://aoai-farm.bosch-temp.com/api/google/v1/publishers/anthropic/models/{model}:rawPredict
```

**Request Format (sent to Bosch AOAI farm):**
```json
{
  "anthropic_version": "vertex-2023-10-16",
  "messages": [
    {"role": "user", "content": "..."}
  ],
  "max_tokens": 4096,
  "system": "optional system prompt"
}
```

## Quick Start

1. **Install dependencies:**
   ```bash
   cd backend
   pip install -r requirements.txt
   ```

2. **Update `.env` with your API key**

3. **Start server:**
   ```bash
   python run.py
   ```

4. **Test:**
   ```bash
   curl http://localhost:8000/api/llm/health
   ```

## Available Models

- `claude-sonnet-4-5@20250929` (default) - Best for complex reasoning
- `claude-haiku-4-5@20251001` - Faster, cheaper responses

## Troubleshooting

**"LLM_FARM_API_KEY is not configured"**
- Update `.env` file with your actual API key
- Restart the backend server

**Connection errors**
- Verify network access to `aoai-farm.bosch-temp.com`
- Check if you're on Bosch network/VPN

**Authentication errors**
- Verify your API key is valid
- Contact AOAI farm team for access
