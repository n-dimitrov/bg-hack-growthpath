# Frontend Usage Guide

## 🎯 How to Use Your GrowthPath Frontend

### Current Status
✅ Frontend is running at: **http://localhost:3001**
✅ Components are integrated into the app
✅ Navigation is set up with routing

---

## 📱 Available Pages

Open http://localhost:3001 in your browser and navigate to:

### 1. **Career Paths**
**URL:** http://localhost:3001/career-paths

**What it does:**
- Shows interactive career progression ladder
- Displays Software Engineer track (5 levels)
- Displays Software Architect track (2 levels)
- Click on level cards to see details

**Features:**
- Visual career ladder with arrows
- Pay class badges (PC06-PC10)
- Impact scope descriptions
- Switch between Engineer and Architect tracks

---

### 2. **Skills Catalog**
**URL:** http://localhost:3001/skills

**What it does:**
- Browse all 315 technology skills
- Search skills by name
- Filter by category or type
- View skill details and descriptions

**How to use:**
1. Use search box to find specific skills (try "react", "python", "database")
2. Filter by Type: All Skills / Technology Skills / Data Skills
3. Filter by Category: Select from 48+ categories
4. Click on skill cards to see details

**Features:**
- Real-time search
- Category grouping
- Skill badges (Standard/Advanced/Niche)
- Responsive grid layout

---

### 3. **Gap Analysis Dashboard**
**URL:** http://localhost:3001/gap-analysis

**What it does:**
- Analyze skills gaps between career levels
- Compare current vs target level
- Generate development plans
- See detailed competency differences

**How to use:**
1. Select your **Current Level** (e.g., PC07 - Software Engineer)
2. Select your **Target Level** (e.g., PC08 - Senior Software Engineer)
3. View the competency gaps automatically
4. Click "Generate Development Plan" to create a 6-month plan

**Features:**
- Interactive level selectors
- Statistics cards showing gap count
- Detailed gap comparison (current vs required)
- Auto-generated development plans
- Priority assignment (High/Medium/Low)

---

## 🎨 Component Overview

### CareerPathVisualizer
```jsx
<CareerPathVisualizer />
```
**Props:** None (standalone component)

**Styling:** Beautiful gradient cards with hover effects

---

### SkillsCatalog
```jsx
<SkillsCatalog />
```
**Props:** None (standalone component)

**Features:**
- Searches backend API: `GET /api/skills/catalog`
- Filters work in real-time
- Displays grouped by category

---

### Dashboard (Gap Analysis)
```jsx
<Dashboard />
```
**Props:** None (standalone component)

**API Calls:**
- Skills Gap: `POST /api/career/skills-gap`
- Development Plan: `POST /api/career/development-plan`

---

## 🔧 How It Works

### 1. Components Auto-Connect to Backend

All components are configured to connect to:
```
http://localhost:8000
```

No additional configuration needed!

### 2. Navigation

The app uses React Router. Click the navigation links in the header:
- **Home** → Original dashboard
- **Career Paths** → CareerPathVisualizer
- **Skills Catalog** → SkillsCatalog
- **Gap Analysis** → Skills gap dashboard
- **Assessment** → Original assessment form

### 3. Real-Time Updates

When you:
- Search for skills → API call happens instantly
- Select levels → Gap analysis runs automatically
- Generate plan → Creates entry in database

---

## 📊 Try These Demo Flows

### Demo Flow 1: Explore Career Path
1. Go to http://localhost:3001/career-paths
2. View the Software Engineer track
3. See progression: Junior → Engineer → Senior → Lead → Principal
4. Switch to Architect track
5. Notice different requirements

### Demo Flow 2: Find Skills
1. Go to http://localhost:3001/skills
2. Search for "React"
3. See 3 React-related skills
4. Try "Python", "Java", "Database"
5. Filter by category: "Web Development"

### Demo Flow 3: Analyze Gap
1. Go to http://localhost:3001/gap-analysis
2. Select Current: PC07 (Software Engineer)
3. Select Target: PC08 (Senior Software Engineer)
4. Review 8 identified gaps
5. Read current vs required differences
6. Click "Generate Development Plan"
7. See 6-month plan with priorities

---

## 🎨 Customization

### Change Colors
Edit the CSS files in `src/components/`:
- `CareerPathVisualizer.css`
- `SkillsCatalog.css`
- `Dashboard.css`

### Change API URL
If backend is on different port, edit the components:
```jsx
// Change this in each component
const API_URL = 'http://localhost:8000';
```

### Add More Features
The components are modular. Add features like:
- Save favorite skills
- Track progress over time
- Compare multiple levels
- Export development plans

---

## 🐛 Troubleshooting

### Components not loading?
Check browser console (F12) for errors.

**Common issues:**
1. Backend not running → Start with `python run.py`
2. CORS errors → Check backend CORS settings
3. 404 errors → Verify API endpoints

### API not responding?
1. Verify backend is running: http://localhost:8000/health
2. Check API docs: http://localhost:8000/docs
3. Test endpoint in browser or curl

### Styling issues?
1. Check if CSS files are imported
2. Clear browser cache (Ctrl+Shift+R)
3. Verify CSS file paths

---

## 📱 Responsive Design

All components work on:
- ✅ Desktop (1920px+)
- ✅ Laptop (1366px)
- ✅ Tablet (768px)
- ✅ Mobile (375px)

Test by resizing browser window!

---

## 🎯 For Your Hackathon Demo

### Recommended Demo Order (10 minutes):

**1. Career Paths (2 min)**
- Show the visual ladder
- Explain the progression
- Highlight real Bosch framework

**2. Skills Catalog (2 min)**
- Search functionality
- Show 315+ skills
- Filter demonstration

**3. Gap Analysis (4 min)**
- Select levels (PC07 → PC08)
- Show 8 gaps identified
- Explain current vs required
- Generate development plan
- Show prioritized objectives

**4. API Documentation (2 min)**
- Open http://localhost:8000/docs
- Show interactive API
- Test an endpoint live

---

## 🚀 Quick Start Summary

1. **Backend running?** → http://localhost:8000 ✅
2. **Frontend running?** → http://localhost:3001 ✅
3. **Open browser** → http://localhost:3001
4. **Navigate pages** → Use header links
5. **Test features** → Follow demo flows above

---

## 💡 Tips

- Keep browser console open to see API calls
- Use "React Developer Tools" browser extension
- Test on different screen sizes
- Prepare sample searches: "react", "python", "database"
- Know the gap analysis story (PC07 → PC08)

---

## 📞 Need Help?

Check the documentation:
- `QUICKSTART.md` - Setup instructions
- `IMPLEMENTATION_SUMMARY.md` - Technical details
- `DEMO_RESULTS.md` - API test results
- `INTEGRATION_GUIDE.md` - Code examples

---

**You're ready to demo! Good luck! 🎉**
