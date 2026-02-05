# Progress Tracker Guide

The Progress Tracker feature allows you to monitor and update your career development progress in real-time.

## Features

### 1. View All Development Plans
- See all your development plans at a glance
- Each plan shows:
  - Current and target career levels
  - Completion percentage
  - Number of completed/total objectives
  - Plan status (Active, Completed, Cancelled)
  - Created and target dates
  - Visual progress bar

### 2. Track Learning Objectives
- View all learning objectives for each plan
- See current status: Not Started, In Progress, Completed
- View priority levels: High, Medium, Low
- Track statistics:
  - Total objectives
  - Completed count
  - In progress count
  - Not started count

### 3. Update Progress
- **Change Objective Status**: Click status buttons to mark objectives as:
  - Not Started (grey)
  - In Progress (yellow)
  - Completed (green)
- **Change Plan Status**: Use dropdown to mark plan as:
  - Active (blue)
  - Completed (green)
  - Cancelled (red)

## How to Use

### Access the Tracker
1. Navigate to `http://localhost:3001/progress`
2. Or click "Progress Tracker" in the navigation menu

### View Your Plans
- All plans are displayed as cards
- Click on a plan card to view its details
- The selected plan is highlighted with blue border

### Update Objective Status
1. Find the objective you want to update
2. Click one of the three status buttons:
   - "Not Started" - Haven't begun working on it yet
   - "In Progress" - Currently working on it
   - "Completed" - Finished this objective
3. Progress updates automatically across the interface

### Change Plan Status
1. Select a plan by clicking its card
2. Use the dropdown in the top-right to change status
3. Choose from Active, Completed, or Cancelled

## API Endpoints

### Get User Plans
```bash
GET /api/career/user-plans/{user_id}
```
Returns all plans with progress statistics.

### Get Plan Details
```bash
GET /api/career/development-plan/{plan_id}
```
Returns detailed plan information with all objectives.

### Update Objective Status
```bash
PUT /api/career/objective/{objective_id}?status={status}
```
Updates objective status (not_started, in_progress, completed).

### Update Plan Status
```bash
PUT /api/career/plan/{plan_id}/status?status={status}
```
Updates plan status (active, completed, cancelled).

## Example Workflow

1. **Create a Plan**: Go to Gap Analysis → Generate Development Plan
2. **Track Progress**: Navigate to Progress Tracker
3. **Start Working**: Mark first objective as "In Progress"
4. **Complete Objective**: When done, mark as "Completed"
5. **Monitor Progress**: Watch completion percentage increase
6. **Complete Plan**: When all objectives done, mark plan as "Completed"

## Visual Indicators

- **Progress Bar**: Shows completion percentage (green = 100%)
- **Status Colors**:
  - Grey: Not Started
  - Yellow: In Progress
  - Green: Completed
  - Blue: Active Plan
  - Red: Cancelled Plan

## Testing the Feature

You can test with API calls:

```bash
# View user plans
curl http://localhost:8000/api/career/user-plans/1 | jq

# Mark objective as in progress
curl -X PUT "http://localhost:8000/api/career/objective/1?status=in_progress"

# Mark objective as completed
curl -X PUT "http://localhost:8000/api/career/objective/2?status=completed"

# Mark plan as completed
curl -X PUT "http://localhost:8000/api/career/plan/1/status?status=completed"
```

## Demo Data

The system currently has 12 development plans for user ID 1:
- 7 plans: PC07 → PC08 (8 objectives each)
- 5 plans: PC09 → PC10 (15 objectives each)

All objectives start as "Not Started" and can be updated as you make progress.
