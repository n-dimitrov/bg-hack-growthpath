# Start GrowthPath Application

## Quick Start (Easiest)

### 1. Start Backend
```bash
cd backend
./start.sh
```

The backend will start on **http://localhost:8000**

### 2. Start Frontend (Optional)
```bash
cd frontend
npm run dev
```

The frontend will start on **http://localhost:3000**

### 3. Open LLM Tester
Open in browser:
```
frontend/public/llm-tester.html
```

Or direct path:
```bash
open frontend/public/llm-tester.html
```

---

## Manual Start

### Backend
```bash
cd backend

# Activate virtual environment (if exists)
source venv/bin/activate  # Mac/Linux
# OR
venv\Scripts\activate  # Windows

# Install dependencies (first time only)
pip install -r requirements.txt

# Start server
python run.py
```

### Frontend (React App)
```bash
cd frontend
npm install  # First time only
npm run dev
```

---

## Verify Everything is Running

### Check Backend
```bash
curl http://localhost:8000/api/llm/health
```

Expected response:
```json
{
  "status": "configured",
  "has_api_key": true
}
```

### Check LLM API
```bash
curl -X POST "http://localhost:8000/api/llm/chat" \
  -H "Content-Type: application/json" \
  -d '{"user_content": "Hello"}'
```

---

## URLs

- **Backend API**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs
- **Frontend App**: http://localhost:3000
- **LLM Tester**: `frontend/public/llm-tester.html`

---

## Troubleshooting

### Port already in use
If port 8000 is busy:
```bash
# Find process using port 8000
lsof -ti:8000

# Kill it
kill -9 $(lsof -ti:8000)
```

### Backend won't start
```bash
cd backend
pip install --upgrade pydantic pydantic-settings
python run.py
```

### Frontend won't start
```bash
cd frontend
rm -rf node_modules package-lock.json
npm install
npm run dev
```
