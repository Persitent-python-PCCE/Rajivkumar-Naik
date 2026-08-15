from config.database import get_connection
from mysql.connector import Error


class UserDAO:
 def insert_user(self, user):
    conn = None
    cursor = None

    try:
        conn = get_connection()
        cursor = conn.cursor()

        q = """
            INSERT INTO users
            (username, password, email, role)
            VALUES (%s, %s, %s, %s)
        """

        cursor.execute(
            q,
            (user.username, user.password, user.email, user.role)
        )

        conn.commit()

        return cursor.lastrowid

    except Error as e:
        if conn:
            conn.rollback()

        if e.errno == 1062:
            raise ValueError("Username or email already exists.")

        raise RuntimeError(f"[UserDAO.insert_user] DB error: {e}")

    except Exception as e:
        raise RuntimeError(
            f"[UserDAO.insert_user] Unexpected error: {e}"
        )

    finally:
        if cursor:
            cursor.close()

        if conn and conn.is_connected():
            conn.close() 


 def find_by_username(self, username):
        conn = None
        cursor = None

        try:
            conn = get_connection()
            cursor = conn.cursor(dictionary=True)

            cursor.execute(
                "SELECT * FROM users WHERE username = %s",
                (username,)
            )

            return cursor.fetchone()

        except Error as e:
            raise RuntimeError(
                f"[UserDAO.find_by_username] DB error: {e}"
            )

        except Exception as e:
            raise RuntimeError(
                f"[UserDAO.find_by_username] Unexpected error: {e}"
            )

        finally:
            if cursor:
                cursor.close()

            if conn and conn.is_connected():
                conn.close()   


 def find_by_id(self, user_id):
        conn = None
        cursor = None

        try:
            conn = get_connection()
            cursor = conn.cursor(dictionary=True)

            cursor.execute(
                "SELECT * FROM users WHERE user_id = %s",
                (user_id,)
            )

            return cursor.fetchone()

        except Error as e:
            raise RuntimeError(
                f"[UserDAO.find_by_id] DB error: {e}"
            )

        except Exception as e:
            raise RuntimeError(
                f"[UserDAO.find_by_id] Unexpected error: {e}"
            )

        finally:
            if cursor:
                cursor.close()

            if conn and conn.is_connected():
                conn.close()  

                              
 def update_password(self, user_id, new_hash):
        conn = None
        cursor = None

        try:
            conn = get_connection()
            cursor = conn.cursor()

            cursor.execute(
                "UPDATE users SET password = %s WHERE user_id = %s",
                (new_hash, user_id)
            )

            conn.commit()

        except Error as e:
            if conn:
                conn.rollback()

            raise RuntimeError(
                f"[UserDAO.update_password] DB error: {e}"
            )

        except Exception as e:
            raise RuntimeError(
                f"[UserDAO.update_password] Unexpected error: {e}"
            )

        finally:
            if cursor:
                cursor.close()

            if conn and conn.is_connected():
                conn.close()                


 def delete_user(self, user_id):
        conn = None
        cursor = None

        try:
            conn = get_connection()
            cursor = conn.cursor()

            cursor.execute(
                "DELETE FROM users WHERE user_id = %s",
                (user_id,)
            )

            conn.commit()

        except Error as e:
            if conn:
                conn.rollback()

            raise RuntimeError(
                f"[UserDAO.delete_user] DB error: {e}"
            )

        except Exception as e:
            raise RuntimeError(
                f"[UserDAO.delete_user] Unexpected error: {e}"
            )

        finally:
            if cursor:
                cursor.close()

            if conn and conn.is_connected():
                conn.close()               