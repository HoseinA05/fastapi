import logging
import database.connection as connection

logger = logging.getLogger(__name__)


class testModel:
    def getAllUsers():
        conn = None
        try:
            conn = connection.get_db_connection()
            if not conn:
                return None
            
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM students");
            result = cursor.fetchall()
            cursor.close()

            return result if result else None
        except Exception as e:
            logger.error(f"Database query error: {e}")
            return None
        finally:
            if conn:
                connection.release_db_connection(conn)