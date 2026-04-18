import pandas as pd
from backend import db
from flask import session as flask_session
from backend.models.student import Student
from backend.models.marks import Mark
from backend.models.session import AcademicSession
from backend.models.course_assignment import CourseAssignment
from backend.models.batch import Batch
from backend.models.course import Course
from backend.models.branch import Branch



def process_upload(file):

    df = pd.read_excel(file)

    df.columns = (
        df.columns
        .str.strip()
        .str.lower()
        .str.replace(" ", "_")
    )

    required = {"roll_no", "co_id", "obtained", "total"}

    if not required.issubset(df.columns):
        raise Exception("Invalid file format")

    df = df[list(required)].drop_duplicates()

    preview_data = []
    error_rows = []

    session_obj = AcademicSession.query.filter_by(name="Auto Session").first()

    if not session_obj:
        session_obj = AcademicSession(name="Auto Session")
        db.session.add(session_obj)
        db.session.commit()

    for idx, row in df.iterrows():

        try:
            roll_no = str(row["roll_no"]).strip()
            co_id = int(float(row["co_id"]))
            obtained = float(row["obtained"])
            total = float(row["total"])

            if total <= 0 or obtained < 0:
                error_rows.append(idx + 2)
                continue

            student = Student.query.filter_by(roll_no=roll_no).first()

            preview_data.append({
                "roll_no": roll_no,
                "co_id": co_id,
                "obtained": obtained,
                "total": total,
                "student_found": bool(student),
                "student_id": student.id if student else None,
                "session_id": session_obj.id,
                "session": session_obj.name
            })

        except Exception:
            error_rows.append(idx + 2)

    return preview_data, error_rows, session_obj.name



def confirm_upload():

    data = flask_session.get("upload_preview")

    if not data:
        raise Exception("No upload session found")

    success = 0
    failed = 0

    for row in data:

        try:
            if not row["student_found"]:
                failed += 1
                continue

            mark = Mark.query.filter_by(
                student_id=row["student_id"],
                co_id=row["co_id"],
                session=row["session_id"]
            ).first()

            if mark:
                mark.obtained = row["obtained"]
                mark.total = row["total"]
            else:
                db.session.add(Mark(
                    student_id=row["student_id"],
                    co_id=row["co_id"],
                    obtained=row["obtained"],
                    total=row["total"],
                    session=row["session_id"]
                ))

            success += 1

        except Exception:
            failed += 1

    db.session.commit()
    flask_session.pop("upload_preview", None)

    return success, failed



def get_student_marks_grid_data(batch, branch, co_id, session_id, Student, Mark):

    students = Student.query.filter(
        Student.batch_id == batch,
        Student.branch == branch
    ).all()

    student_ids = [s.id for s in students]

    marks = Mark.query.filter(
        Mark.student_id.in_(student_ids),
        Mark.co_id == co_id,
        Mark.session == session_id
    ).all()

    marks_map = {m.student_id: m for m in marks}

    result = []

    for s in students:
        mark = marks_map.get(s.id)

        result.append({
            "student_id": s.id,
            "roll_no": s.roll_no,
            "name": getattr(s, "name", ""),
            "total": mark.total if mark else "",
            "obtained": mark.obtained if mark else "",
            "mark_id": mark.id if mark else None
        })

    return result



class MarksService:


    @staticmethod
    def get_student_marks_grid(batch, branch, co_id, session_id):

        if not batch or not branch or not co_id or not session_id:
            return []

        if not str(batch).isdigit() or not str(co_id).isdigit() or not str(session_id).isdigit():
            return []

        batch = int(batch)
        co_id = int(co_id)
        session_id = int(session_id)

        students = Student.query.filter(
            Student.batch_id == batch,
            Student.branch == branch
        ).all()

        student_ids = [s.id for s in students]

        marks = Mark.query.filter(
            Mark.student_id.in_(student_ids),
            Mark.co_id == co_id,
            Mark.session == session_id
        ).all()

        marks_map = {m.student_id: m for m in marks}

        result = []

        for s in students:
            mark = marks_map.get(s.id)

            result.append({
                "student_id": s.id,
                "roll_no": s.roll_no,
                "name": getattr(s, "name", ""),
                "total": mark.total if mark else "",
                "obtained": mark.obtained if mark else "",
                "mark_id": mark.id if mark else None
            })

        return result



    @staticmethod
    def save_mark_row(data):

        try:
            student_id = int(data["student_id"])
            co_id = int(data["co_id"])
            session_id = int(data["session"])
            total = float(data["total"])
            obtained = float(data["obtained"])

        except (TypeError, ValueError):
            return {"error": "Invalid input"}

        if total < 0:
            return {"error": "Total cannot be negative"}

        if obtained > total:
            return {"error": "Obtained cannot exceed total"}

        mark = Mark.query.filter_by(
            student_id=student_id,
            co_id=co_id,
            session=session_id
        ).first()

        if mark:
            mark.total = total
            mark.obtained = obtained
        else:
            db.session.add(Mark(
                student_id=student_id,
                co_id=co_id,
                session=session_id,
                total=total,
                obtained=obtained
            ))

        db.session.commit()

        return {"success": True}
    


def get_assigned_courses(faculty_id):
        assigned_course_ids = (
            db.session.query(CourseAssignment.course_id)
            .filter(CourseAssignment.faculty_id == faculty_id)
            .subquery()
        )

        courses = Course.query.filter(
            Course.id.in_(assigned_course_ids)
        ).all()

        return courses


def get_static_academic_data():
    batches = Batch.query.all()
    branches = Branch.query.all()
    sessions = AcademicSession.query.all()

    return {
        "batches": batches,
        "branches": branches,
        "sessions": sessions
    }