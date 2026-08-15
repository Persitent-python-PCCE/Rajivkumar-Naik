from config.database import get_connection
from mysql.connector import Error


class OrderDAO:

    def place_order(self, user_id):
        """
        Full checkout inside ONE transaction:
        cart -> validate stock -> orders -> order_items
        -> reduce stock -> clear cart.
        Returns (order_id, total_amount).
        """
        conn = None
        cursor = None

        try:
            conn = get_connection()
            conn.autocommit = False
            cursor = conn.cursor(dictionary=True)

            cursor.execute(
                """
                SELECT
                    c.product_id,
                    c.quantity,
                    p.name,
                    p.price,
                    p.stock
                FROM cart c
                JOIN products p
                    ON c.product_id = p.product_id
                WHERE c.user_id = %s
                FOR UPDATE
                """,
                (user_id,)
            )

            items = cursor.fetchall()

            if not items:
                raise ValueError("Your cart is empty.")

            total = 0.0

            for item in items:
                if item['quantity'] > item['stock']:
                    raise ValueError(
                        f"'{item['name']}' has only "
                        f"{item['stock']} unit(s) in stock."
                    )

                total += float(item['price']) * item['quantity']

            cursor.execute(
                """
                INSERT INTO orders (user_id, total_amount, status)
                VALUES (%s, %s, %s)
                """,
                (user_id, total, 'confirmed')
            )

            order_id = cursor.lastrowid

            for item in items:
                subtotal = float(item['price']) * item['quantity']

                cursor.execute(
                    """
                    INSERT INTO order_items
                    (order_id, product_id, quantity, unit_price, subtotal)
                    VALUES (%s, %s, %s, %s, %s)
                    """,
                    (
                        order_id,
                        item['product_id'],
                        item['quantity'],
                        item['price'],
                        subtotal
                    )
                )

                cursor.execute(
                    """
                    UPDATE products
                    SET stock = stock - %s
                    WHERE product_id = %s AND stock >= %s
                    """,
                    (item['quantity'], item['product_id'], item['quantity'])
                )

                if cursor.rowcount == 0:
                    raise ValueError(
                        f"Stock for '{item['name']}' just changed. "
                        f"Please review your cart."
                    )

            cursor.execute(
                "DELETE FROM cart WHERE user_id = %s",
                (user_id,)
            )

            conn.commit()

            return order_id, total

        except ValueError:
            if conn:
                conn.rollback()
            raise

        except Error as e:
            if conn:
                conn.rollback()

            raise RuntimeError(
                f"[OrderDAO.place_order] DB error: {e}"
            )

        except Exception as e:
            if conn:
                conn.rollback()

            raise RuntimeError(
                f"[OrderDAO.place_order] Unexpected error: {e}"
            )

        finally:
            if cursor:
                cursor.close()

            if conn and conn.is_connected():
                conn.close()


    def get_orders_by_user(self, user_id):
        conn = None
        cursor = None

        try:
            conn = get_connection()
            cursor = conn.cursor(dictionary=True)

            cursor.execute(
                """
                SELECT * FROM orders
                WHERE user_id = %s
                ORDER BY ordered_at DESC
                """,
                (user_id,)
            )

            return cursor.fetchall()

        except Error as e:
            raise RuntimeError(
                f"[OrderDAO.get_orders_by_user] DB error: {e}"
            )

        finally:
            if cursor:
                cursor.close()

            if conn and conn.is_connected():
                conn.close()


    def get_order_by_id(self, order_id):
        conn = None
        cursor = None

        try:
            conn = get_connection()
            cursor = conn.cursor(dictionary=True)

            cursor.execute(
                "SELECT * FROM orders WHERE order_id = %s",
                (order_id,)
            )

            return cursor.fetchone()

        except Error as e:
            raise RuntimeError(
                f"[OrderDAO.get_order_by_id] DB error: {e}"
            )

        finally:
            if cursor:
                cursor.close()

            if conn and conn.is_connected():
                conn.close()


    def get_all_orders(self):
        """Admin only — all orders across all users."""
        conn = None
        cursor = None

        try:
            conn = get_connection()
            cursor = conn.cursor(dictionary=True)

            cursor.execute(
                "SELECT * FROM orders ORDER BY ordered_at DESC"
            )

            return cursor.fetchall()

        except Error as e:
            raise RuntimeError(
                f"[OrderDAO.get_all_orders] DB error: {e}"
            )

        finally:
            if cursor:
                cursor.close()

            if conn and conn.is_connected():
                conn.close()


    def get_order_items(self, order_id):
        conn = None
        cursor = None

        try:
            conn = get_connection()
            cursor = conn.cursor(dictionary=True)

            cursor.execute(
                """
                SELECT
                    oi.product_id,
                    p.name AS product_name,
                    oi.quantity,
                    oi.unit_price,
                    oi.subtotal
                FROM order_items oi
                JOIN products p
                    ON oi.product_id = p.product_id
                WHERE oi.order_id = %s
                """,
                (order_id,)
            )

            return cursor.fetchall()

        except Error as e:
            raise RuntimeError(
                f"[OrderDAO.get_order_items] DB error: {e}"
            )

        finally:
            if cursor:
                cursor.close()

            if conn and conn.is_connected():
                conn.close()


    def cancel_order(self, order_id, user_id):
        """Restore stock and mark the order cancelled — one transaction."""
        conn = None
        cursor = None

        try:
            conn = get_connection()
            conn.autocommit = False
            cursor = conn.cursor(dictionary=True)

            cursor.execute(
                "SELECT * FROM orders WHERE order_id = %s FOR UPDATE",
                (order_id,)
            )

            order = cursor.fetchone()

            if not order:
                raise ValueError("Order not found.")

            if order['user_id'] != user_id:
                raise PermissionError(
                    "This order does not belong to you."
                )

            if order['status'] == 'cancelled':
                raise ValueError("Order is already cancelled.")

            cursor.execute(
                """
                SELECT product_id, quantity
                FROM order_items
                WHERE order_id = %s
                """,
                (order_id,)
            )

            for item in cursor.fetchall():
                cursor.execute(
                    """
                    UPDATE products
                    SET stock = stock + %s
                    WHERE product_id = %s
                    """,
                    (item['quantity'], item['product_id'])
                )

            cursor.execute(
                "UPDATE orders SET status = 'cancelled' WHERE order_id = %s",
                (order_id,)
            )

            conn.commit()

        except (ValueError, PermissionError):
            if conn:
                conn.rollback()
            raise

        except Error as e:
            if conn:
                conn.rollback()

            raise RuntimeError(
                f"[OrderDAO.cancel_order] DB error: {e}"
            )

        except Exception as e:
            if conn:
                conn.rollback()

            raise RuntimeError(
                f"[OrderDAO.cancel_order] Unexpected error: {e}"
            )

        finally:
            if cursor:
                cursor.close()

            if conn and conn.is_connected():
                conn.close()