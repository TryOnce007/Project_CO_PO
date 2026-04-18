from backend import db
from backend.models.course import Course
from backend.models.po import PO
from backend.models.co import CO
from backend.models.co_po_map import COPOMap
from backend.models.professor import Professor


class COPOService:

    @staticmethod
    def get_page_data(hod_id):

        hod = Professor.query.get(hod_id)

        if not hod:
            return None, [], [], []

        courses = Course.query.filter_by(branch=hod.branch).all()
        pos = PO.query.filter_by(branch=hod.branch).all()

        return hod, courses, pos


    @staticmethod
    def get_cos(course_id):

        if not course_id:
            return []

        return CO.query.filter_by(course_id=course_id).all()



    @staticmethod
    def save_mapping(course_id, co_id, po_id, level):

        # validation
        if not all([course_id, co_id, po_id, level]):
            return False, "All fields are required!"

        try:
            level = int(level)
        except:
            return False, "Invalid level"

        if level not in [1, 2, 3]:
            return False, "Level must be 1, 2, or 3"

        existing = COPOMap.query.filter_by(
            co_id=co_id,
            po_id=po_id
        ).first()

        if existing:
            existing.level = level
            message = "Mapping updated!"
        else:
            db.session.add(COPOMap(
                co_id=co_id,
                po_id=po_id,
                level=level
            ))
            message = "Mapping created!"

        db.session.commit()
        return True, message