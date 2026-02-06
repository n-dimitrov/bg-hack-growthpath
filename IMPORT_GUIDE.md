# Planisware Employee Data Import Guide

This guide explains how to import employee skillset data from Planisware Excel files into the GrowthPath application database.

## Overview

The import script (`backend/import_plw_data.py`) reads employee tagging data from an Excel file and imports it into the database, creating:
- **Users**: Employee records with auto-generated emails
- **Competencies**: Skills/skillsets from the Planisware data
- **Assessments**: Links between users and competencies with proficiency levels

## Excel File Format

The Excel file should contain the following columns:

| Column Name | Description | Required |
|------------|-------------|----------|
| Name | Employee full name | Yes |
| Skillset | Name of the skill/competency | Yes |
| Skillset Level | Proficiency level (1st, 2nd, 3rd, 4th) | Yes |
| Skillsets.Description | Detailed description of the skillset | No |
| Skillsets.Category | Category (Standard, Advanced, Niche, etc.) | No |
| Skillsets.Role | Role associated with the skillset | No |
| Resource Location | Employee location | No |
| Resource Country | Employee country | No |
| Resource Region | Employee region | No |

### Example Data

```
Name        | Skillset Level | Skillset                   | Skillsets.Category | Skillsets.Role
------------|----------------|----------------------------|-------------------|----------------
Ana Smith   | 1st            | Backend                    | Standard          | Data Engineer
John Dow    | 2nd            | ML Engineering (Data)      | Advanced          | Data Scientist
Bobi Jay    | 3rd            | SAP Datasphere (Data)      | Niche             | Data Engineer
```

## Data Mapping

### Skillset Level → Proficiency Level

| Planisware Level | Database Level |
|-----------------|----------------|
| 1st | BEGINNER |
| 2nd | INTERMEDIATE |
| 3rd | ADVANCED |
| 4th | EXPERT |

### Category Mapping

| Planisware Category | Competency Category |
|--------------------|---------------------|
| Standard/Advanced | TECHNICAL |
| Leadership | LEADERSHIP |
| Niche/Domain | DOMAIN_KNOWLEDGE |
| Other/Null | TECHNICAL (default) |

## Usage

### 1. Import Data from Excel File

```bash
cd backend
python3 import_plw_data.py path/to/excel_file.xlsx
```

Using the test file:
```bash
cd backend
python3 import_plw_data.py ../plw_employee_taging-test.xlsx
```

### 2. Verify Imported Data

After importing, verify the data was imported correctly:

```bash
cd backend
python3 verify_import.py
```

This will display:
- Total counts of users, competencies, and assessments
- Detailed list of all users with their skills
- All competencies grouped by category

### 3. Cleanup Data (Testing Only)

To remove all imported data and start fresh:

```bash
cd backend
python3 import_plw_data.py --cleanup
```

**Warning**: This will delete ALL users, competencies, and assessments from the database!

## Import Behavior

### Duplicate Handling

The script intelligently handles duplicates:

1. **Users**: Identified by email (generated from name as `firstname.lastname@bosch.com`)
   - If a user already exists, it reuses the existing record
   - Default password for new users: `password123`

2. **Competencies**: Identified by exact skillset name
   - If a competency already exists, it reuses the existing record
   - Description is only set for new competencies

3. **Assessments**: Identified by (user, competency, proficiency_level)
   - Only creates new assessments if the exact combination doesn't exist
   - Prevents duplicate skill assignments

### Data Validation

- Skips rows with missing `Name` or `Skillset`
- Handles null/NaN values gracefully in optional fields
- Auto-assigns default values for missing categories

## Output Example

```
============================================================
PLANISWARE EMPLOYEE DATA IMPORT
============================================================

Reading Excel file: ../plw_employee_taging-test.xlsx
Found 9 records in Excel file

Created user: Ana Smith (ana.smith@bosch.com)
Created competency: Backend (technical)
Created assessment: Ana Smith -> Backend (BEGINNER)
Created user: John Dow (john.dow@bosch.com)
Created competency: ML Engineering (Data) (technical)
Created assessment: John Dow -> ML Engineering (Data) (INTERMEDIATE)

============================================================
IMPORT SUMMARY
============================================================
Users created: 3
Users existing: 6
Competencies created: 7
Competencies existing: 2
Assessments created: 6
============================================================

Import completed successfully!
```

## Troubleshooting

### Missing Dependencies

If you get import errors, ensure you have the required packages:

```bash
pip install pandas openpyxl sqlalchemy werkzeug
```

### Database Connection Issues

Make sure the database is properly configured in `backend/app/core/database.py` and the database file/server is accessible.

### Excel File Format Issues

- Ensure the Excel file is in `.xlsx` format (not `.xls`)
- Check that column names match exactly (case-sensitive)
- Verify that the file is not open in Excel when running the import

## Notes

- Email addresses are auto-generated as `firstname.lastname@bosch.com`
- All new users are created with role `EMPLOYEE`
- Default password for all imported users is `password123` (should be changed on first login)
- The script creates database tables automatically if they don't exist
- Import is transactional - if any error occurs, all changes are rolled back
