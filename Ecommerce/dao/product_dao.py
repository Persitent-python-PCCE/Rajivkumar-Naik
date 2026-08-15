from config.database import get_connection
from mysql.connector import Error
from model.product import Product

class ProductDAO:
  def insert(self,product):
    conn = None
    cursor = None
    try:
        conn=get_connection()
        cursor=conn.cursor()

        q="""
          INSERT INTO products (name,description,price,stock,category)VALUES(%s,%s,%s,%s,%s)
          """
        values=(product.name,product.description,product.price,product.stock,product.category)

        cursor.execute(q,values)
        conn.commit()
        return cursor.lastrowid

    except Error as e:
        if conn:
            conn.rollback()

        if e.errno==1062:
            raise ValueError(
                "Product with that name exists."
            )    
        raise RuntimeError(
            f"[ProductDAO.insert] DB error:{e}"
        )

    finally:
        if cursor:
            cursor.close()

        if conn and conn.is_connected():
            conn.close()    


  def get_all(self):
        conn = None
        cursor = None

        try:
            conn = get_connection()
            cursor = conn.cursor(dictionary=True)

            cursor.execute(
                "SELECT * FROM products ORDER BY product_id"
            )

            rows = cursor.fetchall()
            return [
                Product(
                    row['name'],
                    row['description'],
                    row['price'],
                    row['stock'],
                    row['category'],
                    row['product_id'],
                    row['created_at']
                )
                for row in rows
            ]
            

        except Error as e:
            raise RuntimeError(
                f"[ProductDAO.get_all] DB error: {e}"
            )

        except Exception as e:
            raise RuntimeError(
                f"[ProductDAO.get_all] Unexpected error: {e}"
            )

        finally:
            if cursor:
                cursor.close()

            if conn and conn.is_connected():
                conn.close()


  def _build_filters(self, category, min_price, max_price, search):
        """Shared WHERE-clause builder used by get_paginated and count_products."""
        conditions = ["1=1"]
        params = []

        if category:
            conditions.append("category LIKE %s")
            params.append(f"%{category}%")

        if min_price is not None:
            conditions.append("price >= %s")
            params.append(min_price)

        if max_price is not None:
            conditions.append("price <= %s")
            params.append(max_price)

        if search:
            conditions.append("name LIKE %s")
            params.append(f"%{search}%")

        return " AND ".join(conditions), params


  def get_paginated(self, page=1, page_size=10, category=None,
                     min_price=None, max_price=None, search=None):
        conn = None
        cursor = None

        try:
            conn = get_connection()
            cursor = conn.cursor(dictionary=True)

            where_clause, params = self._build_filters(
                category, min_price, max_price, search
            )

            offset = (page - 1) * page_size

            query = f"""
                SELECT * FROM products
                WHERE {where_clause}
                ORDER BY product_id
                LIMIT %s OFFSET %s
            """

            cursor.execute(query, params + [page_size, offset])

            rows = cursor.fetchall()
            return [
                Product(
                    row['name'],
                    row['description'],
                    row['price'],
                    row['stock'],
                    row['category'],
                    row['product_id'],
                    row['created_at']
                )
                for row in rows
            ]

        except Error as e:
            raise RuntimeError(
                f"[ProductDAO.get_paginated] DB error: {e}"
            )

        except Exception as e:
            raise RuntimeError(
                f"[ProductDAO.get_paginated] Unexpected error: {e}"
            )

        finally:
            if cursor:
                cursor.close()

            if conn and conn.is_connected():
                conn.close()


  def count_products(self, category=None, min_price=None,
                      max_price=None, search=None):
        conn = None
        cursor = None

        try:
            conn = get_connection()
            cursor = conn.cursor()

            where_clause, params = self._build_filters(
                category, min_price, max_price, search
            )

            query = f"SELECT COUNT(*) FROM products WHERE {where_clause}"

            cursor.execute(query, params)

            return cursor.fetchone()[0]

        except Error as e:
            raise RuntimeError(
                f"[ProductDAO.count_products] DB error: {e}"
            )

        except Exception as e:
            raise RuntimeError(
                f"[ProductDAO.count_products] Unexpected error: {e}"
            )

        finally:
            if cursor:
                cursor.close()

            if conn and conn.is_connected():
                conn.close()


  def get_by_id(self, product_id):
        conn = None
        cursor = None

        try:
            conn = get_connection()
            cursor = conn.cursor(dictionary=True)

            cursor.execute(
                "SELECT * FROM products WHERE product_id = %s",
                (product_id,)
            )

            row = cursor.fetchone()
            if not row:
                return None

            return Product(
                row['name'],
                row['description'],
                row['price'],
                row['stock'],
                row['category'],
                row['product_id'],
                row['created_at']
            )

        except Error as e:
            raise RuntimeError(
                f"[ProductDAO.get_by_id] DB error: {e}"
            )

        except Exception as e:
            raise RuntimeError(
                f"[ProductDAO.get_by_id] Unexpected error: {e}"
            )

        finally:
            if cursor:
                cursor.close()

            if conn and conn.is_connected():
                conn.close()


  def update(self, product):
        conn = None
        cursor = None

        try:
            conn = get_connection()
            cursor = conn.cursor()

            q = """
                UPDATE products
                SET name = %s,
                    description = %s,
                    price = %s,
                    stock = %s,
                    category = %s
                WHERE product_id = %s
            """

            cursor.execute(
                q,
                (
                    product.name,
                    product.description,
                    product.price,
                    product.stock,
                    product.category,
                    product.product_id
                )
            )

            if cursor.rowcount == 0:
                raise ValueError("Product not found.")

            conn.commit()

        except Error as e:
            if conn:
                conn.rollback()

            raise RuntimeError(
                f"[ProductDAO.update] DB error: {e}"
            )

        except ValueError:
            raise

        except Exception as e:
            raise RuntimeError(
                f"[ProductDAO.update] Unexpected error: {e}"
            )

        finally:
            if cursor:
                cursor.close()

            if conn and conn.is_connected():
                conn.close()              


  def delete(self, product_id):
        conn = None
        cursor = None

        try:
            conn = get_connection()
            cursor = conn.cursor()

            cursor.execute(
                "DELETE FROM products WHERE product_id = %s",
                (product_id,)
            )

            if cursor.rowcount == 0:
                raise ValueError("Product not found.")

            conn.commit()

        except Error as e:
            if conn:
                conn.rollback()

            raise RuntimeError(
                f"[ProductDAO.delete] DB error: {e}"
            )

        except ValueError:
            raise

        except Exception as e:
            raise RuntimeError(
                f"[ProductDAO.delete] Unexpected error: {e}"
            )

        finally:
            if cursor:
                cursor.close()

            if conn and conn.is_connected():
                conn.close()