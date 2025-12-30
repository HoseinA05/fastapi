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
    print(student)
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
    Format student data into a nice message
    student is a tuple: (id, username, created_at, email, phone_number, last_seen, is_verified, birthday)
    """
    print(teacher)
    id, username, name, created_at, email, phone_number, last_seen, is_verfied, birthday, about_me, job_title = teacher

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
