class StudentAlreadyEnroledException (Exception):
    def __init__(self):
        self.message = "Student has an active enrolment to this group."
        super().__init__(self.message)
        

class StudentHasEnroledException (Exception):
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
  
        
class ProductsDoNotMatchException (Exception):
    def __init__(self):
        self.message = "Products do not match."
        super().__init__(self.message)
        

class NoAlternativeException (Exception):
    def __init__(self):
        self.message = "There are no group alternatives."
        super().__init__(self.message)