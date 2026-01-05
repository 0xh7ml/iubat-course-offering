# Data Flow Diagram (DFD)

## Level 0: Context Diagram

```mermaid
graph TD
    Student[Student User]
    Admin[Admin User]
    System[IUBAT Course Offering System]
    DB[(Database)]
    
    Student -->|Login, Enroll, View Schedule| System
    System -->|Dashboard, Course Info, Schedule| Student
    
    Admin -->|Manage Data, Create Users| System
    System -->|Reports, Status| Admin
    
    System <-->|Store/Retrieve Data| DB
```

## Level 1: System Overview

```mermaid
graph TD
    subgraph "External Entities"
        Student[Student]
        Admin[Admin]
    end
    
    subgraph "IUBAT Course Offering System"
        Auth[Authentication Process]
        StudentMgmt[Student Management]
        CourseMgmt[Course Management]
        EnrollMgmt[Enrollment Management]
        ScheduleMgmt[Schedule Management]
    end
    
    subgraph "Data Stores"
        UserDB[(User Data)]
        StudentDB[(Student Data)]
        CourseDB[(Course Data)]
        ScheduleDB[(Schedule Data)]
        EnrollDB[(Enrollment Data)]
        DeptDB[(Department Data)]
        SemDB[(Semester Data)]
    end
    
    %% Student flows
    Student -->|Login Credentials| Auth
    Auth -->|Authentication Result| Student
    Auth <-->|Validate User| UserDB
    Auth <-->|Get Student Profile| StudentDB
    
    Student -->|View Dashboard Request| StudentMgmt
    StudentMgmt -->|Dashboard Data| Student
    StudentMgmt <-->|Student Statistics| EnrollDB
    
    Student -->|Enrollment Request| EnrollMgmt
    EnrollMgmt -->|Enrollment Status| Student
    EnrollMgmt <-->|Enrollment Records| EnrollDB
    EnrollMgmt <-->|Course Info| CourseDB
    
    Student -->|Schedule Request| ScheduleMgmt
    ScheduleMgmt -->|Weekly Schedule| Student
    ScheduleMgmt <-->|Schedule Data| ScheduleDB
    ScheduleMgmt <-->|Enrollment Data| EnrollDB
    
    %% Admin flows
    Admin -->|Manage Students| StudentMgmt
    StudentMgmt <-->|Student Records| StudentDB
    StudentMgmt <-->|User Accounts| UserDB
    StudentMgmt <-->|Department Info| DeptDB
    
    Admin -->|Manage Courses| CourseMgmt
    CourseMgmt <-->|Course Records| CourseDB
    CourseMgmt <-->|Department Info| DeptDB
    
    Admin -->|Manage Schedules| ScheduleMgmt
    ScheduleMgmt <-->|Schedule Records| ScheduleDB
    ScheduleMgmt <-->|Course Info| CourseDB
    
    Admin -->|Manage Enrollments| EnrollMgmt
    EnrollMgmt <-->|Student Info| StudentDB
    EnrollMgmt <-->|Semester Info| SemDB
```

## Level 2: Detailed Process Flow

```mermaid
graph TD
    subgraph "Authentication Process"
        A1[Validate Credentials]
        A2[Check Student Profile]
        A3[Verify Account Status]
        A4[Create Session]
    end
    
    subgraph "Student Dashboard Process"
        D1[Get Student Info]
        D2[Calculate Statistics]
        D3[Get Current Enrollments]
        D4[Format Dashboard Data]
    end
    
    subgraph "Course Enrollment Process"
        E1[Get Available Courses]
        E2[Check Current Enrollments]
        E3[Validate Enrollment Request]
        E4[Create/Remove Enrollment]
        E5[Update Enrollment Status]
    end
    
    subgraph "Schedule Management Process"
        S1[Get Student Enrollments]
        S2[Fetch Course Schedules]
        S3[Organize by Day/Time]
        S4[Generate Weekly View]
    end
    
    subgraph "Admin Management Process"
        M1[CRUD Operations]
        M2[Data Validation]
        M3[Auto-create Users]
        M4[Relationship Management]
    end
    
    %% Process flows
    Student -->|Login| A1
    A1 --> A2 --> A3 --> A4
    A4 -->|Success| D1
    
    D1 --> D2 --> D3 --> D4
    D4 -->|Dashboard| Student
    
    Student -->|Enroll/Unenroll| E1
    E1 --> E2 --> E3 --> E4 --> E5
    E5 -->|Result| Student
    
    Student -->|View Schedule| S1
    S1 --> S2 --> S3 --> S4
    S4 -->|Weekly Schedule| Student
    
    Admin -->|Manage Data| M1
    M1 --> M2 --> M3 --> M4
    M4 -->|Status| Admin
```

## Data Flow Summary

### Student Processes:
1. **Authentication**: Login validation and session management
2. **Dashboard**: View enrollment statistics and current semester info
3. **Course Enrollment**: Enroll/unenroll from available courses
4. **Schedule Viewing**: Display weekly class routine
5. **AJAX Operations**: Quick enrollment actions

### Admin Processes:
1. **Department Management**: CRUD operations on departments
2. **Course Management**: Manage courses and their details
3. **Schedule Management**: Set up course schedules and sections
4. **Student Management**: Create students and auto-generate user accounts
5. **Enrollment Management**: Oversee student enrollments
6. **Semester Management**: Manage academic semesters

### Key Data Flows:
- **User Authentication** → Student Profile → Dashboard Statistics
- **Course Selection** → Enrollment Validation → Database Update
- **Student Enrollments** → Course Schedules → Weekly Routine
- **Admin Operations** → Data Validation → Database CRUD → Status Response