# Quick Start Guide - Employee Directory & Import

## 🚀 Getting Started in 5 Minutes

### Step 1: Start the Backend
```bash
cd backend
python3 run.py
```
Server starts at: http://localhost:8000

### Step 2: Start the Frontend
```bash
cd frontend
npm run dev
```
App opens at: http://localhost:5173

### Step 3: Import Employee Data
1. Go to http://localhost:5173/import
2. Drag and drop `plw_employee_taging-test.xlsx`
3. Click "Upload & Import"
4. Wait for success message

### Step 4: View Employees
1. Click **"Employees"** in the navigation menu
2. Browse the employee directory
3. Click **"View Profile"** on any employee
4. See their skills and proficiency levels

## 📋 Main Features

### 🔹 Import Data
**URL**: http://localhost:5173/import
- Upload Excel files with employee skills
- View import statistics
- See database totals

### 🔹 Employee Directory
**URL**: http://localhost:5173/employees
- Search employees by name or email
- View employee cards with skills count
- Click to see detailed profiles

### 🔹 Skills Catalog
**URL**: http://localhost:5173/skills
- Browse all skills
- Click "View Users" on any skill
- See who has that skill and their proficiency

## 🎯 Quick Actions

### Import New Data
```
Navigate → Import Data → Upload Excel → Import
```

### Find an Employee
```
Navigate → Employees → Search → View Profile
```

### Find Expertise
```
Navigate → Skills Catalog → Find Skill → View Users
```

## 📊 What You'll See

After importing the test data:
- **3 employees** (Ana Smith, John Dow, Bobi Jay)
- **7 competencies** (Backend, Power BI, Java, etc.)
- **9 assessments** (employee-skill mappings)

## 🔧 API Endpoints

All accessible at http://localhost:8000/docs

- `POST /import/planisware` - Import Excel
- `GET /import/status` - Database stats
- `GET /users` - List employees
- `GET /users/{id}` - Employee details
- `GET /users/{id}/skills` - Employee skills
- `GET /users/search/by-skill/{id}` - Find users by skill

## 💡 Tips

1. **Use the search** - Type in the Employee Directory search box for quick finding
2. **Check proficiency** - Color-coded badges show skill levels
3. **Export profiles** - Click "Export PDF" in user profiles
4. **Find experts** - Use Skills Catalog to find who has specific skills

## 🎨 Navigation Map

```
Home
├── Employees ⭐ (NEW)
│   └── Click user → View Profile Modal
├── Career Paths
├── Skills Catalog ⭐ (ENHANCED)
│   └── Click "View Users" → Users with Skill Modal
├── Gap Analysis
├── Progress Tracker
├── Assessment
└── Import Data ⭐ (NEW)
```

## ✅ Checklist

- [ ] Backend running on port 8000
- [ ] Frontend running on port 5173
- [ ] Import test data successful
- [ ] Can view employee directory
- [ ] Can search employees
- [ ] Can view employee profiles
- [ ] Can see users by skill

## 🆘 Troubleshooting

**Problem**: Can't import Excel file
- **Solution**: Install dependencies: `pip install pandas openpyxl werkzeug`

**Problem**: Employee directory is empty
- **Solution**: Import data first via Import Data page

**Problem**: Search not working
- **Solution**: Check backend is running and responding at http://localhost:8000

**Problem**: Modal won't close
- **Solution**: Click the X button or click outside the modal

## 📖 Full Documentation

- **Import Guide**: See `IMPORT_GUIDE.md`
- **Import Feature**: See `IMPORT_FEATURE.md`
- **Employee Directory**: See `EMPLOYEE_DIRECTORY_COMPLETE.md`
- **Proposal**: See `USER_DIRECTORY_PROPOSAL.md`

## 🎉 You're Ready!

Everything is set up and ready to use. Start by importing data, then explore the employee directory!
