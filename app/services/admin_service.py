from app import db
from app.models.co import CO
from app.models.student import Student
from app.models.marks import Mark
from app.models.co_po_map import COPOMap
from app.models.course_assignment import CourseAssignment
from app.models.po import PO
from app.models.course import Course
from filters import row_to_dict




def get_dashboard_data(user_id, role):

    if role == 'HOD':

        cos = CO.query.all()
        students = Student.query.all()
        marks = Mark.query.all()
        copomaps = COPOMap.query.all()

    else:

        assigned_course_ids = db.session.query(
            CourseAssignment.course_id
        ).filter(
            CourseAssignment.faculty_id == user_id
        ).subquery()

        cos = CO.query.filter(
            CO.course_id.in_(assigned_course_ids)
        ).all()

        co_ids = [c.id for c in cos]

        marks = Mark.query.filter(Mark.co_id.in_(co_ids)).all()
        copomaps = COPOMap.query.filter(COPOMap.co_id.in_(co_ids)).all()

        student_ids = {m.student_id for m in marks}
        students = Student.query.filter(Student.id.in_(student_ids)).all()

    return {
    "cos_list": [row_to_dict(c, ["id", "description", "course_id"]) for c in cos],
    "students_list":[row_to_dict(s, ['id', 'roll_no']) for s in students],
    "marks_list": [row_to_dict(m, ['id', 'student_id', 'co_id', 'obtained', 'total']) for m in marks],
    "copomap_list": [row_to_dict(cpm, ['id', 'co_id', 'po_id', 'level']) for cpm in copomaps]
}



def update_record(table, id, data):

    try:

        if table == 'cos':
            row = CO.query.get_or_404(id)
            row.description = data.get('description', row.description)
            row.course_id = int(data.get('course_id', row.course_id))

        elif table == 'pos':
            row = PO.query.get_or_404(id)
            row.description = data.get('description', row.description)

        elif table == 'courses':
            row = Course.query.get_or_404(id)
            row.name = data.get('name', row.name)
            row.code = data.get('code', row.code)

        elif table == 'students':
            row = Student.query.get_or_404(id)
            row.roll_no = data.get('roll_no', row.roll_no)

        elif table == 'marks':
            row = Mark.query.get_or_404(id)
            row.student_id = int(data.get('student_id', row.student_id))
            row.co_id = int(data.get('co_id', row.co_id))
            row.obtained = float(data.get('obtained', row.obtained))
            row.total = float(data.get('total', row.total))

        elif table == 'co_po_map':
            row = COPOMap.query.get_or_404(id)

            level = int(data.get('level', row.level))
            if level < 1 or level > 3:
                return False, "Level must be between 1 and 3"

            row.co_id = int(data.get('co_id', row.co_id))
            row.po_id = int(data.get('po_id', row.po_id))
            row.level = level

        else:
            return False, "Invalid table"

        db.session.commit()
        return True, "Updated successfully"

    except Exception as e:
        return False, str(e)



def delete_record(table, id):

    try:

        model_map = {
            'cos': CO,
            'pos': PO,
            'students': Student,
            'marks': Mark,
            'co_po_map': COPOMap,
            'courses': Course
        }

        model = model_map.get(table)

        if not model:
            return False, "Invalid table"

        row = model.query.get_or_404(id)

        db.session.delete(row)
        db.session.commit()

        return True, f"Deleted from {table}"

    except Exception as e:
        return False, str(e)