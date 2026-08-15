from config.database import get_connection
from mysql.connector import Error


class CartDAO:

    def get_cart_item(self, user_id, product_id):
        """Check if product already exists in user's cart."""
        conn = None
        cursor = None

        try:
            conn = get_connection()
            cursor = conn.cursor(dictionary=True)

            cursor.execute(
                "SELECT * FROM cart WHERE user_id = %s AND product_id = %s",
                (user_id, product_id)
            )

            return cursor.fetchone()

        except Error as e:
            raise RuntimeError(
                f"[CartDAO.get_cart_item] DB error: {e}"
            )

        finally:
            if cursor:
                cursor.close()

            if conn and conn.is_connected():
                conn.close()


    def insert_item(self, user_id, product_id, quantity):
        conn = None
        cursor = None

        try:
            conn = get_connection()
            cursor = conn.cursor()

            cursor.execute(
                """
                INSERT INTO cart
                (user_id, product_id, quantity)
                VALUES (%s, %s, %s)
                """,
                (user_id, product_id, quantity)
            )

            conn.commit()

        except Error as e:
            if conn:
                conn.rollback()

            raise RuntimeError(
                f"[CartDAO.insert_item] DB error: {e}"
            )

        finally:
            if cursor:
                cursor.close()

            if conn and conn.is_connected():
                conn.close()


    def update_quantity(self, user_id, product_id, quantity):
        conn = None
        cursor = None

        try:
            conn = get_connection()
            cursor = conn.cursor()

            cursor.execute(
                """
                UPDATE cart
                SET quantity = %s
                WHERE user_id = %s AND product_id = %s
                """,
                (quantity, user_id, product_id)
            )

            conn.commit()

        except Error as e:
            if conn:
                conn.rollback()

            raise RuntimeError(
                f"[CartDAO.update_quantity] DB error: {e}"
            )

        finally:
            if cursor:
                cursor.close()

            if conn and conn.is_connected():
                conn.close()


    def get_cart_with_details(self, user_id):
        """Get cart items with product name, price and subtotal."""
        conn = None
        cursor = None

        try:
            conn = get_connection()
            cursor = conn.cursor(dictionary=True)

            query = """
                SELECT
                    c.cart_id,
                    c.product_id,
                    p.name AS product_name,
                    c.quantity,
                    p.price,
                    (c.quantity * p.price) AS subtotal
                FROM cart c
                JOIN products p
                    ON c.product_id = p.product_id
                WHERE c.user_id = %s
            """

            cursor.execute(query, (user_id,))

            return cursor.fetchall()

        except Error as e:
            raise RuntimeError(
                f"[CartDAO.get_cart_with_details] DB error: {e}"
            )

        finally:
            if cursor:
                cursor.close()

            if conn and conn.is_connected():
                conn.close()


    def get_cart_total(self, user_id):
        conn = None
        cursor = None

        try:
            conn = get_connection()
            cursor = conn.cursor()

            cursor.execute(
                """
                SELECT SUM(c.quantity * p.price)
                FROM cart c
                JOIN products p
                    ON c.product_id = p.product_id
                WHERE c.user_id = %s
                """,
                (user_id,)
            )

            result = cursor.fetchone()[0]

            return float(result) if result else 0.0

        except Error as e:
            raise RuntimeError(
                f"[CartDAO.get_cart_total] DB error: {e}"
            )

        finally:
            if cursor:
                cursor.close()

            if conn and conn.is_connected():
                conn.close()


    def remove_item(self, user_id, product_id):
        conn = None
        cursor = None

        try:
            conn = get_connection()
            cursor = conn.cursor()

            cursor.execute(
                """
                DELETE FROM cart
                WHERE user_id = %s AND product_id = %s
                """,
                (user_id, product_id)
            )

            conn.commit()

        except Error as e:
            if conn:
                conn.rollback()

            raise RuntimeError(
                f"[CartDAO.remove_item] DB error: {e}"
            )

        finally:
            if cursor:
                cursor.close()

            if conn and conn.is_connected():
                conn.close()


    def clear_cart(self, user_id):
        conn = None
        cursor = None

        try:
            conn = get_connection()
            cursor = conn.cursor()

            cursor.execute(
                "DELETE FROM cart WHERE user_id = %s",
                (user_id,)
            )

            conn.commit()

        except Error as e:
            if conn:
                conn.rollback()

            raise RuntimeError(
                f"[CartDAO.clear_cart] DB error: {e}"
            )

        finally:
            if cursor:
                cursor.close()

            if conn and conn.is_connected():
                conn.close()