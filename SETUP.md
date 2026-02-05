# GrowthPath Setup Guide

## Prerequisites

- Python 3.9+ installed
- Node.js 18+ and npm installed
- Git

## Backend Setup

1. Navigate to the backend directory:
```bash
cd backend
```

2. Create a virtual environment:
```bash
python -m venv venv
```

3. Activate the virtual environment:
- On macOS/Linux:
  ```bash
  source venv/bin/activate
  ```
- On Windows:
  ```bash
  venv\Scripts\activate
  ```

4. Install dependencies:
```bash
pip install -r requirements.txt
```

5. Create a `.env` file (optional, defaults to SQLite):
```bash
cp .env.example .env
```

6. Run the backend server:
```bash
python run.py
```

The API will be available at `http://localhost:8000`
API documentation at `http://localhost:8000/docs`

## Frontend Setup

1. Navigate to the frontend directory:
```bash
cd frontend
```

2. Install dependencies:
```bash
npm install
```

3. Start the development server:
```bash
npm run dev
```

The frontend will be available at `http://localhost:3000`

## Initial Data Setup

To populate the database with sample competencies, you can use the API:

1. Open `http://localhost:8000/docs`
2. Use the POST `/competencies/` endpoint to add competencies

Example competencies:
```json
{
  "name": "Python Programming",
  "description": "Proficiency in Python language and ecosystem",
  "category": "technical"
}
```

Or use the provided seed script (coming soon).

## Project Structure

```
growthpath/
├── backend/
│   ├── app/
│   │   ├── api/           # API endpoints
│   │   ├── core/          # Config and database
│   │   ├── models/        # SQLAlchemy models
│   │   └── schemas/       # Pydantic schemas
│   ├── requirements.txt
│   └── run.py
├── frontend/
│   ├── src/
│   │   ├── components/    # React components
│   │   ├── pages/         # Page components
│   │   ├── services/      # API calls
│   │   └── styles/        # CSS files
│   └── package.json
└── README.md
```

## Next Steps

1. Add sample competencies via the API
2. Test the assessment form at `/assessment`
3. Implement user authentication
4. Add data visualization for assessments
