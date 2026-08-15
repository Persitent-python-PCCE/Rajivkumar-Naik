from service.order_service import OrderService
from service.file_service import FileService


class OrderController:

    def __init__(self, current_user):
        self.current_user = current_user
        self.order_service = OrderService()
        self.file_service = FileService()


    def place_order(self):
        try:
            order_id, total = self.order_service.place_order(
                self.current_user.user_id
            )

            print(f"\n Order placed successfully!")
            print(f"Order ID: {order_id}")
            print(f"Total: ₹{total:.2f}")
            print("Your cart has been cleared.")

            self.file_service.write_log(
                self.current_user.user_id,
                'ORDER_PLACED',
                f"order_id={order_id}, total={total:.2f}"
            )

            self.file_service.backup_orders_json()

        except ValueError as e:
            print(f" Could not place order: {e}")

        except RuntimeError as e:
            print(f" System error: {e}")

        except Exception as e:
            print(f" Unexpected error: {e}")


    def view_order_history(self):
        try:
            orders = self.order_service.get_order_history(
                self.current_user.user_id
            )

            if not orders:
                print("You have no orders yet.")
                return

            print(
                f"\n{'Order ID':<10} "
                f"{'Total':>12} "
                f"{'Status':<12} "
                f"{'Ordered At'}"
            )
            print("-" * 55)

            for order in orders:
                print(
                    f"{order['order_id']:<10} "
                    f"₹{float(order['total_amount']):>10.2f} "
                    f"{order['status']:<12} "
                    f"{order['ordered_at']}"
                )

        except RuntimeError as e:
            print(f" Could not load orders: {e}")

        except Exception as e:
            print(f" Unexpected error: {e}")


    def view_order_detail(self):
        try:
            order_id = int(input("Enter order ID: "))

            order, items = self.order_service.get_order_detail(
                order_id,
                self.current_user
            )

            print(f"\nOrder #{order['order_id']}")
            print(f"Status: {order['status']}")
            print(f"Ordered At: {order['ordered_at']}")
            print(
                f"\n{'Product':<25} "
                f"{'Qty':>5} "
                f"{'Unit Price':>12} "
                f"{'Subtotal':>10}"
            )
            print("-" * 58)

            for item in items:
                print(
                    f"{item['product_name']:<25} "
                    f"{item['quantity']:>5} "
                    f"₹{float(item['unit_price']):>10.2f} "
                    f"₹{float(item['subtotal']):>9.2f}"
                )

            print(f"\n{'TOTAL':>46} ₹{float(order['total_amount']):>9.2f}")

        except ValueError as e:
            print(f" {e}")

        except PermissionError as e:
            print(f" {e}")

        except RuntimeError as e:
            print(f" System error: {e}")

        except Exception as e:
            print(f" Unexpected error: {e}")


    def cancel_order(self):
        try:
            order_id = int(input("Enter order ID to cancel: "))

            self.order_service.cancel_order(
                order_id,
                self.current_user.user_id
            )

            print(" Order cancelled and stock restored.")

            self.file_service.write_log(
                self.current_user.user_id,
                'ORDER_CANCELLED',
                f"order_id={order_id}"
            )

        except ValueError as e:
            print(f" {e}")

        except PermissionError as e:
            print(f" {e}")

        except RuntimeError as e:
            print(f" System error: {e}")

        except Exception as e:
            print(f" Unexpected error: {e}")