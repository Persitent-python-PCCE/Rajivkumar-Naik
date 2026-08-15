from dao.order_dao import OrderDAO


class OrderService:

    def __init__(self):
        self.order_dao = OrderDAO()


    def place_order(self, user_id):
        try:
            return self.order_dao.place_order(user_id)

        except ValueError:
            raise

        except RuntimeError:
            raise

        except Exception as e:
            raise RuntimeError(
                f"[OrderService.place_order] Unexpected error: {e}"
            )


    def get_order_history(self, user_id):
        try:
            return self.order_dao.get_orders_by_user(user_id)

        except RuntimeError:
            raise

        except Exception as e:
            raise RuntimeError(
                f"[OrderService.get_order_history] Unexpected error: {e}"
            )


    def get_order_detail(self, order_id, requester):
        try:
            order = self.order_dao.get_order_by_id(order_id)

            if not order:
                raise ValueError("Order not found.")

            is_owner = order['user_id'] == requester.user_id
            is_admin = requester.role == 'admin'

            if not is_owner and not is_admin:
                raise PermissionError("This order does not belong to you.")

            items = self.order_dao.get_order_items(order_id)

            return order, items

        except (ValueError, PermissionError):
            raise

        except RuntimeError:
            raise

        except Exception as e:
            raise RuntimeError(
                f"[OrderService.get_order_detail] Unexpected error: {e}"
            )


    def cancel_order(self, order_id, user_id):
        try:
            self.order_dao.cancel_order(order_id, user_id)

        except (ValueError, PermissionError):
            raise

        except RuntimeError:
            raise

        except Exception as e:
            raise RuntimeError(
                f"[OrderService.cancel_order] Unexpected error: {e}"
            )