import os
import logging
import psycopg2
from psycopg2 import pool

logger = logging.getLogger(__name__)

# Connection pool for reusing connections (important for serverless!)
_connection_pool = None

def get_connection_pool():
    """Create a connection pool"""
    global _connection_pool
    if _connection_pool is None:
        try:
            # --- Production settings
            # DATABASE_URL = os.environ.get("DATABASE_URL")
            # _connection_pool = psycopg2.pool.SimpleConnectionPool(1, 5, DATABASE_URL);
            
            # --- Development settings
            dev_url = "postgresql://postgres:123@localhost:5432/OLP"
            _connection_pool = psycopg2.pool.SimpleConnectionPool(1, 5, dev_url);
            
            logger.info("Database connection pool created")
        except Exception as e:
            logger.error(f"Failed to create connection pool: {e}")
            return None
    return _connection_pool

def get_db_connection():
    """Get a connection from the pool"""
    try:
        pool = get_connection_pool()
        if pool:
            conn = pool.getconn()
            return conn
        return None
    except Exception as e:
        logger.error(f"Database connection error: {e}")
        return None

def release_db_connection(conn):
    """Return connection to the pool"""
    try:
        pool = get_connection_pool()
        if pool and conn:
            pool.putconn(conn)
    except Exception as e:
        logger.error(f"Error releasing connection: {e}")