# Excel Import Feature - Complete Guide

The GrowthPath application now includes a complete web-based import system for Planisware employee tagging data.

## What Was Added

### Backend Components

1. **API Endpoint** (`backend/app/api/import_data.py`)
   - `POST /import/planisware` - Upload and import Excel files
   - `GET /import/status` - Get current database statistics
   - Full error handling and validation
   - Progress tracking and detailed statistics

2. **Updated Files**
   - `backend/app/main.py` - Added import router
   - `backend/requirements.txt` - Added pandas, openpyxl, werkzeug

### Frontend Components

1. **Import Page** (`frontend/src/pages/DataImport.jsx`)
   - Drag-and-drop file upload
   - File validation
   - Real-time statistics display
   - Detailed import results
   - Instructions and help text

2. **Styling** (`frontend/src/styles/DataImport.css`)
   - Modern card-based layout
   - Purple gradient theme matching app design
   - Responsive design for mobile
   - Animated upload zone

3. **Navigation**
   - Added "Import Data" link to main navigation
   - New route: `/import`

## How to Use

### Setup

1. **Install Backend Dependencies**
   ```bash
   cd backend
   pip install -r requirements.txt
   ```

2. **Start the Backend Server**
   ```bash
   cd backend
   python3 run.py
   ```
   Server will run on http://localhost:8000

3. **Start the Frontend**
   ```bash
   cd frontend
   npm install
   npm run dev
   ```
   Frontend will run on http://localhost:5173

### Using the Import Feature

1. **Navigate to Import Page**
   - Click "Import Data" in the navigation menu
   - Or go directly to http://localhost:5173/import

2. **View Current Statistics**
   - See current number of users, competencies, and assessments
   - Stats update automatically after each import

3. **Upload Excel File**
   - **Drag and drop** your Excel file into the upload zone, OR
   - Click "Browse Files" to select a file
   - Supported formats: `.xlsx`, `.xls`

4. **Import Data**
   - Click "Upload & Import" button
   - Wait for processing (shows "Uploading..." during import)
   - View detailed results

5. **Review Results**
   - Success message with breakdown:
     - Users created/existing
     - Competencies created/existing
     - Assessments created/existing
     - Rows processed/skipped
   - Any errors will be displayed

## Excel File Format

### Required Columns

| Column Name | Description | Example |
|------------|-------------|---------|
| Name | Employee full name | "Ana Smith" |
| Skillset | Skill/competency name | "Backend" |
| Skillset Level | 1st, 2nd, 3rd, or 4th | "2nd" |

### Optional Columns

| Column Name | Description |
|------------|-------------|
| Skillsets.Description | Detailed skill description |
| Skillsets.Category | Standard, Advanced, Niche, Leadership |
| Skillsets.Role | Role associated with skill |
| Resource Location | Employee location |
| Resource Country | Employee country |
| Resource Region | Employee region |

### Example Excel Data

```
Name        | Skillset Level | Skillset              | Skillsets.Category | Skillsets.Description
------------|----------------|-----------------------|--------------------|-----------------------
Ana Smith   | 1st            | Backend               | Standard           | SAP BW Modeling
John Dow    | 2nd            | ML Engineering (Data) | Advanced           | ML model training
Bobi Jay    | 3rd            | Deep Learning (Data)  | Advanced           | Neural Networks
```

## Data Processing Rules

### Email Generation
- Automatically generated as `firstname.lastname@bosch.com`
- Example: "Ana Smith" → `ana.smith@bosch.com`

### Proficiency Level Mapping
- **1st** → Beginner
- **2nd** → Intermediate
- **3rd** → Advanced
- **4th** → Expert

### Category Mapping
- **Standard/Advanced** → Technical
- **Leadership** → Leadership
- **Niche/Domain** → Domain Knowledge
- **Other/Null** → Technical (default)

### Duplicate Handling
- **Users**: Matched by email - reuses existing users
- **Competencies**: Matched by name - reuses existing competencies
- **Assessments**: Creates only if (user + competency + level) combination doesn't exist

### Default Values
- New users get default password: `password123`
- New users assigned role: `EMPLOYEE`
- Missing categories default to: `TECHNICAL`

## API Endpoints

### Import Planisware Data
```http
POST http://localhost:8000/import/planisware
Content-Type: multipart/form-data

file: [Excel file]
```

**Response:**
```json
{
  "success": true,
  "message": "Import completed successfully",
  "statistics": {
    "users_created": 3,
    "users_existing": 0,
    "competencies_created": 7,
    "competencies_existing": 0,
    "assessments_created": 9,
    "assessments_existing": 0,
    "rows_processed": 9,
    "rows_skipped": 0,
    "errors": []
  }
}
```

### Get Database Statistics
```http
GET http://localhost:8000/import/status
```

**Response:**
```json
{
  "users": 3,
  "competencies": 7,
  "assessments": 25
}
```

## Testing

### Test with Sample File

A test file is included: `plw_employee_taging-test.xlsx`

1. Navigate to http://localhost:5173/import
2. Upload `plw_employee_taging-test.xlsx`
3. Click "Upload & Import"
4. Should create 3 users, 7 competencies, and 9 assessments

### Test API Directly

Using curl:
```bash
curl -X POST http://localhost:8000/import/planisware \
  -F "file=@plw_employee_taging-test.xlsx"
```

Using the backend server's API docs:
1. Go to http://localhost:8000/docs
2. Find `POST /import/planisware`
3. Try it out with your Excel file

## Troubleshooting

### Backend Issues

**Error: Module not found (pandas, openpyxl)**
```bash
cd backend
pip install -r requirements.txt
```

**Error: Database connection**
- Check database configuration in `backend/app/core/database.py`
- Ensure database is running

**Error: Port already in use**
```bash
# Kill process on port 8000
lsof -ti:8000 | xargs kill -9
```

### Frontend Issues

**Error: Cannot connect to backend**
- Ensure backend is running on port 8000
- Check CORS settings in `backend/app/main.py`

**Error: Build failed**
```bash
cd frontend
rm -rf node_modules
npm install
```

### Import Issues

**File rejected**
- Ensure file is `.xlsx` or `.xls` format
- Check that required columns exist

**No data imported**
- Check that rows have required fields (Name, Skillset, Skillset Level)
- Review error messages in import results

**Duplicate assessments**
- System prevents exact duplicates (same user + competency + level)
- If you see duplicates, they have different proficiency levels

## Features

- ✅ Drag-and-drop file upload
- ✅ File validation (format, size, columns)
- ✅ Real-time database statistics
- ✅ Detailed import results
- ✅ Error handling and reporting
- ✅ Duplicate prevention
- ✅ Responsive design
- ✅ Progress indicators
- ✅ Help documentation built-in

## Files Modified/Created

### Backend
- ✅ Created: `backend/app/api/import_data.py`
- ✅ Modified: `backend/app/main.py`
- ✅ Modified: `backend/requirements.txt`

### Frontend
- ✅ Created: `frontend/src/pages/DataImport.jsx`
- ✅ Created: `frontend/src/styles/DataImport.css`
- ✅ Modified: `frontend/src/App.jsx`

### Documentation
- ✅ Created: `IMPORT_FEATURE.md` (this file)
- ✅ Existing: `IMPORT_GUIDE.md` (CLI import guide)

## Notes

- The web import uses the same logic as the CLI import script
- All imports are transactional - failures rollback completely
- Password for all imported users is `password123` (should be changed on first login)
- Import preserves existing data - only adds new records
- Statistics refresh automatically after successful import
