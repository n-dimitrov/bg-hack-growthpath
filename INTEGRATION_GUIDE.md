# GrowthPath Career Framework Integration Guide

## Overview
The CareerFramework.json file contains the complete Bosch Software Engineering career progression framework extracted from the official competency document.

## File Structure

### 1. Metadata
```json
{
  "document_title": "Software Engineering Career Framework",
  "source": "1. Software Engineering-v5-20260205_122313.pdf",
  "organization": "Robert Bosch GmbH"
}
```

### 2. Career Tracks

#### Software Engineer Track (5 Levels)
| Level | Title | Pay Class | Impact Scope |
|-------|-------|-----------|--------------|
| 1 | Junior Software Engineer | PC06 | Individual tasks |
| 2 | Software Engineer | PC07 | Component-level |
| 3 | Senior Software Engineer | PC08 | System-level |
| 4 | Lead Software Engineer | PC09 | Team-level |
| 5 | Principal Software Engineer | PC10 | Organization-wide |

#### Software Architect Track (2 Levels)
| Level | Title | Pay Class | Project Category |
|-------|-------|-----------|------------------|
| 1 | Software Architect | PC09 | Category D |
| 2 | Senior Software Architect | PC10 | Category C |

### 3. Competency Areas (10 Total)

Each competency area defines expectations for each pay class (PC06-PC10):

1. **Design, Implementation, Documentation** - Core technical execution
2. **Process Development & Improvement** - Process understanding and optimization
3. **Quality Assurance** - Quality control and testing
4. **Error Analysis & Repair** - Debugging and problem-solving
5. **Technology Adoption** - Learning and applying new technologies
6. **Operations & SRE** - System reliability and operations
7. **Architecture & System Design** - System design (PC08+)
8. **CI/CD Infrastructure** - Build and deployment automation
9. **Knowledge Sharing & Mentorship** - Teaching and developing others
10. **Technical Communication** - Representing technical perspective (PC09+)

### 4. Architect-Specific Competencies (9 Total)

1. **Requirements Engineering**
2. **Conception & Design**
3. **Stakeholder Management**
4. **Project & Product Scope**
5. **Innovation & Technology Trends**
6. **Development Team Support**
7. **Pre-Sales Activities**
8. **Knowledge Exchange**
9. **Architecture Documentation**

---

## Integration with GrowthPath

### Use Case 1: Career Path Visualization

**Example**: Show an employee their progression path

```javascript
// Frontend (React)
import careerFramework from './CareerFramework.json';

// Get career ladder for Software Engineer track
const engineerTrack = careerFramework.career_tracks.software_engineer;

// Display progression
engineerTrack.levels.forEach(level => {
  console.log(`${level.title} (${level.pay_class})`);
  console.log(`  Impact: ${level.impact_scope}`);
});
```

### Use Case 2: Competency Assessment

**Example**: Evaluate employee against competency requirements

```javascript
// Check what's expected at Senior level (PC08)
const seniorExpectations = careerFramework.competency_areas
  .design_implementation_documentation
  .levels['PC08'];

console.log(seniorExpectations.expectations);
// Output: "Independently expand, implement and document..."
```

### Use Case 3: Skills Gap Analysis

**Example**: Identify what an employee needs to learn for next level

```python
# Backend (Python/FastAPI)
import json

with open('CareerFramework.json') as f:
    framework = json.load(f)

current_level = 'PC07'  # Software Engineer
next_level = 'PC08'     # Senior Software Engineer

# Get competency differences
for area_key, area in framework['competency_areas'].items():
    current = area['levels'].get(current_level)
    next_lvl = area['levels'].get(next_level)
    
    if current and next_lvl:
        print(f"\n{area['name']}:")
        print(f"  Current: {current['expectations']}")
        print(f"  Next: {next_lvl['expectations']}")
```

### Use Case 4: Development Plan Generation

**Example**: Auto-generate learning objectives based on level

```javascript
// Get all competencies for target level
function getCompetenciesForLevel(payClass) {
  const competencies = [];
  
  for (const [key, area] of Object.entries(careerFramework.competency_areas)) {
    if (area.levels[payClass]) {
      competencies.push({
        area: area.name,
        expectations: area.levels[payClass].expectations
      });
    }
  }
  
  return competencies;
}

// Generate learning plan for PC09 (Lead Engineer)
const leadCompetencies = getCompetenciesForLevel('PC09');
```

### Use Case 5: Role Mapping

**Example**: Map employee roles from EmployeeData.json to career framework

```javascript
// Map employee role to career level
function mapRoleToCareerLevel(employeeRole) {
  const roleMapping = {
    "BD>IT Specialist>Software Development Engineer": "software_engineer",
    "BD>IT Architect>Data Architect": "software_architect",
    // ... more mappings
  };
  
  return roleMapping[employeeRole] || 'software_engineer';
}

// Get employee's potential career path
const employee = employees.employees[0];
const track = mapRoleToCareerLevel(employee.primary_role);
const careerPath = careerFramework.career_tracks[track];
```

---

## Database Schema Suggestions

### Table: `career_levels`
```sql
CREATE TABLE career_levels (
  id INTEGER PRIMARY KEY,
  track VARCHAR(50),  -- 'software_engineer' or 'software_architect'
  level INTEGER,
  title VARCHAR(100),
  pay_class VARCHAR(10),
  summary TEXT,
  impact_scope TEXT
);
```

### Table: `competency_areas`
```sql
CREATE TABLE competency_areas (
  id INTEGER PRIMARY KEY,
  area_key VARCHAR(100),
  name VARCHAR(200),
  description TEXT
);
```

### Table: `competency_expectations`
```sql
CREATE TABLE competency_expectations (
  id INTEGER PRIMARY KEY,
  competency_area_id INTEGER,
  pay_class VARCHAR(10),
  expectations TEXT,
  FOREIGN KEY (competency_area_id) REFERENCES competency_areas(id)
);
```

### Table: `employee_assessments`
```sql
CREATE TABLE employee_assessments (
  id INTEGER PRIMARY KEY,
  employee_id VARCHAR(100),
  competency_area_id INTEGER,
  current_level VARCHAR(10),
  target_level VARCHAR(10),
  assessment_date DATE,
  notes TEXT,
  FOREIGN KEY (competency_area_id) REFERENCES competency_areas(id)
);
```

---

## API Endpoint Examples

### GET /api/career-paths
**Description**: Get all available career tracks

```json
{
  "tracks": [
    {
      "key": "software_engineer",
      "name": "Software Engineer Track",
      "levels": 5
    },
    {
      "key": "software_architect",
      "name": "Software Architect Track",
      "levels": 2
    }
  ]
}
```

### GET /api/career-paths/:track/:level
**Description**: Get detailed info for specific level

```json
{
  "level": 3,
  "title": "Senior Software Engineer",
  "pay_class": "PC08",
  "summary": "Independent contributor working on clearly defined tasks",
  "competencies": [
    {
      "area": "Design, Implementation, Documentation",
      "expectations": "Independently expand, implement..."
    }
  ]
}
```

### GET /api/employees/:id/career-progression
**Description**: Get employee's current level and next steps

```json
{
  "employee_id": "johndoe",
  "current_level": {
    "title": "Software Engineer",
    "pay_class": "PC07"
  },
  "next_level": {
    "title": "Senior Software Engineer",
    "pay_class": "PC08"
  },
  "skills_gap": [
    {
      "competency": "Design, Implementation, Documentation",
      "current": "Assistance in implementing...",
      "required": "Independently expand, implement...",
      "gap": "Need to work independently without assistance"
    }
  ]
}
```

---

## React Component Examples

### CareerPathVisualization.jsx
```jsx
import React from 'react';
import careerFramework from '../data/CareerFramework.json';

const CareerPathVisualization = ({ track = 'software_engineer' }) => {
  const levels = careerFramework.career_tracks[track].levels;
  
  return (
    <div className="career-path">
      <h2>{careerFramework.career_tracks[track].name}</h2>
      <div className="levels">
        {levels.map(level => (
          <div key={level.level} className="level-card">
            <h3>{level.title}</h3>
            <span className="pay-class">{level.pay_class}</span>
            <p>{level.summary}</p>
            <p className="impact">{level.impact_scope}</p>
          </div>
        ))}
      </div>
    </div>
  );
};
```

### CompetencyMatrix.jsx
```jsx
const CompetencyMatrix = ({ payClass }) => {
  const areas = careerFramework.competency_areas;
  
  return (
    <div className="competency-matrix">
      <h2>Competencies for {payClass}</h2>
      {Object.entries(areas).map(([key, area]) => {
        const levelData = area.levels[payClass];
        if (!levelData) return null;
        
        return (
          <div key={key} className="competency-card">
            <h3>{area.name}</h3>
            <p className="description">{area.description}</p>
            <div className="expectations">
              <strong>Expectations:</strong>
              <p>{levelData.expectations}</p>
            </div>
          </div>
        );
      })}
    </div>
  );
};
```

---

## Matching Employee Data to Career Framework

### Example Analysis

From your **EmployeeData.json** (514 employees):
- Primary roles include "Software Development Engineer", "Data Engineer", "Data Scientist"
- These can be mapped to career levels based on proficiency and experience

**Suggested Mapping Logic**:
```javascript
function estimateCareerLevel(employee, skillAssessments) {
  // Count advanced skills
  const advancedSkills = skillAssessments.filter(
    s => s.employee_id === employee.id && s.proficiency_level === 'advanced'
  ).length;
  
  // Estimate based on skills and role
  if (advancedSkills >= 5 && employee.rate_card >= 3) {
    return 'PC09'; // Lead or Principal
  } else if (advancedSkills >= 2) {
    return 'PC08'; // Senior
  } else if (employee.rate_card >= 2) {
    return 'PC07'; // Mid-level
  } else {
    return 'PC06'; // Junior
  }
}
```

---

## Next Steps

1. **Import into Database**: Load CareerFramework.json into your SQLite/PostgreSQL database
2. **Create Mappings**: Link employee roles to career tracks
3. **Build UI Components**: Create React components to visualize career paths
4. **Assessment Tools**: Build tools for managers to assess employees against competencies
5. **Development Plans**: Auto-generate development plans based on skills gaps

---

## Files Created

1. **CareerFramework.json** - Complete career framework data
2. **EmployeeData.json** - Employee profiles and skills
3. **SkillAssessments.json** - Skill proficiency data
4. **Skillsets.json** - Master skill definitions
5. **TechMasterData.json** - Technology skills taxonomy

All files are ready for integration into your GrowthPath application!
