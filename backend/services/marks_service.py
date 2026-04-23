import math
import pandas as pd
from backend import db
from sqlalchemy import select
from backend.models.student import Student
from backend.models.marks import Mark
from backend.models.session import AcademicSession
from backend.models.course_assignment import CourseAssignment
from backend.models.batch import Batch
from backend.models.course import Course
from backend.models.branch import Branch




def safe_float(value):
    try:
        if value in [None, "-", ""]:
            return 0.0   
        return float(value)
    except:
        return 0.0

# def get_student_marks_grid_data(batch, branch, co_id, session_id, Student, Mark):

#     students = Student.query.filter(
#         Student.batch_id == batch,
#         Student.branch == branch
#     ).all()

#     student_ids = [s.id for s in students]

#     marks = Mark.query.filter(
#         Mark.student_id.in_(student_ids),
#         Mark.co_id == co_id,
#         Mark.session == session_id
#     ).all()

#     marks_map = {m.student_id: m for m in marks}

#     result = []

#     for s in students:
#         mark = marks_map.get(s.id)

#         result.append({
#             "student_id": s.id,
#             "roll_no": s.roll_no,
#             "name": getattr(s, "name", ""),
#             "total": mark.total if mark else "",
#             "obtained": mark.obtained if mark else "",
#             "mark_id": mark.id if mark else None
#         })

#     return result



class MarksService:



    @staticmethod
    def get_student_marks_grid(batch, branch, co_id, session_id, page=1, per_page=12):

        if not batch or not branch or not co_id or not session_id:
            return []

        if not str(batch).isdigit() or not str(co_id).isdigit() or not str(session_id).isdigit():
            return []

        batch = int(batch)
        co_id = int(co_id)
        session_id = int(session_id)

        page = max(int(page or 1), 1)

        marks_query = Mark.query.filter(
            Mark.co_id == co_id,
            Mark.session == session_id
        )

        total_marks = marks_query.count()

        if total_marks == 0:
            return {
                "data": [],
                "page": page,
                "per_page": per_page,
                "total_pages": 0,
                "total_students": 0
            }

        total_pages = math.ceil(total_marks / per_page)

        if page > total_pages:
            page = total_pages

        offset = (page - 1) * per_page

        marks = marks_query.order_by(Mark.id).offset(offset).limit(per_page).all()

        student_ids = [m.student_id for m in marks]

        students = Student.query.filter(
            Student.id.in_(student_ids),
            Student.batch_id == batch,
            Student.branch == branch
        ).all()

        student_map = {s.id: s for s in students}
        marks_map = {m.student_id: m for m in marks}

        result = []

        for m in marks:
            s = student_map.get(m.student_id)

            if not s:
                continue

            result.append({
                "student_id": s.id,
                "roll_no": s.roll_no,
                "name": getattr(s, "name", ""),
                "total": m.total,
                "obtained": m.obtained,
                "indirect_total": m.indirect_total,
                "indirect_obtained": m.indirect_obtained,
                "mark_id": m.id
            })

        return {
            "data": result,
            "page": page,
            "per_page": per_page,
            "total_pages": total_pages,
            "total_students": total_marks
        }



    @staticmethod
    def save_mark_row(data):

        try:
            student_id = int(data["student_id"])
            co_id = int(data["co_id"])
            session_id = int(data["session"])
            total = float(data["total"])
            obtained = float(data["obtained"])
            obtained_indirect = float(data["indirect_obtained"])
            total_indirect = float(data["indirect_total"])

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
            mark.indirect_total = total_indirect
            mark.indirect_obtained = obtained_indirect
        else:
            db.session.add(Mark(
                student_id=student_id,
                co_id=co_id,
                session=session_id,
                total=total,
                obtained=obtained,
                indirect_total = total_indirect,
                indirect_obtained = obtained_indirect
            ))

        db.session.commit()

        return {"success": True}
    

    @staticmethod
    def get_sessions():
        return AcademicSession.query.all()
    


    @staticmethod
    def get_batches():
        return Batch.query.all()
    

    @staticmethod
    def get_all_branches():
        return Branch.query.all()
    


    @staticmethod
    def process_upload(file, session_id, branch, batch_id):

        session_obj = AcademicSession.query.get(session_id)

        df = pd.read_excel(file, engine="openpyxl")

        df.columns = (
            df.columns.str.strip()
            .str.lower()
            .str.replace(" ", "_")
        )

        df = df.drop_duplicates(subset=["roll_no", "co_id"])

        preview_data = []

        for _, row in df.iterrows():

            roll_no = str(row["roll_no"]).strip().lstrip("0")
            co_id = int(row["co_id"])

            obtained = float(row["obtained"]) if not pd.isna(row["obtained"]) else 0.0
            total = float(row["total"]) if not pd.isna(row["total"]) else 0.0

            student = Student.query.filter_by(
                roll_no=roll_no,
                branch=branch,
                batch_id=batch_id
            ).first()

            existing_mark = None
            if student:
                existing_mark = Mark.query.filter_by(
                    student_id=student.id,
                    co_id=co_id,
                    session=session_obj.id
                ).first()

            preview_data.append({
                "roll_no": roll_no,
                "co_id": co_id,
                "obtained": obtained,
                "total": total,

                "student_found": bool(student),
                "student_id": student.id if student else None,

                "duplicate": bool(existing_mark),   
                "session_id": session_obj.id,
                "session_name": session_obj.name,

                "branch": branch,
                "batch_id": batch_id
            })

        return preview_data
    
    
    @staticmethod
    def confirm_upload(data):

        success = 0
        failed = 0
        skipped_duplicates = 0

        for row in data:

            try:
                roll_no = str(row["roll_no"]).strip().lstrip("0")
                branch = row["branch"]
                batch_id = row["batch_id"]
                session_id = row["session_id"]
                co_id = row["co_id"]

                

                student = Student.query.filter_by(
                    roll_no=roll_no,
                    branch=branch,
                    batch_id=batch_id
                ).first()

                if not student:
                    student = Student(
                        roll_no=roll_no,
                        branch=branch,
                        batch_id=batch_id
                    )
                    db.session.add(student)
                    db.session.flush()

                

                obtained = float(row.get("obtained") or 0)
                total = float(row.get("total") or 0)

                indirect_obtained = row.get("indirect_obtained")
                indirect_total = row.get("indirect_total")

                indirect_obtained = float(indirect_obtained) if indirect_obtained not in [None, "", "-"] else None
                indirect_total = float(indirect_total) if indirect_total not in [None, "", "-"] else None

               

                existing_mark = db.session.query(Mark).join(Student).filter(
                    Student.roll_no == roll_no,
                    Student.branch == branch,
                    Student.batch_id == batch_id,
                    Mark.co_id == co_id,
                    Mark.session == session_id
                ).first()

                if existing_mark:
                    existing_mark.obtained = obtained
                    existing_mark.total = total
                    existing_mark.indirect_obtained = indirect_obtained
                    existing_mark.indirect_total = indirect_total

                    skipped_duplicates += 1

                else:
                    db.session.add(Mark(
                        student_id=student.id,
                        co_id=co_id,
                        obtained=obtained,
                        total=total,
                        indirect_obtained=indirect_obtained,
                        indirect_total=indirect_total,
                        session=session_id
                    ))

                success += 1

            except Exception as e:
                db.session.rollback()
                failed += 1

        db.session.commit()

        return success, failed, skipped_duplicates
                


def get_assigned_courses(faculty_id):
    assigned_course_ids = select(CourseAssignment.course_id).where(
        CourseAssignment.faculty_id == faculty_id
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


