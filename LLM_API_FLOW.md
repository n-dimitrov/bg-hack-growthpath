# LLM API Integration Flow

## Architecture

The skills analysis feature uses a **layered API architecture** for better separation of concerns:

```
Frontend → Users API → LLM API → LLM Farm (Bosch)
```

### Why This Approach?

1. **Separation of Concerns** - Users API handles user data, LLM API handles AI calls
2. **Reusability** - LLM API can be used by other endpoints
3. **Centralized Configuration** - All LLM settings in one place
4. **Better Error Handling** - Consistent error responses
5. **Easier Testing** - Can mock LLM API independently

## Request Flow

### Step 1: Frontend Calls Users API

```javascript
// Frontend: UserProfile.jsx
const response = await axios.post(
  `http://localhost:8000/users/${userId}/analyze-skills`
)
```

### Step 2: Users API Prepares Data

```python
# Backend: app/api/users.py
@router.post("/{user_id}/analyze-skills")
async def analyze_user_skills(user_id: int, db: Session):
    # 1. Get user from database
    user = db.query(User).filter(User.id == user_id).first()

    # 2. Get all user's skills
    assessments = db.query(Assessment).filter(
        Assessment.user_id == user_id
    ).all()

    # 3. Build skills summary
    skills_summary = "\n".join([
        f"- {skill['name']} ({skill['category']}): {skill['proficiency']}"
        for skill in skills_data
    ])

    # 4. Create prompts
    system_prompt = "You are an expert career advisor..."
    user_prompt = f"Analyze the following employee profile:\n{skills_summary}..."
```

### Step 3: Users API Calls LLM API

```python
# Backend: app/api/users.py (continued)

    # Call LLM API endpoint (not direct client)
    async with httpx.AsyncClient() as client:
        llm_response = await client.post(
            "http://localhost:8000/api/llm/chat",
            json={
                "user_content": user_prompt,
                "system_content": system_prompt,
                "max_tokens": 2000
            },
            timeout=60.0
        )
```

**Request to LLM API:**
```json
POST http://localhost:8000/api/llm/chat
Content-Type: application/json

{
  "user_content": "Analyze the following employee profile:\n\n**Employee:** Ana Smith\n**Role:** employee\n**Current Skills (9 total):**\n\n- Backend (technical): ADVANCED\n- Power BI (technical): BEGINNER\n...",
  "system_content": "You are an expert career advisor and skills analyst.\nAnalyze the employee's current skills and provide actionable insights...",
  "max_tokens": 2000,
  "model": null
}
```

### Step 4: LLM API Calls Bosch LLM Farm

```python
# Backend: app/api/llm.py
@router.post("/chat")
async def chat_completion(request: ChatRequest):
    response = await llm_client.chat_completion(
        user_content=request.user_content,
        system_content=request.system_content,
        model=request.model,
        max_tokens=request.max_tokens
    )
    return response
```

```python
# Backend: app/services/llm_client.py
async def chat_completion(self, user_content, system_content, model, max_tokens):
    endpoint_url = f"{self.base_url}/publishers/anthropic/models/{model}:rawPredict"

    payload = {
        "anthropic_version": "vertex-2023-10-16",
        "messages": [{"role": "user", "content": user_content}],
        "max_tokens": max_tokens,
        "system": system_content
    }

    headers = {
        "Authorization": f"Bearer {self.api_key}",
        "Content-Type": "application/json"
    }

    async with httpx.AsyncClient(timeout=60.0) as client:
        response = await client.post(endpoint_url, json=payload, headers=headers)
        return response.json()
```

**Request to Bosch LLM Farm:**
```json
POST https://llm-farm.bosch.com/publishers/anthropic/models/claude-sonnet-4-5@20250929:rawPredict
Authorization: Bearer YOUR_API_KEY
Content-Type: application/json

{
  "anthropic_version": "vertex-2023-10-16",
  "max_tokens": 2000,
  "system": "You are an expert career advisor and skills analyst...",
  "messages": [
    {
      "role": "user",
      "content": "Analyze the following employee profile:\n\n**Employee:** Ana Smith..."
    }
  ]
}
```

### Step 5: Response Flows Back

```
Bosch LLM Farm → LLM Service → LLM API → Users API → Frontend
```

**LLM Farm Response:**
```json
{
  "id": "msg_01ABC...",
  "type": "message",
  "role": "assistant",
  "model": "claude-sonnet-4-5@20250929",
  "content": [
    {
      "type": "text",
      "text": "# Skill Gaps Analysis\n\n**Important Skills Missing:**\n- Cloud Computing..."
    }
  ],
  "usage": {
    "input_tokens": 412,
    "output_tokens": 856
  }
}
```

**Users API Response:**
```json
{
  "user": {
    "id": 1,
    "name": "Ana Smith",
    "email": "ana.smith@bosch.com",
    "role": "employee"
  },
  "skills_analyzed": 9,
  "skills_by_category": {
    "technical": 7,
    "domain_knowledge": 2
  },
  "analysis": "# Skill Gaps Analysis\n\n**Important Skills Missing:**\n- Cloud Computing...",
  "model_used": "claude-sonnet-4-5@20250929"
}
```

## Complete Flow Diagram

```
┌──────────────────────────────────────────────────────────────────────┐
│                          Frontend (React)                             │
│  UserProfile.jsx: Click "Analyze Skills"                             │
└────────────────────────────────┬─────────────────────────────────────┘
                                 │
                                 │ POST /users/1/analyze-skills
                                 ▼
┌──────────────────────────────────────────────────────────────────────┐
│                    Backend - Users API                                │
│  app/api/users.py                                                     │
│  ┌────────────────────────────────────────────────────────────────┐ │
│  │ 1. Get user from database                                       │ │
│  │ 2. Get all skills/assessments                                   │ │
│  │ 3. Build skills_summary string                                  │ │
│  │ 4. Create system_prompt & user_prompt                          │ │
│  └────────────────────────────────────────────────────────────────┘ │
└────────────────────────────────┬─────────────────────────────────────┘
                                 │
                                 │ POST /api/llm/chat
                                 │ {
                                 │   user_content: "Analyze...",
                                 │   system_content: "You are...",
                                 │   max_tokens: 2000
                                 │ }
                                 ▼
┌──────────────────────────────────────────────────────────────────────┐
│                     Backend - LLM API                                 │
│  app/api/llm.py                                                       │
│  ┌────────────────────────────────────────────────────────────────┐ │
│  │ 1. Validate request                                             │ │
│  │ 2. Call llm_client.chat_completion()                           │ │
│  └────────────────────────────────────────────────────────────────┘ │
└────────────────────────────────┬─────────────────────────────────────┘
                                 │
                                 │ Call LLM service
                                 ▼
┌──────────────────────────────────────────────────────────────────────┐
│                    Backend - LLM Client Service                       │
│  app/services/llm_client.py                                          │
│  ┌────────────────────────────────────────────────────────────────┐ │
│  │ 1. Build endpoint URL                                           │ │
│  │ 2. Prepare Anthropic format payload                            │ │
│  │ 3. Add authentication headers                                   │ │
│  │ 4. Send HTTP request                                            │ │
│  └────────────────────────────────────────────────────────────────┘ │
└────────────────────────────────┬─────────────────────────────────────┘
                                 │
                                 │ POST /publishers/anthropic/models/...
                                 │ Authorization: Bearer API_KEY
                                 │ {
                                 │   anthropic_version: "...",
                                 │   messages: [...],
                                 │   system: "...",
                                 │   max_tokens: 2000
                                 │ }
                                 ▼
┌──────────────────────────────────────────────────────────────────────┐
│                    Bosch LLM Farm (External)                          │
│  Google Vertex AI → Anthropic Claude                                 │
│  ┌────────────────────────────────────────────────────────────────┐ │
│  │ 1. Authenticate request                                         │ │
│  │ 2. Route to Claude model                                        │ │
│  │ 3. Process prompt                                               │ │
│  │ 4. Generate analysis                                            │ │
│  │ 5. Return response                                              │ │
│  └────────────────────────────────────────────────────────────────┘ │
└──────────────────────────────────────────────────────────────────────┘
                                 │
                                 │ Response flows back up
                                 │
                                 ▼
                            [Frontend displays]
```

## API Endpoints Involved

### 1. Frontend → Users API
```
POST http://localhost:8000/users/{user_id}/analyze-skills
```

### 2. Users API → LLM API (Internal)
```
POST http://localhost:8000/api/llm/chat
```

### 3. LLM Service → Bosch LLM Farm
```
POST https://llm-farm.bosch.com/publishers/anthropic/models/claude-sonnet-4-5@20250929:rawPredict
```

## Benefits of This Architecture

### 1. **Separation of Concerns**
- Users API: Handles user data and business logic
- LLM API: Handles AI/ML requests
- Clean boundaries between layers

### 2. **Reusability**
- LLM API can be used by:
  - Users analysis
  - Skills recommendations
  - Gap analysis
  - Career suggestions
  - Any other AI features

### 3. **Error Handling**
```python
# Users API handles LLM API errors gracefully
try:
    llm_response = await client.post("http://localhost:8000/api/llm/chat", ...)
except httpx.HTTPStatusError as e:
    if "not configured" in error_detail:
        raise HTTPException(503, "LLM not configured")
```

### 4. **Testing**
```python
# Can mock LLM API in tests
@pytest.fixture
def mock_llm_api(mocker):
    mocker.patch('httpx.AsyncClient.post', return_value=mock_response)

def test_analyze_skills(mock_llm_api):
    response = client.post("/users/1/analyze-skills")
    assert response.status_code == 200
```

### 5. **Monitoring**
- Track LLM API usage separately
- Monitor response times at each layer
- Debug issues more easily

## Configuration

All LLM configuration in one place:

```env
# .env
LLM_FARM_BASE_URL=https://llm-farm.bosch.com
LLM_FARM_API_KEY=your-secret-key
LLM_DEFAULT_MODEL=claude-sonnet-4-5@20250929
LLM_DEFAULT_MAX_TOKENS=2000
```

## Error Handling Chain

```
Frontend Error → Users API Error → LLM API Error → LLM Farm Error
```

**Example Error Flow:**
1. LLM Farm returns 500 (service down)
2. LLM Service throws exception
3. LLM API returns 500 to Users API
4. Users API catches and returns 503 to Frontend
5. Frontend shows: "LLM service unavailable"

## Summary

✅ **Layered Architecture** - Clean separation
✅ **REST API Call** - Users API → LLM API (not direct import)
✅ **Reusable LLM API** - Can be used by multiple features
✅ **Better Error Handling** - Proper HTTP status codes
✅ **Easier Testing** - Mock at API level
✅ **Centralized Config** - One place for LLM settings

This architecture makes the codebase more maintainable and scalable! 🚀
