# AI Skills Analysis Feature 🤖

## Overview

The Skills Analysis feature uses LLM (Large Language Model) to analyze an employee's skills and provide intelligent insights, gap analysis, and career recommendations.

## What It Does

When you click the **"🤖 Analyze Skills"** button on a user's profile, the system:

1. **Collects** all user's skills and proficiency levels
2. **Sends** to LLM with a structured prompt
3. **Analyzes** the skills using AI
4. **Returns** comprehensive analysis including:
   - Skill gaps identification
   - Missing competencies for their role
   - Top 5 recommended skills to develop
   - Career opportunities and progression paths
   - Strengths and unique skill combinations

## How to Use

### Step 1: View Employee Profile
1. Go to **Employees** page
2. Search for an employee
3. Click **"View Profile"**

### Step 2: Analyze Skills
1. In the profile modal, click **"🤖 Analyze Skills"** button
2. Wait for analysis (usually 5-10 seconds)
3. Results appear below the skills list

### Step 3: Review Analysis
The AI provides:
- **Skill Gaps Analysis** - What's missing?
- **Recommendations** - What to learn next?
- **Career Opportunities** - What roles are possible?
- **Strengths** - What are they good at?

## Example Output

```
🤖 AI Skills Analysis

📊 Analyzed 9 skills | 🤖 Model: claude-sonnet-4-5

Skill Gaps Analysis:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
**Important Skills Missing:**
- Cloud Computing (AWS, Azure, GCP) - Critical for modern data engineering
- Real-time Data Processing (Kafka, Spark Streaming)
- Data Pipeline Orchestration (Airflow, Prefect)

**Categories Needing Strengthening:**
- Leadership Skills: No leadership competencies recorded
- Soft Skills: Communication and collaboration skills not documented

Recommendations:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
**Top 5 Skills to Develop:**

1. **Cloud Data Platforms (High Priority)**
   - Focus: AWS Redshift, Azure Synapse, or GCP BigQuery
   - Impact: Essential for modern data engineering roles
   - Learning Path: AWS Solutions Architect certification

2. **Real-time Processing (High Priority)**
   - Focus: Apache Kafka, Spark Streaming
   - Impact: Opens up streaming data engineer roles
   - Learning Path: Apache Kafka course + hands-on projects

3. **Data Pipeline Orchestration (Medium Priority)**
   - Focus: Apache Airflow
   - Impact: Industry standard for workflow management
   - Learning Path: Airflow fundamentals + DAG development

4. **Python Advanced (Medium Priority)**
   - Current: Beginner → Target: Advanced
   - Impact: Core skill for all data roles
   - Learning Path: Advanced Python, async programming

5. **Leadership Skills (Long-term)**
   - Focus: Team management, mentoring
   - Impact: Required for senior/lead roles
   - Learning Path: Technical leadership courses

Career Opportunities:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
**Possible Roles with Current Skills:**
- Junior Data Engineer (Strong fit)
- SAP BI Developer (Excellent fit - leverages SAP expertise)
- Business Intelligence Analyst (Good fit)

**With Additional Skills:**
- Senior Data Engineer (Add: Cloud platforms, Kafka)
- Data Platform Engineer (Add: Airflow, Kubernetes)
- Lead Data Engineer (Add: Leadership skills + cloud)

**Suggested Progression Path:**
1. Current: Junior Data Engineer
2. Next (6-12 months): Mid-level Data Engineer
   - Requirement: Master cloud platforms + real-time processing
3. Future (2-3 years): Senior Data Engineer
   - Requirement: Leadership skills + architectural design

Strengths:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
**Strongest Areas:**
- SAP Ecosystem: Deep knowledge in SAP BW, HANA, Datasphere
- Backend Development: Good foundation in backend systems
- Data Visualization: Power BI proficiency

**Unique Skill Combination:**
- SAP + Backend + Data = Excellent for SAP modernization projects
- Can bridge traditional SAP with modern data platforms
- Valuable for companies migrating from SAP to cloud
```

## API Endpoint

### POST /users/{user_id}/analyze-skills

**Request:**
```bash
POST http://localhost:8000/users/1/analyze-skills
```

**Response:**
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
  "analysis": "Full LLM analysis text...",
  "model_used": "claude-sonnet-4-5@20250929"
}
```

## LLM Prompt Structure

The system sends a structured prompt to the LLM:

### System Prompt
```
You are an expert career advisor and skills analyst.
Analyze the employee's current skills and provide actionable insights.
Focus on identifying skill gaps, missing competencies, and career development opportunities.
Provide specific, practical recommendations.
```

### User Prompt
```
Analyze the following employee profile:

Employee: [Name]
Role: [Role]
Current Skills (X total):
- [Skill 1] (category): proficiency_level
- [Skill 2] (category): proficiency_level
...

Skills by Category:
- technical: X skills
- domain_knowledge: X skills

Please provide:
1. Skill Gaps Analysis
2. Recommendations (Top 5)
3. Career Opportunities
4. Strengths
```

## Configuration

### Required Environment Variables

In `backend/.env`:
```env
LLM_FARM_BASE_URL=https://your-llm-farm-url
LLM_FARM_API_KEY=your-api-key
LLM_DEFAULT_MODEL=claude-sonnet-4-5@20250929
LLM_DEFAULT_MAX_TOKENS=2000
```

### Check LLM Configuration

```bash
curl http://localhost:8000/api/llm/health
```

Should return:
```json
{
  "status": "configured",
  "has_api_key": true,
  "base_url": "https://...",
  "default_model": "claude-sonnet-4-5@20250929"
}
```

## Features

### Frontend
- ✅ **Analyze Button** - Green gradient button in profile modal
- ✅ **Loading State** - Shows "🔄 Analyzing..." while processing
- ✅ **Results Display** - Formatted with headers, lists, paragraphs
- ✅ **Close Analysis** - X button to hide results
- ✅ **Scrollable** - Max height with scroll for long analyses
- ✅ **Beautiful Design** - Purple/pink gradient background

### Backend
- ✅ **Skills Collection** - Gathers all user skills and levels
- ✅ **Prompt Engineering** - Structured, detailed prompt
- ✅ **LLM Integration** - Uses existing LLM client
- ✅ **Error Handling** - Graceful failures with messages
- ✅ **Response Formatting** - Returns structured data

## Benefits

### For Employees
- 🎯 **Clear Direction** - Know what to learn next
- 📈 **Career Path** - See possible progression
- 💪 **Recognize Strengths** - Understand their value
- 🎓 **Learning Guidance** - Specific recommendations

### For Managers
- 👥 **Team Assessment** - Quick skills overview
- 📊 **Gap Identification** - Find training needs
- 🚀 **Career Planning** - Support employee growth
- 💼 **Role Assignment** - Match skills to projects

### For HR
- 📈 **Workforce Planning** - Identify organizational gaps
- 🎓 **Training Programs** - Data-driven L&D decisions
- 🔄 **Talent Mobility** - Find internal candidates
- 📊 **Skills Inventory** - Track competency distribution

## Error Handling

### LLM Not Configured
```
Error: LLM service not configured. Please set LLM_FARM_API_KEY.
```
**Solution**: Set up environment variables in `.env`

### No Skills to Analyze
```
Error: User has no skills to analyze
```
**Solution**: User needs to have at least one skill/assessment

### API Failure
```
Error: Analysis failed: [error message]
```
**Solution**: Check backend logs, verify LLM service availability

## Customization

### Modify Analysis Focus

Edit the prompt in `backend/app/api/users.py`:

```python
user_prompt = f"""Analyze the following employee profile:
...
Please provide:
1. [Your custom analysis type]
2. [Your custom recommendations]
3. [Your custom insights]
"""
```

### Change LLM Model

In `.env`:
```env
LLM_DEFAULT_MODEL=claude-opus-4-5@20251101  # Use more powerful model
```

### Adjust Response Length

In the API call:
```python
llm_response = await llm_client.chat_completion(
    user_content=user_prompt,
    system_content=system_prompt,
    max_tokens=3000  # Increase for longer analysis
)
```

## UI Mockup

```
┌────────────────────────────────────────────────────────┐
│  Ana Smith's Profile                          [X]      │
│  ana.smith@bosch.com • Employee                        │
├────────────────────────────────────────────────────────┤
│                                                         │
│  📊 Skills Overview                                    │
│  9 Total Skills | 7 Technical | 2 Domain Knowledge    │
│                                                         │
│  🔧 TECHNICAL SKILLS (7)                              │
│  [Skills list with proficiency bars...]               │
│                                                         │
├────────────────────────────────────────────────────────┤
│  🤖 AI Skills Analysis                         [X]     │
│  📊 Analyzed 9 skills | 🤖 Model: claude-sonnet-4-5  │
│  ┌──────────────────────────────────────────────────┐ │
│  │ [Scrollable analysis content]                     │ │
│  │ - Skill gaps                                      │ │
│  │ - Recommendations                                 │ │
│  │ - Career paths                                    │ │
│  │ - Strengths                                       │ │
│  └──────────────────────────────────────────────────┘ │
├────────────────────────────────────────────────────────┤
│  [Close] [🤖 Analyze Skills] [Export PDF]             │
└────────────────────────────────────────────────────────┘
```

## Next Steps

Potential enhancements:
1. **Save Analysis** - Store analysis results in database
2. **Compare Over Time** - Track skill development
3. **Team Analysis** - Analyze entire team's skills
4. **Custom Prompts** - Let users ask specific questions
5. **PDF Export** - Include analysis in PDF export
6. **Email Report** - Send analysis via email
7. **Action Items** - Convert recommendations to tasks
8. **Learning Resources** - Link to courses/materials

## Summary

✅ **New Endpoint**: `POST /users/{user_id}/analyze-skills`
✅ **New Button**: "🤖 Analyze Skills" in UserProfile
✅ **LLM Integration**: Uses Bosch LLM Farm
✅ **Comprehensive Analysis**: Gaps, recommendations, career paths
✅ **Beautiful UI**: Gradient design, scrollable, formatted
✅ **Error Handling**: Graceful failures with messages

The feature is **ready to use** once LLM is configured! 🎉
