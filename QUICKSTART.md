# GrowthPath Quick Start Guide

## 🚀 Getting Started

Follow these steps to get your GrowthPath application running with career framework and skills data.

## Step 1: Seed the Database

First, populate the database with career framework and skills data:

```bash
cd backend
python seed_career_data.py
```

This will:
- ✅ Create database tables
- ✅ Load career framework (7 career levels)
- ✅ Load 19 competency areas
- ✅ Load 300+ skills from TechMasterData and Skillsets
- ✅ Set up the complete data structure

Expected output:
```
📊 Seeding Career Framework...
  ✓ Added 7 career levels
  ✓ Added 10 competency areas
  ✓ Added 50 competency expectations
  ...
✅ Database seeding completed successfully!
```

## Step 2: Start the Backend

```bash
# Make sure you're in the backend directory
cd backend

# Activate virtual environment (if using one)
source venv/bin/activate  # On macOS/Linux
# or
venv\Scripts\activate  # On Windows

# Start the FastAPI server
python run.py
```

Backend will be available at: **http://localhost:8000**
API Documentation: **http://localhost:8000/docs**

## Step 3: Start the Frontend

```bash
# In a new terminal, go to frontend directory
cd frontend

# Install dependencies (if not done already)
npm install

# Start development server
npm run dev
```

Frontend will be available at: **http://localhost:5173** (or 3000)

## Step 4: Test the API Endpoints

Open http://localhost:8000/docs and try these endpoints:

### Career Framework Endpoints

1. **GET /api/career/paths**
   - Returns all career tracks (Software Engineer, Software Architect)

2. **GET /api/career/paths/software_engineer/PC08**
   - Get details for Senior Software Engineer level

3. **POST /api/career/skills-gap**
   - Body: `{"current_level": "PC07", "target_level": "PC08"}`
   - Returns competency gaps

4. **POST /api/career/development-plan**
   - Body: `{"user_id": 1, "current_level": "PC07", "target_level": "PC08"}`
   - Generates development plan

### Skills Endpoints

1. **GET /api/skills/catalog**
   - Returns all skills

2. **GET /api/skills/categories**
   - Returns skill categories

3. **GET /api/skills/recommend/PC08**
   - Get recommended skills for Senior level

## Step 5: Use the React Components

### Import Components in Your App

```jsx
// frontend/src/App.jsx
import CareerPathVisualizer from './components/CareerPathVisualizer';
import SkillsCatalog from './components/SkillsCatalog';
import Dashboard from './components/Dashboard';

function App() {
  return (
    <div className="App">
      <nav>
        <a href="#career">Career Paths</a>
        <a href="#skills">Skills</a>
        <a href="#dashboard">Dashboard</a>
      </nav>

      <section id="career">
        <CareerPathVisualizer />
      </section>

      <section id="skills">
        <SkillsCatalog />
      </section>

      <section id="dashboard">
        <Dashboard />
      </section>
    </div>
  );
}

export default App;
```

## 🎯 What Each Component Does

### 1. CareerPathVisualizer
**Purpose**: Visualize career progression paths
- Shows Software Engineer track (PC06 → PC10)
- Shows Software Architect track (PC09 → PC10)
- Interactive level cards with competency links
- Beautiful gradient design

**Usage**:
```jsx
import CareerPathVisualizer from './components/CareerPathVisualizer';

<CareerPathVisualizer />
```

### 2. SkillsCatalog
**Purpose**: Browse and search all available skills
- Search 300+ skills
- Filter by category and type
- View skill details and descriptions
- Shows Standard/Advanced/Niche badges

**Usage**:
```jsx
import SkillsCatalog from './components/SkillsCatalog';

<SkillsCatalog />
```

### 3. Dashboard
**Purpose**: Skills gap analysis and development planning
- Compare current vs target levels
- See detailed competency gaps
- Generate development plans
- Track learning objectives

**Usage**:
```jsx
import Dashboard from './components/Dashboard';

<Dashboard />
```

## 📊 Sample Workflows

### Workflow 1: View Career Path
1. Open CareerPathVisualizer
2. Select "Software Engineer Track"
3. See progression from Junior (PC06) to Principal (PC10)
4. Click "View Competencies" on any level

### Workflow 2: Explore Skills
1. Open SkillsCatalog
2. Search for "React" or filter by "Web Development"
3. Browse skill cards with descriptions
4. Note the skill categories (Standard/Advanced/Niche)

### Workflow 3: Analyze Skills Gap
1. Open Dashboard
2. Select Current Level: PC07 (Software Engineer)
3. Select Target Level: PC08 (Senior Software Engineer)
4. Review the competency gaps
5. Click "Generate Development Plan"

## 🔧 API Examples

### Get Career Paths
```bash
curl http://localhost:8000/api/career/paths
```

### Calculate Skills Gap
```bash
curl -X POST "http://localhost:8000/api/career/skills-gap?current_level=PC07&target_level=PC08"
```

### Get Skills Catalog
```bash
curl "http://localhost:8000/api/skills/catalog?search=javascript"
```

### Recommend Skills for Level
```bash
curl http://localhost:8000/api/skills/recommend/PC08
```

## 📁 File Structure

```
growthpath/
├── backend/
│   ├── app/
│   │   ├── api/
│   │   │   ├── career.py      # Career framework endpoints
│   │   │   └── skills.py      # Skills catalog endpoints
│   │   └── models/
│   │       └── career.py      # Database models
│   └── seed_career_data.py    # Database seeding script
├── frontend/
│   └── src/
│       └── components/
│           ├── CareerPathVisualizer.jsx
│           ├── SkillsCatalog.jsx
│           └── Dashboard.jsx
├── CareerFramework.json       # Career progression data
├── Skillsets.json            # Data-focused skills
└── TechMasterData.json       # Technology skills
```

## 🎨 Customization

### Change API URL
Edit the fetch URLs in components:
```jsx
const API_URL = 'http://localhost:8000';  // Change this
```

### Add New Career Tracks
Edit `CareerFramework.json` and re-run seed script.

### Add New Skills
Edit `TechMasterData.json` or `Skillsets.json` and re-seed.

## 🐛 Troubleshooting

### Database errors
```bash
# Re-seed the database
cd backend
python seed_career_data.py
# Answer 'yes' when prompted to clear and re-seed
```

### CORS errors
Make sure backend CORS settings include your frontend URL:
```python
# backend/app/main.py
allow_origins=["http://localhost:3000", "http://localhost:5173"]
```

### Import errors
```bash
# Re-install backend dependencies
cd backend
pip install -r requirements.txt

# Re-install frontend dependencies
cd frontend
npm install
```

## 📚 Next Steps

1. ✅ Customize the styling in CSS files
2. ✅ Add user authentication
3. ✅ Create user profiles
4. ✅ Track user progress over time
5. ✅ Add skill recommendations based on role
6. ✅ Build reporting and analytics

## 🎉 You're Ready!

Your GrowthPath application now has:
- ✅ Complete career framework
- ✅ 300+ skills catalog
- ✅ Skills gap analysis
- ✅ Development planning
- ✅ Beautiful UI components
- ✅ RESTful API

Start building your competence management system! 🚀
