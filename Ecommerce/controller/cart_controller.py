from service.cart_service import CartService


class CartController:

    def __init__(self, current_user):
        self.current_user = current_user
        self.cart_service = CartService()


    def add_to_cart(self):
        try:
            product_id = int(input("Product ID to add: "))
            quantity = int(input("Quantity: "))

            self.cart_service.add_to_cart(
                self.current_user.user_id,
                product_id,
                quantity
            )

            print("✅ Added to cart.")

        except ValueError as e:
            print(f"❌ Invalid input: {e}")

        except RuntimeError as e:
            print(f"❌ System error: {e}")

        except Exception as e:
            print(f"❌ Unexpected error: {e}")


    def view_cart(self):
        try:
            items = self.cart_service.view_cart(
                self.current_user.user_id
            )

            if not items:
                print("🛒 Your cart is empty.")
                return

            print(
                f"\n{'Product':<25} "
                f"{'Qty':>5} "
                f"{'Price':>10} "
                f"{'Subtotal':>10}"
            )

            print("-" * 55)

            for item in items:
                print(
                    f"{item['product_name']:<25} "
                    f"{item['quantity']:>5} "
                    f"₹{float(item['price']):>9.2f} "
                    f"₹{float(item['subtotal']):>9.2f}"
                )

            total = self.cart_service.get_total(
                self.current_user.user_id
            )

            print(f"\n{'TOTAL':>43} ₹{total:>9.2f}")

        except RuntimeError as e:
            print(f"❌ Could not load cart: {e}")

        except Exception as e:
            print(f"❌ Unexpected error: {e}")


    def update_quantity(self):
        try:
            product_id = int(input("Product ID: "))
            quantity = int(input("New quantity: "))

            self.cart_service.update_item_quantity(
                self.current_user.user_id,
                product_id,
                quantity
            )

            print("✅ Cart updated.")

        except ValueError as e:
            print(f"❌ Invalid input: {e}")

        except RuntimeError as e:
            print(f"❌ System error: {e}")

        except Exception as e:
            print(f"❌ Unexpected error: {e}")


    def remove_from_cart(self):
        try:
            product_id = int(
                input("Product ID to remove: ")
            )

            self.cart_service.remove_from_cart(
                self.current_user.user_id,
                product_id
            )

            print("✅ Item removed from cart.")

        except ValueError:
            print(
                "❌ Please enter a valid product ID (number)."
            )

        except RuntimeError as e:
            print(f"❌ System error: {e}")

        except Exception as e:
            print(f"❌ Unexpected error: {e}")