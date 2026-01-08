from datetime import datetime


def format_date(date_string):
    """Convert database date to readable format"""
    if not date_string:
        return "N/A"

    try:
        # If date_string is already a datetime object
        if isinstance(date_string, datetime):
            return date_string.strftime("%d %b %Y, %H:%M")

        # If it's a string, parse it first
        date_obj = datetime.strptime(str(date_string), "%Y-%m-%d %H:%M:%S")
        return date_obj.strftime("%d %b %Y, %H:%M")
    except:
        return str(date_string)


def calculate_age(birthday_string):
    """Calculate age from birthday"""
    if not birthday_string:
        return "N/A"

    try:
        birth_date = datetime.strptime(str(birthday_string), "%Y-%m-%d").date()
        today = datetime.now().date()
        age = today.year - birth_date.year - \
            ((today.month, today.day) < (birth_date.month, birth_date.day))
        return age
    except:
        return "N/A"


# Student Info Formatter
def format_student_info(student):
    """
    Format student data into a nice message
    student is a tuple: (id, username, name, created_at, email, phone_number, last_seen, is_verified, birthday)
    """
    # print(student)

    id, username, name, created_at, email, phone_number, last_seen, is_verfied, birthday = student

    verified_status = "✅ Verified" if is_verfied else "❌ Not Verified"

    # Format dates nicely
    created_date = format_date(created_at)
    last_seen_date = format_date(last_seen)

    # Calculate age from birthday
    age = calculate_age(birthday)

    details = f"""
  <b>👤 Student Profile</b>

  <b>Name:</b> {name}
  <b>Username:</b> {username}
  <b>Email:</b> {email}
  <b>Phone:</b> {phone_number}
  <b>Birthday:</b> {birthday} (Age: {age})
  <b>Account Status:</b> {verified_status}

  <b>📅 Account Info</b>
  <b>Joined:</b> {created_date}
  <b>Last Seen:</b> {last_seen_date}
  <b>ID:</b> <code>{id}</code>
  """
    return details.strip()


# Teacher Info Formatter
def format_teacher_info(teacher):
    """
    Format teacher data into a nice message
    teacher is a tuple: (id, username, name, created_at, email, phone_number, last_seen, is_verified, birthday, about_me, job_title)
    """
    # print(teacher)

    id, username, name, created_at, email, phone_number, last_seen, is_verfied, birthday, about_me, job_title = teacher

    verified_status = "✅ Verified" if is_verfied else "❌ Not Verified"

    # Format dates nicely
    created_date = format_date(created_at)
    last_seen_date = format_date(last_seen)

    # Calculate age from birthday
    age = calculate_age(birthday)

    details = f"""
  <b>👤 Teacher Profile</b>

  <b>Name:</b> {name}
  <b>Username:</b> {username}
  <b>Job Title:</b> {job_title}
  <b>About Me:</b> {about_me}

  <b>Email:</b> {email}
  <b>Phone:</b> {phone_number}
  <b>Birthday:</b> {birthday} (Age: {age})
  <b>Account Status:</b> {verified_status}

  <b>📅 Account Info</b>
  <b>Joined:</b> {created_date}
  <b>Last Seen:</b> {last_seen_date}
  <b>ID:</b> <code>{id}</code>
  """
    return details.strip()

# Course Info Formatter


def format_course_info(course):
    """
    Format course data into a nice message
    course is a tuple: (id, name, created_at, teacher_id, updated_at, description, difficulty, language, avgerage_rate)
    """
    # print(course)

    id, name, created_at, teacher_id, updated_at, description, difficulty, language, avgerage_rate = course

    # Format dates nicely
    created_date = format_date(created_at)
    updated_at = format_date(updated_at)

    details = f"""
  <b>📚 Course Profile</b>

  <b>Name:</b> {name}
  <b>⭐️ Average Rating:</b> {avgerage_rate}
  <b>Description:</b>
  {description}

  <b>Language:</b> {language}
  <b>Difficulty:</b> {difficulty}

  <b>📅 Course Info</b>
  <b>Created At:</b> {created_date}
  <b>Last Updated At:</b> {updated_at}
  <b>ID:</b> <code>{id}</code>
  """
    return details.strip()


def format_course_review(review):
    """
    Formate course review into a nice message
    :param review: tuple(body: str, rate: int, student_name: str, course_name: str, created_at: date, updated_at: date)
    """

    reviewBody, rate, student_name, course_name, created_at, updated_at = review

    created_date = format_date(created_at)
    updated_at = format_date(updated_at)

    details = f"""
  <b>✉️ Review</b>

  <b>rate:</b> {'⭐️' * rate}
  <b>Body:</b>\n{reviewBody}

  <b>Course name:</b> {course_name}
  <b>Student name:</b> {student_name}

  <b>📅 Review Info</b>
  <b>Created At:</b> {created_date}
  <b>Last Updated At:</b> {updated_at}
  """
    return details.strip()
