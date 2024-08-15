
def generate_course_identifier_name(course_name):
    """
    Generates the course identifier based on the first three characters of the course name.
    """
    words = course_name.split()  # Split the course name into words

    # Get the first three characters of the first word
    first_word_initials = words[0][:3]

    # Get the first three characters of the second word (if available)
    second_word_initials = words[1][:3] if len(words) > 1 else ""

    return f"{first_word_initials}{second_word_initials}-"