# College Management System - Student-Subject API Documentation

## Overview
The student-subject system allows you to manage student enrollments and subject assignments through both Django Admin and REST API.

## Features
- Add students with personal and academic information
- Assign multiple subjects to each student
- Track subject groups (science, business, humanities, religion)
- View student details with enrolled subjects
- REST API endpoints for integration

## How to Use

### 1. **Admin Panel - Adding Students with Subjects**

**URL:** `http://localhost:8000/admin/students/student/`

#### Steps:
1. Click "Add Student" button
2. Fill in basic information:
   - Name (e.g., "Ahmed Hassan")
   - Roll Number (e.g., "XI-A-001")
   - Email, Phone (optional)
3. Select academic info:
   - Class (e.g., "XI-A Science")
   - Session (e.g., "2025-2026")
4. **Add Subjects** - In the "Student Subjects" section (below):
   - Click "Add another Student Subject" row
   - Select Subject (e.g., "Bangla 1st Paper")
   - Select Group (science, business, humanities, religion)
   - Can add multiple subjects
5. Click "Save"

### 2. **REST API Endpoints**

#### **A. Student List**
```
GET /api/v1/students/list/
```
Returns all students with subject count.

**Response:**
```json
[
  {
    "id": 1,
    "name": "Ahmed Hassan",
    "roll_number": "XI-A-001",
    "class_name": "XI-A Science",
    "session": "2025-2026",
    "email": "ahmed@example.com",
    "phone": null,
    "subject_count": 5
  }
]
```

#### **B. Student Detail**
```
GET /api/v1/students/{id}/
```
Returns student with all enrolled subjects and details.

**Response:**
```json
{
  "id": 1,
  "name": "Ahmed Hassan",
  "roll_number": "XI-A-001",
  "class_name": "XI-A Science",
  "session": "2025-2026",
  "email": "ahmed@example.com",
  "student_subjects": [
    {
      "id": 1,
      "subject": 1,
      "subject_details": {
        "id": 1,
        "name": "Bangla 1st Paper",
        "code": "101",
        "group": "science",
        "category": "compulsory"
      },
      "group": "science",
      "enrollment_date": "2026-01-19T23:38:59.143476Z"
    }
  ]
}
```

#### **C. All Student-Subject Enrollments**
```
GET /api/v1/students/subjects/
```
Returns all student-subject relationships.

#### **D. Student's Subjects**
```
GET /api/v1/students/{student_id}/subjects/
```
Returns subjects enrolled by a specific student.

**Response:**
```json
{
  "student": {
    "id": 1,
    "name": "Ahmed Hassan",
    "roll_number": "XI-A-001",
    "class_name": "XI-A Science"
  },
  "subjects": [
    {
      "id": 1,
      "subject": 1,
      "subject_details": {
        "name": "Bangla 1st Paper",
        "code": "101"
      },
      "group": "science"
    }
  ],
  "total_subjects": 5
}
```

### 3. **Database Models**

#### **Student Model**
- `name` - Student name
- `roll_number` - Unique student ID
- `class_name` - FK to Class
- `session` - FK to Session
- `email` - Student email
- `phone` - Student phone
- `address` - Address
- `date_of_birth` - DOB
- `subjects` - M2M to Subject (through StudentSubject)

#### **StudentSubject Model**
- `student` - FK to Student
- `subject` - FK to Subject
- `group` - Subject group (science/business/humanities/religion)
- `enrollment_date` - When enrolled
- `unique_together` - (student, subject) - prevents duplicate enrollments

### 4. **Sample Data Script**

Run the sample script to create test data:
```bash
python create_sample_students.py
```

This creates:
- Sample class "XI-A Science"
- Two sample students with 5 subjects each
- Proper subject enrollments

## Admin Features

### Student Admin
- List view showing: Name, Roll Number, Class, Session, Email, Phone
- Inline subject addition
- Search by name, roll number, email
- Filter by class and session

### StudentSubject Admin
- View all student-subject relationships
- List: Student, Subject, Group, Enrollment Date
- Filter by group and enrollment date
- Search by student or subject name

### Subject Admin (Enhanced)
- Shows group and category in list
- Filter by group (science, business, humanities, religion)
- Filter by category (compulsory, group, optional)
- Better organization for curriculum management

## Workflow Example

1. **Create Classes** (if not exists):
   - Go to /admin/academics/class/
   - Create: "XI-A Science", "XI-B Science", etc.

2. **Create Sessions**:
   - Go to /admin/academics/session/
   - Create: "2025-2026", "2026-2027", etc.

3. **Bulk Import Subjects** (already done):
   - POST to /api/v1/academics/subjects/bulk-import/
   - 54 subjects already imported

4. **Add Students**:
   - Go to /admin/students/student/
   - Add New Student
   - Fill basic info, select class and session
   - Add subjects in the inline form
   - Save

5. **View Data**:
   - API: GET /api/v1/students/list/
   - API: GET /api/v1/students/{id}/
   - API: GET /api/v1/students/{id}/subjects/

## Notes
- When adding a student subject, the group field helps track which group (science/business/etc) the student is enrolled in
- Each student can have multiple subjects
- Subject categories (compulsory, group, optional) are defined per subject, not per enrollment
- Enrollment tracking helps with analytics and student progress
