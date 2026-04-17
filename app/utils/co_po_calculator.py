from app.models.marks import Mark
from app.models.co_po_map import COPOMap



def calculate_co_stats(cos, selected_session_id):

    co_stats = []
    co_levels = {}

    for co in cos:

        if selected_session_id:
            marks = Mark.query.filter_by(
                co_id=co.id,
                session=selected_session_id
            ).all()
        else:
            marks = Mark.query.filter_by(co_id=co.id).all()

        total_obtained = sum(m.obtained for m in marks)
        total_possible = sum(m.total for m in marks)

        percent = (total_obtained / total_possible * 100) if total_possible else 0

        level = (
            3 if percent >= 70 else
            2 if percent >= 60 else
            1 if percent >= 50 else
            0
        )

        co_levels[co.id] = level

        co_stats.append({
            "co": co,
            "percent": round(percent, 2),
            "level": level
        })

    return co_stats, co_levels




def calculate_po_stats(pos, co_levels):

    po_stats = []

    for po in pos:

        mappings = COPOMap.query.filter_by(po_id=po.id).all()

        numerator = sum(
            co_levels.get(m.co_id, 0) * m.level
            for m in mappings
        )

        denominator = sum(
            m.level for m in mappings if m.co_id in co_levels
        )

        avg_level = numerator / denominator if denominator else 0

        po_stats.append({
            "po": po,
            "avg_level": round(avg_level, 2)
        })

    return po_stats