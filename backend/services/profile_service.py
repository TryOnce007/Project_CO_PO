from backend.models.professor import Professor
from backend import db


def get_professor_profile(professor_id):
    return Professor.query.get(professor_id)



def update_professor_profile(professor, username, phone):

    if not username or not phone:
        return False, "Username and Phone number cannot be empty."

    professor.username = username
    professor.phone = phone

    db.session.commit()

    return True, "Profile updated successfully!"