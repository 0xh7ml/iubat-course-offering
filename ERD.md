# Entity Relationship Diagram (ERD)

```mermaid
erDiagram
    User {
        int id PK
        string username
        string email
        string first_name
        string last_name
        string password
        datetime date_joined
        boolean is_active
    }

    Department {
        int id PK
        string name
        string code UK
        boolean status
        datetime created_at
        datetime updated_at
    }

    Semester {
        int id PK
        string name
        datetime created_at
        datetime updated_at
    }

    Course {
        int id PK
        string course_name
        string course_code UK
        int department_id FK
        int credits
        boolean lab_course
        datetime created_at
        datetime updated_at
    }

    CourseSchedule {
        int id PK
        int course_id FK
        string day
        string time_slot
        string section
        string room_no
        datetime created_at
        datetime updated_at
    }

    Student {
        int id PK
        int user_id FK
        string student_id UK
        string student_name
        string student_email UK
        int department_id FK
        boolean is_verified
        datetime created_at
        datetime updated_at
    }

    Enrollment {
        int id PK
        int student_id FK
        int course_id FK
        int semester_id FK
        int year
        datetime created_at
        datetime updated_at
    }

    %% Relationships
    User ||--|| Student : "has profile"
    Department ||--o{ Course : "offers"
    Department ||--o{ Student : "belongs to"
    Course ||--o{ CourseSchedule : "has schedules"
    Course ||--o{ Enrollment : "enrolled in"
    Student ||--o{ Enrollment : "enrolls"
    Semester ||--o{ Enrollment : "during"
```

## Key Relationships:

1. **User ↔ Student**: One-to-One relationship (Student profile extends Django User)
2. **Department ↔ Course**: One-to-Many (Department offers multiple courses)
3. **Department ↔ Student**: One-to-Many (Students belong to departments)
4. **Course ↔ CourseSchedule**: One-to-Many (Course can have multiple schedules/sections)
5. **Course ↔ Enrollment**: One-to-Many (Course can have multiple enrollments)
6. **Student ↔ Enrollment**: One-to-Many (Student can enroll in multiple courses)
7. **Semester ↔ Enrollment**: One-to-Many (Multiple enrollments per semester)

## Unique Constraints:
- Department: `code`
- Course: `course_code`
- Student: `student_id`, `student_email`
- CourseSchedule: `(course, day, time_slot, section)`
- Enrollment: `(student, course, semester, year)`