# User Directory & Profile Viewer - Proposal

## Problem Statement
After importing employee data from Planisware Excel files, we need a way to:
1. View all imported users
2. Select a specific user
3. See their complete profile including all skills and competencies
4. View proficiency levels for each skill

## Proposed Solutions

### Option 1: Employee Directory with Profile View (Recommended)

**Description**: Create a dedicated "Employee Directory" page with a searchable list of users and detailed profile view.

**Features:**
- Searchable/filterable employee list
- User cards with basic info (name, email, total skills)
- Click to view detailed profile in modal or separate page
- Profile shows all competencies grouped by category
- Visual proficiency indicators
- Export user profile to PDF

**User Flow:**
```
Navigate to "Employee Directory"
  → See list of all employees
  → Search/filter by name, role, location
  → Click on employee card
  → View detailed profile with all skills
  → See proficiency levels and categories
```

**UI Components:**
```
┌─────────────────────────────────────────┐
│ Employee Directory                       │
│ ┌─────────────────────────────────────┐ │
│ │ Search: [_________________] 🔍      │ │
│ └─────────────────────────────────────┘ │
│                                          │
│ ┌─────────────┐ ┌─────────────┐        │
│ │ Ana Smith   │ │ John Dow    │        │
│ │ 9 skills    │ │ 3 skills    │        │
│ │ Data Eng.   │ │ Data Sci.   │        │
│ └─────────────┘ └─────────────┘        │
└─────────────────────────────────────────┘

Click user →

┌─────────────────────────────────────────┐
│ Ana Smith's Profile                      │
│ ana.smith@bosch.com                     │
│                                          │
│ TECHNICAL SKILLS (7)                    │
│ ● Backend          [████████] Advanced  │
│ ● Java             [██████  ] Intermed. │
│                                          │
│ DOMAIN KNOWLEDGE (2)                     │
│ ● SAP Datasphere   [████████] Advanced  │
└─────────────────────────────────────────┘
```

**Pros:**
- ✅ Dedicated space for user management
- ✅ Easy to browse all employees
- ✅ Can add filtering/sorting
- ✅ Clear separation from other features

**Cons:**
- ❌ Requires creating new page and components
- ❌ More development time

---

### Option 2: Enhanced Import Results Page

**Description**: Add user viewing capability directly to the import page.

**Features:**
- After import, show "View Imported Users" button
- Expandable list showing users just imported
- Click to expand and see user's skills inline
- Quick way to verify import results

**User Flow:**
```
Import Excel file
  → View import results
  → Click "View Imported Users"
  → See list with expandable details
  → Click user to expand skills
```

**Pros:**
- ✅ Quick verification after import
- ✅ Minimal additional development
- ✅ Contextual to import process

**Cons:**
- ❌ Only shows recently imported users
- ❌ Not a general-purpose user directory
- ❌ Limited search/filter capabilities

---

### Option 3: Dashboard Widget

**Description**: Add a "Team Overview" widget to the main dashboard.

**Features:**
- Dashboard card showing user stats
- Top skills across team
- Click "View All Users" to see directory
- Integration with existing dashboard

**User Flow:**
```
Open Dashboard
  → See "Team Overview" widget
  → Shows user count, top skills
  → Click "View Details"
  → Opens user directory modal
```

**Pros:**
- ✅ Visible from main dashboard
- ✅ Provides team-level insights
- ✅ Non-intrusive

**Cons:**
- ❌ Still needs full directory page
- ❌ Two-step process to see users

---

### Option 4: Skills Catalog Enhancement

**Description**: Enhance existing Skills Catalog to show which users have each skill.

**Features:**
- In Skills Catalog, add "Who has this skill?"
- Click skill → see all users with that skill
- Reverse lookup (skill → users)
- Show proficiency distribution

**User Flow:**
```
Go to Skills Catalog
  → Click on a skill (e.g., "Python")
  → See all users with Python
  → View their proficiency levels
  → Click user to see full profile
```

**Pros:**
- ✅ Skills-first approach
- ✅ Good for finding expertise
- ✅ Enhances existing feature

**Cons:**
- ❌ Not user-centric view
- ❌ Hard to browse all users
- ❌ Still needs user profile page

---

## Recommended Implementation: Option 1 + 4 (Hybrid)

**Why this combination?**
1. **Option 1** (Employee Directory) provides the main user browsing interface
2. **Option 4** (Skills Catalog Enhancement) enables skill-based user discovery

**Implementation Plan:**

### Phase 1: Backend API (1-2 hours)
1. Create `/api/users` endpoint
   - GET `/users` - List all users with pagination
   - GET `/users/{id}` - Get user details
   - GET `/users/{id}/skills` - Get user's skills/assessments
   - GET `/users/search?q=name` - Search users

### Phase 2: Employee Directory Page (2-3 hours)
1. Create `EmployeeDirectory.jsx` component
2. User list with search/filter
3. User cards showing:
   - Name, email
   - Number of skills
   - Role (if available)
   - Location (if available)
4. Click to view profile modal

### Phase 3: User Profile Modal (1-2 hours)
1. Create `UserProfile.jsx` component
2. Show user details:
   - Basic info (name, email, location)
   - Skills grouped by category
   - Proficiency bars/badges
   - Total skills count
3. Export to PDF option

### Phase 4: Skills Catalog Enhancement (1 hour)
1. Update Skills Catalog
2. Add "View Users" button on each skill
3. Show users with that skill and their levels

## Data Structure

### API Response Example

**GET /api/users**
```json
{
  "total": 3,
  "users": [
    {
      "id": 1,
      "name": "Ana Smith",
      "email": "ana.smith@bosch.com",
      "role": "employee",
      "skills_count": 9,
      "location": "VA",
      "country": "CA",
      "region": "APA"
    }
  ]
}
```

**GET /api/users/1/skills**
```json
{
  "user": {
    "id": 1,
    "name": "Ana Smith",
    "email": "ana.smith@bosch.com"
  },
  "skills": [
    {
      "category": "technical",
      "competencies": [
        {
          "id": 1,
          "name": "Backend",
          "proficiency_level": "advanced",
          "description": "SAP BW Modeling & Reporting",
          "assessed_at": "2024-01-15T10:30:00Z"
        }
      ]
    }
  ],
  "total_skills": 9,
  "by_category": {
    "technical": 7,
    "domain_knowledge": 2
  }
}
```

## Visual Mockup

### Employee Directory Page
```
┌────────────────────────────────────────────────────────┐
│  🚀 GrowthPath > Employee Directory                    │
├────────────────────────────────────────────────────────┤
│                                                         │
│  [Search employees...                    ] 🔍          │
│                                                         │
│  Showing 3 employees                                   │
│                                                         │
│  ┌───────────────────┐  ┌───────────────────┐         │
│  │  Ana Smith         │  │  John Dow          │         │
│  │  ───────────────── │  │  ───────────────── │         │
│  │  📧 ana.smith@...  │  │  📧 john.dow@...   │         │
│  │  📍 VA, CA         │  │  📍 VA, CA         │         │
│  │  💼 Employee       │  │  💼 Employee       │         │
│  │  ✨ 9 skills      │  │  ✨ 3 skills       │         │
│  │                    │  │                    │         │
│  │  [View Profile]    │  │  [View Profile]    │         │
│  └───────────────────┘  └───────────────────┘         │
└────────────────────────────────────────────────────────┘
```

### User Profile Modal
```
┌────────────────────────────────────────────────────────┐
│  Ana Smith                                      [X]     │
│  ana.smith@bosch.com                                   │
│  Employee • VA, CA • APA Region                        │
├────────────────────────────────────────────────────────┤
│                                                         │
│  📊 Skills Overview                                    │
│  ┌──────────────────────────────────────────────────┐ │
│  │  9 Total Skills                                   │ │
│  │  7 Technical • 2 Domain Knowledge                │ │
│  └──────────────────────────────────────────────────┘ │
│                                                         │
│  🔧 TECHNICAL SKILLS (7)                              │
│  ┌──────────────────────────────────────────────────┐ │
│  │  Backend                                          │ │
│  │  SAP BW Modeling & Reporting                      │ │
│  │  [████████░░] Advanced                            │ │
│  ├──────────────────────────────────────────────────┤ │
│  │  Java                                             │ │
│  │  SAP BW on HANA (Data)                           │ │
│  │  [██████░░░░] Intermediate                        │ │
│  └──────────────────────────────────────────────────┘ │
│                                                         │
│  💼 DOMAIN KNOWLEDGE (2)                              │
│  ┌──────────────────────────────────────────────────┐ │
│  │  SAP Datasphere (Data)                           │ │
│  │  [████████░░] Advanced                            │ │
│  └──────────────────────────────────────────────────┘ │
│                                                         │
│  [Export PDF]  [Close]                                │
└────────────────────────────────────────────────────────┘
```

## Next Steps

Would you like me to:

1. **Implement the full Employee Directory (Option 1)**
   - Complete backend API
   - Employee list page
   - User profile modal
   - Search and filtering

2. **Quick Solution (Option 2)**
   - Add user viewing to import results page
   - Faster to implement
   - Less comprehensive

3. **Custom Approach**
   - Mix and match features from different options
   - Tell me your specific requirements

## Estimated Time

- **Option 1 (Full Directory)**: 4-6 hours
- **Option 2 (Import Enhancement)**: 1-2 hours
- **Option 1 + 4 (Recommended)**: 5-7 hours

What would you prefer? I can start implementing right away!
