class StudentAlreadyEnroledException (Exception):
    def __init__(self):
        self.message = "Student has an active enrolment to this course."
        super().__init__(self.message)
        
class GroupCompleteException (Exception):
    def __init__(self):
        self.message = "Group is full."
        super().__init__(self.message)
        
class TeacherHasGroupsException (Exception):
    def __init__(self):
        self.message = "Teacher teaches groups."
        super().__init__(self.message)