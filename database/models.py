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

    def createStudent(name, email, phone_number, password, username, birthday):
        conn = None
        try:
            conn = connection.get_db_connection()
            if not conn:
                return False

            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO students (name, email, phone_number, hashed_password, username, birthday) VALUES (%s, %s, %s, %s, %s, %s)",
                (name, email, phone_number, password,
                 username, birthday)
            )
            conn.commit()
            cursor.close()

            return True
        except Exception as e:
            logger.error(f"Database query error in createStudent: {e}")
            return False
        finally:
            if conn:
                connection.release_db_connection(conn)

    def updateStudent(student_id, **fields):
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
                columns.append(f"{key} = %s" if key !=
                               'password' else "hashed_password = %s")
                values.append(value)

            values.append(student_id)

            query = f"""
                UPDATE students
                SET {', '.join(columns)}
                WHERE id = %s
            """

            cursor.execute(query, tuple(values))
            conn.commit()
            cursor.close()

            return True

        except Exception as e:
            logger.error(f"Database query error in updateStudent: {e}")
            return False

        finally:
            if conn:
                connection.release_db_connection(conn)

    def deleteStudent(student_id):
        conn = None
        try:
            conn = connection.get_db_connection()
            if not conn:
                return False

            cursor = conn.cursor()
            cursor.execute(
                "DELETE FROM students WHERE id = %s", (student_id,))
            conn.commit()
            cursor.close()

            return True
        except Exception as e:
            logger.error(f"Database query error in deleteStudent: {e}")
            return False
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
                columns.append(f"{key} = %s" if key !=
                               'password' else "hashed_password = %s")
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

    def deleteTeacher(teacher_id):
        conn = None
        try:
            conn = connection.get_db_connection()
            if not conn:
                return False

            cursor = conn.cursor()
            cursor.execute(
                "DELETE FROM teachers WHERE id = %s", (teacher_id,))
            conn.commit()
            cursor.close()

            return True
        except Exception as e:
            logger.error(f"Database query error in deleteTeacher: {e}")
            return False
        finally:
            if conn:
                connection.release_db_connection(conn)


class Courses:
    def getAllCourses():
        conn = None
        try:
            conn = connection.get_db_connection()
            if not conn:
                return None

            cursor = conn.cursor()
            cursor.execute("SELECT id, name FROM courses")
            result = cursor.fetchall()
            cursor.close()

            return result if result else None
        except Exception as e:
            logger.error(f"Database query error in getAllCourses: {e}")
            return None
        finally:
            if conn:
                connection.release_db_connection(conn)

    def getCourseById(course_id):
        conn = None
        try:
            conn = connection.get_db_connection()
            if not conn:
                return None

            cursor = conn.cursor()
            cursor.execute(
                "SELECT id, name, created_at, teacher_id, updated_at, description, difficulty, language FROM courses WHERE id = %s", (course_id, ))
            result = cursor.fetchall()
            cursor.close()

            return result[0] if result else None
        except Exception as e:
            logger.error(f"Database query error in getCourseById: {e}")
            return None
        finally:
            if conn:
                connection.release_db_connection(conn)

    def createCourse(name, teacher_id, description, language, difficulty):
        conn = None
        try:
            conn = connection.get_db_connection()
            if not conn:
                return False

            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO courses (name, teacher_id, description, language, difficulty) VALUES (%s, %s, %s, %s, %s)",
                (name, teacher_id, description, language, difficulty)
            )
            conn.commit()
            cursor.close()

            return True
        except Exception as e:
            logger.error(f"Database query error in createCourse: {e}")
            return False
        finally:
            if conn:
                connection.release_db_connection(conn)

    def updateCourse(course_id, **fields):
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

            values.append(course_id)

            query = f"""
                UPDATE courses
                SET {', '.join(columns)}
                WHERE id = %s
            """

            cursor.execute(query, tuple(values))
            conn.commit()
            cursor.close()

            return True

        except Exception as e:
            logger.error(f"Database query error in updateCourse: {e}")
            return False

        finally:
            if conn:
                connection.release_db_connection(conn)

    def deleteCourse(course_id):
        conn = None
        try:
            conn = connection.get_db_connection()
            if not conn:
                return False

            cursor = conn.cursor()
            cursor.execute(
                "DELETE FROM courses WHERE id = %s", (course_id,))
            conn.commit()
            cursor.close()

            return True
        except Exception as e:
            logger.error(f"Database query error in deleteCourse: {e}")
            return False
        finally:
            if conn:
                connection.release_db_connection(conn)


class Tags:
    def getAllTags():
        conn = None
        try:
            conn = connection.get_db_connection()
            if not conn:
                return None

            cursor = conn.cursor()
            cursor.execute("SELECT id, name, slug FROM tags")
            result = cursor.fetchall()
            cursor.close()

            return result if result else None
        except Exception as e:
            logger.error(f"Database query error in getAllTags: {e}")
            return None
        finally:
            if conn:
                connection.release_db_connection(conn)

    def getTagById(tag_id):
        conn = None
        try:
            conn = connection.get_db_connection()
            if not conn:
                return None

            cursor = conn.cursor()
            cursor.execute(
                "SELECT id, name, slug FROM tags WHERE id = %s", (tag_id, ))
            result = cursor.fetchall()
            cursor.close()

            return result[0] if result else None
        except Exception as e:
            logger.error(f"Database query error in getTagById: {e}")
            return None
        finally:
            if conn:
                connection.release_db_connection(conn)

    def createTag(name, slug):
        conn = None
        try:
            conn = connection.get_db_connection()
            if not conn:
                return False

            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO tags (name, slug) VALUES (%s, %s)",
                (name, slug)
            )
            conn.commit()
            cursor.close()

            return True
        except Exception as e:
            logger.error(f"Database query error in createTag: {e}")
            return False
        finally:
            if conn:
                connection.release_db_connection(conn)

    def updateTag(tag_id, **fields):
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

            values.append(tag_id)

            query = f"""
                UPDATE tags
                SET {', '.join(columns)}
                WHERE id = %s
            """

            cursor.execute(query, tuple(values))
            conn.commit()
            cursor.close()

            return True

        except Exception as e:
            logger.error(f"Database query error in updateTag: {e}")
            return False

        finally:
            if conn:
                connection.release_db_connection(conn)

    def deleteTag(tag_id):
        conn = None
        try:
            conn = connection.get_db_connection()
            if not conn:
                return False

            cursor = conn.cursor()
            cursor.execute(
                "DELETE FROM tags WHERE id = %s", (tag_id,))
            conn.commit()
            cursor.close()

            return True
        except Exception as e:
            logger.error(f"Database query error in deleteTag: {e}")
            return False
        finally:
            if conn:
                connection.release_db_connection(conn)


class Categories:
    def getAllCategories():
        conn = None
        try:
            conn = connection.get_db_connection()
            if not conn:
                return None

            cursor = conn.cursor()
            cursor.execute(
                "SELECT id, name, description, parent_id FROM categories")
            result = cursor.fetchall()
            cursor.close()

            return result if result else None
        except Exception as e:
            logger.error(f"Database query error in getAllCategories: {e}")
            return None
        finally:
            if conn:
                connection.release_db_connection(conn)

    def getCategorieById(category_id):
        conn = None
        try:
            conn = connection.get_db_connection()
            if not conn:
                return None

            cursor = conn.cursor()
            cursor.execute("""
                SELECT
                    c1.id,
                    c1.name,
                    c1.description,
                    COALESCE(c2.name, 'None') AS parent_category
                FROM
                    categories c1
                LEFT JOIN categories c2 ON c2.id = c1.parent_id
                WHERE
                    c1.id = %s;
            """, (category_id,))

            result = cursor.fetchall()
            cursor.close()

            return result[0] if result else None
        except Exception as e:
            logger.error(f"Database query error in getCategoryById: {e}")
            return None
        finally:
            if conn:
                connection.release_db_connection(conn)

    def createCategory(name, description, parent_id=None):
        conn = None
        try:
            conn = connection.get_db_connection()
            if not conn:
                return False

            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO categories (name, description, parent_id) VALUES (%s, %s, %s)",
                (name, description, parent_id)
            )
            conn.commit()
            cursor.close()

            return True
        except Exception as e:
            logger.error(f"Database query error in createCategory: {e}")
            return False
        finally:
            if conn:
                connection.release_db_connection(conn)

    def updateCategory(category_id, **fields):
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

            values.append(category_id)

            query = f"""
                UPDATE categories
                SET {', '.join(columns)}
                WHERE id = %s
            """

            cursor.execute(query, tuple(values))
            conn.commit()
            cursor.close()

            return True

        except Exception as e:
            logger.error(f"Database query error in updateCategory: {e}")
            return False

        finally:
            if conn:
                connection.release_db_connection(conn)

    def deleteCategory(category_id):
        conn = None
        try:
            conn = connection.get_db_connection()
            if not conn:
                return False

            cursor = conn.cursor()
            cursor.execute(
                "DELETE FROM categories WHERE id = %s", (category_id,))
            conn.commit()
            cursor.close()

            return True
        except Exception as e:
            logger.error(f"Database query error in deleteCategory: {e}")
            return False
        finally:
            if conn:
                connection.release_db_connection(conn)
