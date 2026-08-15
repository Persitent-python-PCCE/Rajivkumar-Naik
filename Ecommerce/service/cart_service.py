from dao.cart_dao import CartDAO
from dao.product_dao import ProductDAO


class CartService:

    def __init__(self):
        self.cart_dao = CartDAO()
        self.product_dao = ProductDAO()


    def add_to_cart(self, user_id, product_id, quantity):
        try:
            if quantity <= 0:
                raise ValueError("Quantity must be at least 1.")

            product = self.product_dao.get_by_id(product_id)

            if not product:
                raise ValueError("Product not found.")

            if product.stock < quantity:
                raise ValueError(
                    f"Only {product.stock} unit(s) in stock."
                )

            existing = self.cart_dao.get_cart_item(
                user_id,
                product_id
            )

            if existing:
                new_qty = existing['quantity'] + quantity

                if new_qty > product.stock:
                    raise ValueError(
                        "Total quantity exceeds available stock."
                    )

                self.cart_dao.update_quantity(
                    user_id,
                    product_id,
                    new_qty
                )

            else:
                self.cart_dao.insert_item(
                    user_id,
                    product_id,
                    quantity
                )

        except ValueError:
            raise

        except RuntimeError:
            raise

        except Exception as e:
            raise RuntimeError(
                f"[CartService.add_to_cart] Unexpected error: {e}"
            )


    def view_cart(self, user_id):
        try:
            return self.cart_dao.get_cart_with_details(user_id)

        except RuntimeError:
            raise

        except Exception as e:
            raise RuntimeError(
                f"[CartService.view_cart] Unexpected error: {e}"
            )


    def get_total(self, user_id):
        try:
            return self.cart_dao.get_cart_total(user_id)

        except RuntimeError:
            raise

        except Exception as e:
            raise RuntimeError(
                f"[CartService.get_total] Unexpected error: {e}"
            )


    def update_item_quantity(self, user_id, product_id, quantity):
        try:
            if quantity <= 0:
                raise ValueError(
                    "Quantity must be at least 1."
                )

            product = self.product_dao.get_by_id(product_id)

            if not product:
                raise ValueError("Product not found.")

            if quantity > product.stock:
                raise ValueError(
                    f"Requested quantity exceeds stock "
                    f"({product.stock} available)."
                )

            self.cart_dao.update_quantity(
                user_id,
                product_id,
                quantity
            )

        except ValueError:
            raise

        except RuntimeError:
            raise

        except Exception as e:
            raise RuntimeError(
                f"[CartService.update_item_quantity] Unexpected error: {e}"
            )


    def remove_from_cart(self, user_id, product_id):
        try:
            self.cart_dao.remove_item(
                user_id,
                product_id
            )

        except RuntimeError:
            raise

        except Exception as e:
            raise RuntimeError(
                f"[CartService.remove_from_cart] Unexpected error: {e}"
            )


    def clear_cart(self, user_id):
        try:
            self.cart_dao.clear_cart(user_id)

        except RuntimeError:
            raise

        except Exception as e:
            raise RuntimeError(
                f"[CartService.clear_cart] Unexpected error: {e}"
            )