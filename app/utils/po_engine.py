from app.models.co_po_map import COPOMap
from app.models.co import CO
from app.models.po import PO

from app.models.marks import Mark


def calculate_po_attainment(course_id, session_id):

    pos = []
    pos = PO.query.all()

    po_stats = []

    for po in pos:

        mappings = COPOMap.query.filter_by(po_id=po.id).all()

        co_levels = []

        for m in mappings:

            co = CO.query.get(m.co_id)

            if not co or co.course_id != course_id:
                continue

            marks = Mark.query.filter_by(
                co_id=co.id,
                session=session_id
            ).all()

            if not marks:
                co_levels.append(0)
                continue

            total_obtained = sum(x.obtained for x in marks)
            total_max = sum(x.total for x in marks)

            percent = (total_obtained / total_max * 100) if total_max else 0

            level = (
                3 if percent >= 70 else
                2 if percent >= 60 else
                1 if percent >= 50 else
                0
            )

            co_levels.append(level)

        avg_level = sum(co_levels) / len(co_levels) if co_levels else 0

        po_stats.append({
            "po": po,
            "avg_level": round(avg_level, 2)
        })

    return po_stats