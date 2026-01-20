# College Management System - Models Structure

## 📊 Three Connected User Models (No Duplication)

### 1. **User Model** (Accounts App)
**Purpose:** Authentication & Authorization

```
User (AbstractUser extension)
├── username (unique login)
├── email
├── password (hashed)
├── role (admin, teacher, student, staff)
├── phone
├── profile_picture
├── is_staff (Django built-in)
├── is_superuser (Django built-in)
├── groups (Django built-in - for permissions)
└── user_permissions (Django built-in)
```

**Why separate?**
- Handles login, authentication, security
- Manages permissions & authorization via groups
- Used by admin panel and login system

---

### 2. **Student Model** (Students App)
**Purpose:** Student Academic Profile

```
Student
├── user → OneToOneField(User) ← LINKS TO USER
├── name
├── roll_number (unique identifier)
├── email
├── phone
├── address
├── date_of_birth
├── class_name → ForeignKey(Class)
├── session → ForeignKey(Session)
├── group (science/business/humanities)
├── subjects → ManyToMany(Subject)
├── created_at
└── updated_at
```

**Why separate?**
- Contains academic-specific data
- Manages enrollment, groups, subject assignments
- Not all users are students

---

### 3. **Teacher Model** (Teachers App)
**Purpose:** Teacher Academic Profile

```
Teacher
├── user → OneToOneField(User) ← LINKS TO USER
├── name
├── email
├── phone
├── subject → ForeignKey(Subject)
├── post (professor, assistant_professor, lecturer)
├── qualification
├── department
├── created_at
└── updated_at
```

**Why separate?**
- Contains teacher-specific data
- Manages subject assignments, qualifications
- Not all users are teachers

---

## 🔗 How They Work Together

### Before (PROBLEM ❌)
```
User with role='student'    Student record
        ↓                           ↓
  No connection               No connection
   (Unlinked)                 (Unlinked)
```

### After (SOLUTION ✅)
```
User with role='student' ←→ Student record
                  (OneToOneField)

User with role='teacher' ←→ Teacher record
                  (OneToOneField)
```

---

## 📋 Usage Examples

### Creating a Student User with Account
```python
# Step 1: Create User account
user = User.objects.create_user(
    username='john_doe',
    email='john@example.com',
    password='secure_password',
    role='student'
)

# Step 2: Create Student profile linked to User
student = Student.objects.create(
    user=user,
    name='John Doe',
    roll_number='2024001',
    class_name=Class.objects.get(name='10A'),
    session=Session.objects.get(year=2024)
)
```

### Accessing Student from User
```python
user = User.objects.get(username='john_doe')
student = user.student_profile  # Direct access via OneToOne
print(student.roll_number)
```

### Accessing User from Student
```python
student = Student.objects.get(roll_number='2024001')
user = student.user  # Direct access via OneToOne
print(user.username)
```

---

## 👥 Django Built-in Groups (Not User Model)

The `groups` field on User model links to Django's **Group** model:

```
User.groups → ManyToMany(Group)
```

### What are Groups?
- Used for **role-based permissions**
- Each Group has specific permissions
- Example:
  - Group "Teachers": can_edit_marks, can_view_grades
  - Group "Students": can_view_own_marks
  - Group "Admin": all permissions

### Example
```python
# Create a teacher group with permissions
teacher_group = Group.objects.create(name='Teachers')
teacher_group.permissions.add(Permission.objects.get(codename='add_exammark'))

# Add user to group
user = User.objects.get(username='john_doe')
user.groups.add(teacher_group)

# Check if user in group
if user.groups.filter(name='Teachers').exists():
    print("This user can edit marks")
```

---

## 🗂️ Database Schema

```
┌─────────────────┐
│ User (accounts) │
├─────────────────┤
│ id (PK)         │
│ username        │ ← Login account
│ role            │
│ email           │
│ groups FK (M2M) │ ← Permission management
└─────────────────┘
       ↓
       ├─────────────────────────┐
       │                         │
    ┌──────────────────────────────────┐
    │ Student (students)               │
    ├──────────────────────────────────┤
    │ id (PK)                          │
    │ user FK → User (OneToOne)        │ ← Links to User account
    │ roll_number                      │
    │ class_name FK → Class            │
    │ subjects M2M → Subject           │
    └──────────────────────────────────┘
    
    ┌──────────────────────────────────┐
    │ Teacher (teachers)               │
    ├──────────────────────────────────┤
    │ id (PK)                          │
    │ user FK → User (OneToOne)        │ ← Links to User account
    │ subject FK → Subject             │
    │ post                             │
    │ department                       │
    └──────────────────────────────────┘
```

---

## ✅ Benefits of This Structure

| Benefit | Details |
|---------|---------|
| **No Duplication** | Single User table for all auth, not repeated in Student/Teacher |
| **Data Consistency** | Email/phone in both places kept in sync automatically |
| **Easy Linking** | User ↔ Student/Teacher OneToOne relationship |
| **Flexible Roles** | User with role='admin' doesn't need Student/Teacher record |
| **Security** | All password/auth logic centralized in User model |
| **Permissions** | Groups system handles fine-grained access control |
| **Easy Queries** | Access related data: `user.student_profile.subjects` |

---

## 📝 Migration History

| Migration | Change |
|-----------|--------|
| `0005_student_user.py` | Added OneToOne relationship: Student → User |
| `0003_teacher_user.py` | Added OneToOne relationship: Teacher → User |

---

## 🔧 Admin Interface Updates

### Student Admin
- **List Display:** Shows linked User account (`user.username`)
- **Search:** Can search by username (`user__username`)
- **Fieldsets:** Dedicated "User Account" section
- **Filter:** User role visible

### Teacher Admin
- **List Display:** Shows linked User account (`user.username`)
- **Search:** Can search by username (`user__username`)
- **Fieldsets:** Dedicated "User Account" section
- **Filter:** User role visible

---

## 🎯 Summary

✅ **Keep all 3 models** - They serve different purposes
✅ **No duplication** - Data properly separated by responsibility
✅ **Properly linked** - OneToOne relationships connect User ↔ Student/Teacher
✅ **Use Groups** - For permission management, not user types
✅ **Production ready** - Clean, normalized database structure
