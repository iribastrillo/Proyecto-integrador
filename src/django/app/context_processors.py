from app import authorization

def get_role_processor(request):
    if request.user.is_anonymous:
        return {}
    if authorization.is_staff(request.user):
        return {"role": "staff"}
    if authorization.is_teacher(request.user):
        return {"role": "teacher"}
    if authorization.is_student(request.user):
        return {"role": "student"}
    
