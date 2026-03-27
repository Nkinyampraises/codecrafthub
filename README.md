# CodeCraftHub

CodeCraftHub is a beginner-friendly REST API built with Flask.  
It helps developers track learning courses with a simple JSON file instead of a database.

## 1. Project Overview

CodeCraftHub lets you create and manage personalized learning plans.  
Each course contains:

- `id` (auto-generated integer)
- `name`
- `description`
- `target_date` (format: `YYYY-MM-DD`)
- `status` (`Not Started`, `In Progress`, `Completed`)
- `created_at` (auto-generated timestamp)

This project is ideal if you are learning:

- Flask basics
- REST API fundamentals
- CRUD operations (`Create`, `Read`, `Update`, `Delete`)
- JSON file-based data storage

## 2. Features

- Create a new course
- Get all courses
- Get one course by ID
- Update a course by ID
- Delete a course by ID
- Automatic `courses.json` creation if missing
- Basic request validation
- Date format validation (`YYYY-MM-DD`)
- Status validation with allowed values
- CORS enabled for frontend integration

## 3. Installation Instructions (Step-by-Step)

### Prerequisites

- Python 3.9 or newer
- `pip` package manager
- A terminal (`PowerShell`, `Command Prompt`, or Bash)

### Steps

1. Open terminal and go to the project folder:

```powershell
cd "C:\Users\MATRIX TECHNOLOGY\Documents\ai gens"
```

2. (Optional but recommended) Create a virtual environment:

```powershell
python -m venv .venv
```

3. Activate the virtual environment:

```powershell
.\.venv\Scripts\Activate.ps1
```

4. Install dependencies:

```powershell
pip install flask flask-cors
```

5. Confirm the main file exists:

```powershell
dir app.py
```

## 4. How to Run the Application

Run:

```powershell
python app.py
```

Expected startup output:

```text
CodeCraftHub API is starting...
Data file path: C:\...\courses.json
API will be available at: http://localhost:5000
```

API base URL:

```text
http://localhost:5000
```

Stop the server with `Ctrl + C`.

## 5. API Endpoints Documentation (with Examples)

Base route for courses:

```text
/api/courses
```

### Endpoint Summary

| Method | Endpoint | Description |
|---|---|---|
| POST | `/api/courses` | Create a new course |
| GET | `/api/courses` | Get all courses |
| GET | `/api/courses/<id>` | Get one course by ID |
| PUT | `/api/courses/<id>` | Update a course by ID |
| DELETE | `/api/courses/<id>` | Delete a course by ID |

### A. Create Course

**Request**

```http
POST /api/courses
Content-Type: application/json
```

```json
{
  "name": "Python Basics",
  "description": "Learn Python fundamentals",
  "target_date": "2026-12-31",
  "status": "Not Started"
}
```

**PowerShell example**

```powershell
$body = @{
  name = "Python Basics"
  description = "Learn Python fundamentals"
  target_date = "2026-12-31"
  status = "Not Started"
} | ConvertTo-Json

Invoke-RestMethod -Uri "http://127.0.0.1:5000/api/courses" -Method Post -ContentType "application/json" -Body $body
```

**Success response (`201`)**

```json
{
  "message": "Course created successfully",
  "course": {
    "id": 1,
    "name": "Python Basics",
    "description": "Learn Python fundamentals",
    "target_date": "2026-12-31",
    "status": "Not Started",
    "created_at": "2026-03-27 04:10:00"
  }
}
```

### B. Get All Courses

**Request**

```http
GET /api/courses
```

**PowerShell example**

```powershell
Invoke-RestMethod -Uri "http://127.0.0.1:5000/api/courses" -Method Get
```

**Success response (`200`)**

```json
{
  "message": "Courses retrieved successfully",
  "count": 1,
  "courses": [
    {
      "id": 1,
      "name": "Python Basics",
      "description": "Learn Python fundamentals",
      "target_date": "2026-12-31",
      "status": "Not Started",
      "created_at": "2026-03-27 04:10:00"
    }
  ]
}
```

### C. Get One Course by ID

**Request**

```http
GET /api/courses/1
```

**PowerShell example**

```powershell
Invoke-RestMethod -Uri "http://127.0.0.1:5000/api/courses/1" -Method Get
```

**Success response (`200`)**

```json
{
  "message": "Course retrieved successfully",
  "course": {
    "id": 1,
    "name": "Python Basics",
    "description": "Learn Python fundamentals",
    "target_date": "2026-12-31",
    "status": "Not Started",
    "created_at": "2026-03-27 04:10:00"
  }
}
```

**Not found response (`404`)**

```json
{
  "error": "Course with ID 999 not found"
}
```

### D. Update Course by ID

**Request**

```http
PUT /api/courses/1
Content-Type: application/json
```

```json
{
  "status": "In Progress",
  "description": "Learn Python fundamentals with daily practice"
}
```

**PowerShell example**

```powershell
$body = @{
  status = "In Progress"
  description = "Learn Python fundamentals with daily practice"
} | ConvertTo-Json

Invoke-RestMethod -Uri "http://127.0.0.1:5000/api/courses/1" -Method Put -ContentType "application/json" -Body $body
```

**Success response (`200`)**

```json
{
  "message": "Course updated successfully",
  "course": {
    "id": 1,
    "name": "Python Basics",
    "description": "Learn Python fundamentals with daily practice",
    "target_date": "2026-12-31",
    "status": "In Progress",
    "created_at": "2026-03-27 04:10:00"
  }
}
```

### E. Delete Course by ID

**Request**

```http
DELETE /api/courses/1
```

**PowerShell example**

```powershell
Invoke-RestMethod -Uri "http://127.0.0.1:5000/api/courses/1" -Method Delete
```

**Success response (`200`)**

```json
{
  "message": "Course with ID 1 deleted successfully"
}
```

### Validation Rules

- `name`, `description`, `target_date`, `status` are required on `POST`.
- `status` must be one of:
- `Not Started`
- `In Progress`
- `Completed`
- `target_date` must use `YYYY-MM-DD`.

## 6. Testing Instructions

### Manual Testing (Beginner Friendly)

1. Start the server:

```powershell
python app.py
```

2. In another terminal, test each endpoint using the examples above:

- `POST /api/courses`
- `GET /api/courses`
- `GET /api/courses/<id>`
- `PUT /api/courses/<id>`
- `DELETE /api/courses/<id>`

3. Confirm `courses.json` updates after create, update, and delete requests.

### Quick Error Testing

- Send invalid `status` such as `"Started"` and expect `400`.
- Send invalid `target_date` such as `"12-31-2026"` and expect `400`.
- Request missing ID like `/api/courses/999` and expect `404`.

## 7. Troubleshooting Common Issues

### Issue: `Cannot POST /api/courses`

Possible causes:

- Flask server is not running.
- Wrong URL/port.
- Another app is using port `5000`.
- Command was entered incorrectly in PowerShell.

Fix:

1. Make sure `python app.py` is still running.
2. Use `http://127.0.0.1:5000/api/courses`.
3. Check port usage:

```powershell
netstat -ano | findstr :5000
```

4. If needed, stop conflicting process:

```powershell
Stop-Process -Id <PID> -Force
```

### Issue: `ModuleNotFoundError: No module named 'flask'`

Fix:

```powershell
pip install flask flask-cors
```

### Issue: PowerShell shows `>>` prompt

Cause: Command was not completed correctly (often quote or brace mismatch).

Fix:

- Press `Ctrl + C` to cancel.
- Re-type command carefully.
- Prefer hash table + `ConvertTo-Json` examples shown above.

### Issue: Data not saving in `courses.json`

Possible causes:

- File permission problems.
- Invalid/corrupted JSON file content.

Fix:

1. Ensure the app folder is writable.
2. Open `courses.json` and confirm it is valid JSON.
3. If needed, replace contents with:

```json
[]
```

## 8. Project Structure Explanation

Current project layout:

```text
ai gens/
├── app.py
├── courses.json      # auto-created after first run or first write
└── README.md
```

- `app.py`: Main Flask API file with routes, validation, and JSON file helpers.
- `courses.json`: Local data storage file for courses.
- `README.md`: Documentation and learning guide.

## Notes for Beginners

- This app uses a JSON file instead of a database to keep learning simple.
- For real production systems, use a production server (`gunicorn`, `uwsgi`, or similar) and a real database (`PostgreSQL`, `MySQL`, etc.).
- Start small, test each endpoint one at a time, and inspect the JSON responses.
