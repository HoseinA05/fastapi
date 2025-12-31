import logging
import database.connection as connection

logger = logging.getLogger(__name__)


class Students:
    def getAllStudents():
        conn = None
        try:
            conn = connection.get_db_connection()
            if not conn:
                return None

            cursor = conn.cursor()
            cursor.execute("SELECT id,username FROM students")
            result = cursor.fetchall()
            cursor.close()

            return result if result else None
        except Exception as e:
            logger.error(f"Database query error in getAllStudents: {e}")
            return None
        finally:
            if conn:
                connection.release_db_connection(conn)

    def getStudentById(student_id):
        conn = None
        try:
            conn = connection.get_db_connection()
            if not conn:
                return None

            cursor = conn.cursor()
            cursor.execute(
                "SELECT id,username, name, created_at, email, phone_number, last_seen, is_verfied, birthday FROM students WHERE id = %s", (student_id,))
            result = cursor.fetchall()
            cursor.close()

            return result[0] if result else None
        except Exception as e:
            logger.error(f"Database query error in getStudentById: {e}")
            return None
        finally:
            if conn:
                connection.release_db_connection(conn)


class Teachers:
    def getAllTeachers():
        conn = None
        try:
            conn = connection.get_db_connection()
            if not conn:
                return None

            cursor = conn.cursor()
            cursor.execute("SELECT id,username FROM teachers")
            result = cursor.fetchall()
            cursor.close()

            return result if result else None
        except Exception as e:
            logger.error(f"Database query error in getAllTeachers: {e}")
            return None
        finally:
            if conn:
                connection.release_db_connection(conn)

    def getTeachertById(teacher_id):
        conn = None
        try:
            conn = connection.get_db_connection()
            if not conn:
                return None

            cursor = conn.cursor()
            cursor.execute(
                "SELECT id, username, name, created_at, email, phone_number, last_seen, is_verfied, birthday, about_me, job_title FROM teachers WHERE id = %s", (teacher_id, ))
            result = cursor.fetchall()
            cursor.close()

            return result[0] if result else None
        except Exception as e:
            logger.error(f"Database query error in getTeacherById: {e}")
            return None
        finally:
            if conn:
                connection.release_db_connection(conn)

    def createTeacher(name, email, phone_number, password, username, birthday, about_me, job_title):
        conn = None
        try:
            conn = connection.get_db_connection()
            if not conn:
                return False

            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO teachers (name, email, phone_number, hashed_password, username, birthday, about_me, job_title) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)",
                (name, email, phone_number, password,
                 username, birthday, about_me, job_title)
            )
            conn.commit()
            cursor.close()

            return True
        except Exception as e:
            logger.error(f"Database query error in createTeacher: {e}")
            return False
        finally:
            if conn:
                connection.release_db_connection(conn)

    def updateTeacher(teacher_id, **fields):
        if not fields:
            return False  # nothing to update

        conn = None
        try:
            conn = connection.get_db_connection()
            if not conn:
                return False

            cursor = conn.cursor()

            # Build dynamic SET clause
            columns = []
            values = []

            for key, value in fields.items():
                columns.append(f"{key} = %s")
                values.append(value)

            values.append(teacher_id)

            query = f"""
                UPDATE teachers
                SET {', '.join(columns)}
                WHERE id = %s
            """

            cursor.execute(query, tuple(values))
            conn.commit()
            cursor.close()

            return True

        except Exception as e:
            logger.error(f"Database query error in updateTeacher: {e}")
            return False

        finally:
            if conn:
                connection.release_db_connection(conn)
