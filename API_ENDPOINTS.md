# API Endpoints Documentation

## Base URL
```
http://localhost:8000/api/v1/
```

---

## 1. Accounts API

### Get All Users
```
GET /api/v1/accounts/users/
```

---

## 2. Academics API

### Get All Sessions
```
GET /api/v1/academics/sessions/
```

### Get All Classes
```
GET /api/v1/academics/classes/
```

### Get All Subjects
```
GET /api/v1/academics/subjects/
```

**Query Parameters:**
- `group` - Filter by group (science, business_studies, humanities)
- `category` - Filter by category (compulsory, group, optional)

### Bulk Import Subjects
```
POST /api/v1/academics/subjects/bulk-import/
```

**Body Format:**
```json
{
  "subjects": [
    {
      "name": "Bangla 1st Paper",
      "code": "101",
      "group": "science",
      "category": "compulsory"
    }
  ]
}
```

---

## 3. Students API

### Get All Students (List View)
```
GET /api/v1/students/list/
```

**Response includes:**
- Student ID, Name, Roll Number
- Class Name, Session, Group
- Email, Subjects Display
- Subject Count

### Get Student Details
```
GET /api/v1/students/<student_id>/
```

**Response includes:**
- All list fields plus:
- Address, Date of Birth
- Detailed subject information
- Creation timestamps

### Get Students Report
```
GET /api/v1/students/report/
```

**Response includes:**
- List of all students with:
- Subjects display with `||` separator
- Attendance information
- Group-wise breakdown

---

## 4. Teachers API

### Get All Teachers
```
GET /api/v1/teachers/list/
```

---

## 5. Exams API

### Get All Exams (Legacy)
```
GET /api/v1/exams/list/
```

### Get All Marks (Legacy)
```
GET /api/v1/exams/marks-legacy/
```

### ExamMark Endpoints (New)

#### Get All Exam Marks
```
GET /api/v1/exams/marks/
```

**Query Parameters:**
- `exam_name` - Filter by exam type (ct_exam, midterm, half_yearly, test, pretest, year_final)
- `subject` - Filter by subject ID
- `session` - Filter by session ID
- `group` - Filter by student group (science, business_studies, humanities)
- `student` - Filter by student ID

#### Create New Exam Mark
```
POST /api/v1/exams/marks/
```

**Body:**
```json
{
  "exam_name": "ct_exam",
  "student": 1,
  "subject": 1,
  "session": 1,
  "cq_marks": "8.00",
  "mct_marks": "7.00",
  "lab_marks": "9.00",
  "total_class": 10,
  "present": 8,
  "absent": 2
}
```

#### Get Single Exam Mark
```
GET /api/v1/exams/marks/<mark_id>/
```

#### Update Exam Mark
```
PUT /api/v1/exams/marks/<mark_id>/
```

```
PATCH /api/v1/exams/marks/<mark_id>/
```

#### Delete Exam Mark
```
DELETE /api/v1/exams/marks/<mark_id>/
```

#### Get Exam Marks by Exam Type
```
GET /api/v1/exams/marks/by_exam/?exam_name=ct_exam
```

**Response includes:**
- Exam name and count
- All marks for that exam type

#### Get Available Exam Names
```
GET /api/v1/exams/marks/exam_names/
```

**Response:**
```json
[
  {
    "value": "ct_exam",
    "label": "CT-Exam"
  },
  ...
]
```

#### Bulk Update Exam Marks
```
POST /api/v1/exams/marks/bulk_update/
```

**Body:**
```json
{
  "marks": [
    {
      "id": 1,
      "cq_marks": "8",
      "mct_marks": "7",
      "lab_marks": "9",
      "present": 8,
      "absent": 2
    },
    {
      "id": 2,
      "cq_marks": "9",
      "mct_marks": "8",
      "lab_marks": "8"
    }
  ]
}
```

#### Get Exam Marks Report
```
GET /api/v1/exams/marks/report/
```

**Query Parameters:**
- `exam_name` - Filter by exam type
- `subject` - Filter by subject ID
- `session` - Filter by session ID

**Response includes:**
- Filters applied
- Statistics (total records, average marks, average attendance)
- Detailed marks data

---

## 6. Dashboard API

### Get Dashboard Analytics
```
GET /api/v1/dashboard/
```

---

## Authentication

Currently, the API supports:
- **Anonymous access** for most endpoints
- **Optional authentication** for ExamMark endpoints

To authenticate, add the following header:
```
Authorization: Token <your-token>
```

---

## Common Response Formats

### Success Response (200 OK)
```json
{
  "id": 1,
  "name": "Example",
  "status": "success",
  ...
}
```

### Error Response (4xx, 5xx)
```json
{
  "error": "Error message",
  "details": "Additional details"
}
```

### Validation Error (400 Bad Request)
```json
{
  "field_name": [
    "Error message for this field"
  ]
}
```

---

## Pagination

Some endpoints support pagination using query parameters:
- `page` - Page number (default: 1)
- `page_size` - Number of items per page (default: 20)

Example:
```
GET /api/v1/students/list/?page=2&page_size=10
```

---

## Filtering Examples

### Get Science Students
```
GET /api/v1/students/list/?group=science
```

### Get CT-Exam Marks for Physics Subject
```
GET /api/v1/exams/marks/?exam_name=ct_exam&subject=1
```

### Get Compulsory Subjects
```
GET /api/v1/academics/subjects/?category=compulsory
```

### Get Business Studies Students in 2025-2026 Session
```
GET /api/v1/students/list/?group=business_studies&session=1
```

---

## Status Codes

| Code | Meaning |
|------|---------|
| 200  | OK - Request successful |
| 201  | Created - Resource created successfully |
| 204  | No Content - Successful deletion |
| 400  | Bad Request - Invalid parameters |
| 404  | Not Found - Resource not found |
| 500  | Server Error |

---

## Notes

1. **Subject Display Format**: Subjects are displayed with ` || ` separator (space-pipe-pipe-space)
   - Example: `Bangla 1st Paper || English 1st Paper || Chemistry`

2. **Exam Marks Calculation**: Total marks are auto-calculated as sum of CQ, MCT, and LAB marks

3. **Attendance**: Tracked with present, absent, and total_class fields. Percentage calculated as (present/total_class)*100

4. **Active Exam Types**: Only active exam types appear in dropdowns. Manage them in admin: `/admin/exams/examtype/`

5. **Unique Constraints**:
   - Students: `roll_number` is unique
   - Subjects: `code` is unique
   - ExamMarks: `(exam_name, student, subject, session)` must be unique

---

## Example Usage with cURL

### Get All Students
```bash
curl -X GET http://localhost:8000/api/v1/students/list/
```

### Create Exam Mark
```bash
curl -X POST http://localhost:8000/api/v1/exams/marks/ \
  -H "Content-Type: application/json" \
  -d '{
    "exam_name": "ct_exam",
    "student": 1,
    "subject": 1,
    "session": 1,
    "cq_marks": "8",
    "mct_marks": "7",
    "lab_marks": "9",
    "total_class": 10,
    "present": 8,
    "absent": 2
  }'
```

### Get CT-Exam Marks
```bash
curl -X GET "http://localhost:8000/api/v1/exams/marks/by_exam/?exam_name=ct_exam"
```

### Bulk Update Marks
```bash
curl -X POST http://localhost:8000/api/v1/exams/marks/bulk_update/ \
  -H "Content-Type: application/json" \
  -d '{
    "marks": [
      {"id": 1, "cq_marks": "8", "mct_marks": "7", "lab_marks": "9"},
      {"id": 2, "cq_marks": "9", "mct_marks": "8", "lab_marks": "8"}
    ]
  }'
```

---

## Contact & Support

For API issues or questions, refer to the project documentation or contact the development team.
