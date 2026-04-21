from backend.models.marks import Mark
from backend.models.co_po_map import COPOMap



def calculate_co_stats(cos, selected_session_id):

    co_stats = []
    co_final_scores = {}   # used for PO

    THRESHOLD = 60
    TARGET = 70

    for co in cos:

        query = Mark.query.filter(Mark.co_id == co.id)

        if selected_session_id:
            query = query.filter(Mark.session == selected_session_id)

        marks = query.all()

        if not marks:
            co_stats.append({
                "co": co,
                "direct_percent": 0,
                "indirect_percent": 0,
                "percent": 0,
                "level": 0
            })
            co_final_scores[co.id] = 0
            continue

        # ---------------- MARKS ----------------
        total_students = len(marks)

        # ---------------- THRESHOLD CHECK ----------------
        students_meeting_target = sum(
            1 for m in marks
            if (m.obtained / m.total * 100) >= THRESHOLD
        )

        direct_percent = (students_meeting_target / total_students) * 100

        # ---------------- INDIRECT ----------------
        total_indirect_obtained = sum(m.indirect_obtained or 0 for m in marks)
        total_indirect_possible = sum(m.indirect_total or 0 for m in marks)

        indirect_percent = (
            (total_indirect_obtained / total_indirect_possible) * 100
            if total_indirect_possible else 0
        )

        # ---------------- FINAL CO (80/20) ----------------
        final_co_percent = (0.8 * direct_percent) + (0.2 * indirect_percent)

        # ---------------- LEVEL (TARGET COMPARISON) ----------------
        level = (
            3 if final_co_percent >= TARGET else
            2 if final_co_percent >= (TARGET - 10) else
            1 if final_co_percent >= (TARGET - 20) else
            0
        )

        # store FINAL CO for PO calculation
        co_final_scores[co.id] = final_co_percent

        co_stats.append({
    "co": {
        "id": co.id,
        "description": co.description
    },
    "direct_percent": round(direct_percent, 2),
    "indirect_percent": round(indirect_percent, 2),
    "percent": round(final_co_percent, 2),
    "level": level
})
        




    return co_stats, co_final_scores



def calculate_po_stats(pos, co_final_scores):

    po_stats = []

    for po in pos:

        mappings = COPOMap.query.filter_by(po_id=po.id).all()

        numerator = 0
        denominator = 0

        for m in mappings:

            co_percent = co_final_scores.get(m.co_id, 0)

            # normalize (0–1)
            co_value = co_percent / 100

            numerator += co_value * m.level
            denominator += m.level

        po_attainment = (numerator / denominator) if denominator else 0

        po_stats.append({
            "po": po,
            "avg_level": round(po_attainment * 3, 2),
            "percentage": round(po_attainment * 100, 2)
        })



    return po_stats