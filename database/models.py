import logging
import database.connection as connection

import hashlib
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)


class BaseRepository:
    """Base class for all repository classes"""

    table_name = None  # Should be Overrided in subclasses

    @classmethod
    def _execute_query(cls, query_func, operation_name):
        """Execute a SELECT query"""
        conn = None
        try:
            conn = connection.get_db_connection()
            if not conn:
                return None

            cursor = conn.cursor()
            result = query_func(cursor)
            cursor.close()
            return result

        except Exception as e:
            logger.error(
                f"Database error in {cls.__name__}.{operation_name}: {e}")
            return None
        finally:
            if conn:
                connection.release_db_connection(conn)

    @classmethod
    def _execute_mutation(cls, mutation_func, operation_name):
        """Execute an INSERT, UPDATE, or DELETE"""
        conn = None
        try:
            conn = connection.get_db_connection()
            if not conn:
                return False

            cursor = conn.cursor()
            mutation_func(cursor, conn)
            conn.commit()
            cursor.close()
            return True

        except Exception as e:
            logger.error(
                f"Database error in {cls.__name__}.{operation_name}: {e}")
            return False
        finally:
            if conn:
                connection.release_db_connection(conn)


class Admins(BaseRepository):

    SESSION_TIMEOUT_HOURS = 1

    @staticmethod
    def hash_password(password: str) -> str:
        """Hash password using SHA256"""
        return hashlib.sha256(password.encode()).hexdigest()

    @staticmethod
    def login(username: str, password: str, telegram_id: int) -> bool:
        """
        Verify credentials and create a session.
        Returns True if login successful, False otherwise.
        """

        def query(cursor):
            password_hash = Admins.hash_password(password)
            cursor.execute(
                "SELECT id FROM admins WHERE username = %s AND password_hash = %s AND telegram_id = %s",
                (username, password_hash, telegram_id)
            )
            result = cursor.fetchone()
            return result is not None

        result = Admins._execute_query(query, "login")

        if result:
            # Create session by updating last_login and session_expires_at
            def mutation(cursor, conn):
                expires_at = datetime.now() + timedelta(hours=Admins.SESSION_TIMEOUT_HOURS)
                cursor.execute(
                    """UPDATE admins 
                    SET last_login = CURRENT_TIMESTAMP, 
                        session_expires_at = %s 
                    WHERE telegram_id = %s""",
                    (expires_at, telegram_id)
                )

            return Admins._execute_mutation(mutation, "login")

        return False

    @staticmethod
    def is_authenticated(telegram_id: int) -> bool:
        """Check if user has a valid active session"""
        def query(cursor):
            cursor.execute(
                "SELECT session_expires_at FROM admins WHERE telegram_id = %s",
                (telegram_id,)
            )
            result = cursor.fetchone()

            if not result or result[0] is None:
                return False

            # Check if session has expired
            expires_at = result[0]

            if isinstance(expires_at, str):
                expires_at = datetime.fromisoformat(expires_at)

            return datetime.now() < expires_at

        result = Admins._execute_query(query, "is_authenticated")
        return result if result is not None else False

    @staticmethod
    def logout(telegram_id: int) -> bool:
        """Logout admin by clearing session"""
        def mutation(cursor, conn):
            cursor.execute(
                "UPDATE admins SET session_expires_at = NULL WHERE telegram_id = %s",
                (telegram_id,)
            )

        return Admins._execute_mutation(mutation, "logout")

    @staticmethod
    def get_session_info(telegram_id: int) -> dict:
        """Get session info for the admin"""
        def query(cursor):
            cursor.execute(
                "SELECT username, last_login, session_expires_at FROM admins WHERE telegram_id = %s",
                (telegram_id,)
            )
            result = cursor.fetchone()
            return result

        result = Admins._execute_query(query, "get_session_info")
        if not result:
            return None

        session_info = {
            'username': result[0],
            'last_login': result[1],
            'expires_at': result[2],
            'is_active': False
        }

        if result[2]:
            expires_at = result[2]

            if isinstance(expires_at, str):
                expires_at = datetime.fromisoformat(expires_at)

            session_info['is_active'] = datetime.now() < expires_at
            session_info['time_remaining'] = str(
                expires_at - datetime.now()).split('.')[0]

        return session_info


class Students(BaseRepository):
    table_name = "students"

    @classmethod
    def getAllStudents(cls):
        def query(cursor):
            cursor.execute(
                f"SELECT id,username FROM {cls.table_name}")
            result = cursor.fetchall()
            return result if result else None

        return cls._execute_query(query, "getAllStudents")

    @classmethod
    def getStudentById(cls, student_id):
        def query(cursor):
            cursor.execute(
                f"SELECT id,username, name, created_at, email, phone_number, last_seen, is_verfied, birthday FROM {cls.table_name} WHERE id = %s", (student_id,))
            result = cursor.fetchall()
            return result[0] if result else None

        return cls._execute_query(query, "getStudentById")

    @classmethod
    def createStudent(cls, name, email, phone_number, password, username, birthday):
        def mutation(cursor, conn):
            cursor.execute(
                f"INSERT INTO {cls.table_name} (name, email, phone_number, hashed_password, username, birthday) VALUES (%s, %s, %s, %s, %s, %s)",
                (name, email, phone_number, password,
                 username, birthday))
        return cls._execute_mutation(mutation, "createStudent")

    @classmethod
    def updateStudent(cls, student_id, **fields):
        if not fields:
            return False

        def mutation(cursor, conn):
            columns = [(f"{key} = %s" if key != 'password' else "hashed_password = %s")
                       for key in fields.keys()]
            values = list(fields.values()) + [student_id]
            cursor.execute(
                f"UPDATE {cls.table_name} SET {', '.join(columns)} WHERE id = %s",
                tuple(values)
            )

        return cls._execute_mutation(mutation, "updateStudent")

    @classmethod
    def deleteStudent(cls, student_id):
        def mutation(cursor, conn):
            cursor.execute(
                f"DELETE FROM {cls.table_name} WHERE id = %s", (student_id,))

        return cls._execute_mutation(mutation, "deleteStudent")


class Teachers(BaseRepository):
    table_name = "teachers"

    @classmethod
    def getAllTeachers(cls):
        def query(cursor):
            cursor.execute(
                f"SELECT id,username FROM {cls.table_name}")
            result = cursor.fetchall()
            return result if result else None

        return cls._execute_query(query, "getAllTeachers")

    @classmethod
    def getTeacherById(cls, teacher_id):
        def query(cursor):
            cursor.execute(
                f"SELECT id, username, name, created_at, email, phone_number, last_seen, is_verfied, birthday, about_me, job_title FROM {cls.table_name} WHERE id = %s", (teacher_id, ))
            result = cursor.fetchall()
            return result[0] if result else None

        return cls._execute_query(query, "getTeacherById")

    @classmethod
    def createTeacher(cls, name, email, phone_number, password, username, birthday, about_me, job_title):
        def mutation(cursor, conn):
            cursor.execute(
                f"INSERT INTO {cls.table_name} (name, email, phone_number, hashed_password, username, birthday, about_me, job_title) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)",
                (name, email, phone_number, password,
                 username, birthday, about_me, job_title))
        return cls._execute_mutation(mutation, "createTeacher")

    @classmethod
    def updateTeacher(cls, teacher_id, **fields):
        if not fields:
            return False

        def mutation(cursor, conn):
            columns = [(f"{key} = %s" if key != 'password' else "hashed_password = %s")
                       for key in fields.keys()]
            values = list(fields.values()) + [teacher_id]
            cursor.execute(
                f"UPDATE {cls.table_name} SET {', '.join(columns)} WHERE id = %s",
                tuple(values)
            )

        return cls._execute_mutation(mutation, "updateTeacher")

    @classmethod
    def deleteTeacher(cls, teacher_id):
        def mutation(cursor, conn):
            cursor.execute(
                f"DELETE FROM {cls.table_name} WHERE id = %s", (teacher_id,))

        return cls._execute_mutation(mutation, "deleteTeacher")


class Courses(BaseRepository):
    table_name = "courses"

    @classmethod
    def getAllCourses(cls):
        def query(cursor):
            cursor.execute(
                f"SELECT id, name FROM {cls.table_name}")
            result = cursor.fetchall()
            return result if result else None

        return cls._execute_query(query, "getAllCourses")

    @classmethod
    def getCourseById(cls, course_id):
        def query(cursor):
            cursor.execute(
                f"SELECT id, name, created_at, teacher_id, updated_at, description, difficulty, language FROM {cls.table_name} WHERE id = %s", (course_id, ))
            result = cursor.fetchall()
            return result[0] if result else None

        return cls._execute_query(query, "getCourseById")

    @classmethod
    def createCourse(cls, name, teacher_id, description, language, difficulty):
        def mutation(cursor, conn):
            cursor.execute(
                f"INSERT INTO {cls.table_name} (name, teacher_id, description, language, difficulty) VALUES (%s, %s, %s, %s, %s)",
                (name, teacher_id, description, language, difficulty))
        return cls._execute_mutation(mutation, "createCourse")

    @classmethod
    def updateCourse(cls, course_id, **fields):
        if not fields:
            return False

        def mutation(cursor, conn):
            columns = [f"{key} = %s" for key in fields.keys()]
            values = list(fields.values()) + [course_id]
            cursor.execute(
                f"UPDATE {cls.table_name} SET {', '.join(columns)} WHERE id = %s",
                tuple(values)
            )

        return cls._execute_mutation(mutation, "updateCourse")

    @classmethod
    def deleteCourse(cls, course_id):
        def mutation(cursor, conn):
            cursor.execute(
                f"DELETE FROM {cls.table_name} WHERE id = %s", (course_id,))

        return cls._execute_mutation(mutation, "deleteCourse")


class Tags(BaseRepository):
    table_name = "tags"

    @classmethod
    def getAllTags(cls):
        def query(cursor):
            cursor.execute(
                f"SELECT id, name, slug FROM {cls.table_name}")
            result = cursor.fetchall()
            return result if result else None

        return cls._execute_query(query, "getAllTags")

    @classmethod
    def getTagById(cls, tag_id):
        def query(cursor):
            cursor.execute(
                f"SELECT id, name, slug FROM {cls.table_name} WHERE id = %s", (tag_id,))
            result = cursor.fetchall()
            return result[0] if result else None

        return cls._execute_query(query, "getTagById")

    @classmethod
    def createTag(cls, name, slug):
        def mutation(cursor, conn):
            cursor.execute(
                f"INSERT INTO {cls.table_name} (name, slug) VALUES (%s, %s)", (name, slug))
        return cls._execute_mutation(mutation, "createTag")

    @classmethod
    def updateTag(cls, tag_id, **fields):
        if not fields:
            return False

        def mutation(cursor, conn):
            columns = [f"{key} = %s" for key in fields.keys()]
            values = list(fields.values()) + [tag_id]
            cursor.execute(
                f"UPDATE {cls.table_name} SET {', '.join(columns)} WHERE id = %s",
                tuple(values)
            )

        return cls._execute_mutation(mutation, "updateTag")

    @classmethod
    def deleteTag(cls, tag_id):
        def mutation(cursor, conn):
            cursor.execute(
                f"DELETE FROM {cls.table_name} WHERE id = %s", (tag_id,))

        return cls._execute_mutation(mutation, "deleteTag")


class Categories(BaseRepository):
    table_name = "categories"

    @classmethod
    def getAllCategories(cls):
        def query(cursor):
            cursor.execute(
                f"SELECT id, name, description, parent_id FROM {cls.table_name}")
            result = cursor.fetchall()
            return result if result else None

        return cls._execute_query(query, "getAllCategories")

    @classmethod
    def getCategorieById(cls, category_id):
        def query(cursor):
            cursor.execute(f"""
                SELECT c1.id, c1.name, c1.description,
                       COALESCE(c2.name, 'None') AS parent_category
                FROM {cls.table_name} c1
                LEFT JOIN {cls.table_name} c2 ON c2.id = c1.parent_id
                WHERE c1.id = %s
            """, (category_id,))
            result = cursor.fetchall()
            return result[0] if result else None

        return cls._execute_query(query, "getCategoryById")

    @classmethod
    def createCategory(cls, name, description, parent_id=None):
        def mutation(cursor, conn):
            cursor.execute(
                f"INSERT INTO {cls.table_name} (name, description, parent_id) VALUES (%s, %s, %s)", (name, description, parent_id))

        return cls._execute_mutation(mutation, "createCategory")

    @classmethod
    def updateCategory(cls, category_id, **fields):
        if not fields:
            return False

        def mutation(cursor, conn):
            columns = [f"{key} = %s" for key in fields.keys()]
            values = list(fields.values()) + [category_id]
            cursor.execute(
                f"UPDATE {cls.table_name} SET {', '.join(columns)} WHERE id = %s",
                tuple(values)
            )

        return cls._execute_mutation(mutation, "updateCategory")

    @classmethod
    def deleteCategory(cls, category_id):
        def mutation(cursor, conn):
            cursor.execute(
                f"DELETE FROM {cls.table_name} WHERE id = %s", (category_id,))

        return cls._execute_mutation(mutation, "deleteCategory")
