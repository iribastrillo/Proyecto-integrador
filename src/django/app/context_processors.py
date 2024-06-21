def get_role_processor(request):
    professor = request.user.profesor_set.all()
    student = request.user.alumno_set.all()
    if professor.exists():
        return {"role": professor.first()}
    if student.exists():
        return {"role": student.first()}
