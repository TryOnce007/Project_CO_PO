# 📊 OBE Management System

An **Outcome-Based Education (OBE) Management System** built using Flask to manage, track, and analyze Course Outcomes (CO), Program Outcomes (PO), and student performance in an efficient and structured way.

---

## 🚀 Overview

This system automates the academic assessment process based on OBE principles. It allows faculty members and HODs to manage COs, upload marks, and generate attainment reports with validation and preview features.

It ensures **data accuracy, traceability, and proper CO-PO mapping** for academic accreditation requirements.

---

## ✨ Features

### 👨‍🏫 Faculty Module
- Add and manage Course Outcomes (CO)
- View assigned COs based on faculty mapping
- Upload student marks using Excel file
- Preview data before final submission
- Edit marks before saving
- Validate marks (obtained ≤ total, no negative values)
- Detect duplicate entries (roll_no + CO + session)
- Update existing marks or skip duplicates

---

### 📂 Marks Management
- Excel-based bulk upload
- Live preview before saving
- Inline editing of marks
- Indirect and direct marks support
- Roll number-based student mapping
- Auto student creation if not found

---

### 📊 CO-PO Analytics Dashboard
- CO attainment calculation
- Visual reports (bar charts, radar charts)
- Performance tracking per session
- Branch-wise analysis

---

### 🏫 Admin / HOD Features
- View all COs across courses
- Filter COs by course
- Manage faculty-course assignments
- Oversee overall performance reports

---

## 📌 OBE Calculation Logic

### 🔵 Direct Assessment (80%)
Includes:
- Internal exams
- Assignments
- Quizzes
- Lab performance

### 🟡 Indirect Assessment (20%)
Includes:
- Feedback forms
- Course exit surveys
- Student perception analysis

---

## 📊 CO Attainment Formula
Final CO Attainment = (Direct Assessment × 0.8) + (Indirect Assessment × 0.2)

---

## ⚙️ Key Functional Highlights

- ✔ Roll number-based data processing
- ✔ Duplicate detection (roll_no + co_id + session)
- ✔ Real-time validation before submission
- ✔ Editable preview before final save
- ✔ Prevention of invalid marks entry
- ✔ Secure session-based upload handling
- ✔ Batch and branch-wise filtering
- ✔ Faculty-specific CO assignment system

---

## 📂 System Modules
├── Authentication Module
├── Faculty Dashboard
├── CO Management Module
├── Marks Upload Module
├── Preview & Validation Module
├── CO-PO Analytics Module


---

## 🛠️ Tech Stack

- **Backend:** Flask (Python)
- **Database:** MySQL / SQLite (SQLAlchemy ORM)
- **Frontend:** HTML, Bootstrap 5
- **Data Processing:** Pandas
- **Visualization:** Chart.js (or similar)

---

## 📁 Excel Upload Format

| Roll No | CO ID | Obtained | Total | Indirect Obtained | Indirect Total |
|--------|------|----------|-------|------------------|-----------------|
| 101    | 1    | 45       | 50    | 8                | 10              |

---

## ⚠️ Validation Rules

- Obtained marks must be ≤ Total marks
- Marks cannot be negative
- Roll number is mandatory
- CO ID must exist in system
- Duplicate entries are detected automatically

---

## 🔐 Security Features

- Session-based upload preview
- Server-side validation
- Duplicate prevention logic
- Controlled data commit after confirmation

---

## 📌 Notes

- This system is designed strictly for **Outcome-Based Education (OBE)** academic environments.
- It ensures structured CO-PO mapping aligned with accreditation standards like **NBA/NAAC**.

---

## 📈 Future Enhancements

- AI-based performance prediction
- Automatic CO-PO mapping suggestions
- Student-level analytics dashboard
- PDF report generation
- API integration for LMS systems

---

## 👨‍💻 Developer

Care_n_Trust


Developed for academic use in OBE-based institutions.

---

## 📄 License

This project is for educational purposes.