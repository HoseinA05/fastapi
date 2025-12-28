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
            cursor.execute("SELECT id,name FROM students");
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
            cursor.execute("SELECT id,username, created_at, email, phone_number, last_seen, is_verfied, birthday FROM students WHERE id = %s", (student_id,))
            result = cursor.fetchall()
            cursor.close()

            return result[0] if result else None
        except Exception as e:
            logger.error(f"Database query error in getStudentById: {e}")
            return None
        finally:
            if conn:
                connection.release_db_connection(conn)