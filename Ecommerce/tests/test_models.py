import unittest

from model.user import User, AdminUser
from model.product import Product
from model.cart_item import CartItem
from model.order import Order
from model.order_item import OrderItem


class TestUserModel(unittest.TestCase):

    def test_user_defaults_to_customer_role(self):
        u = User("rajiv", "hash123", "rajiv@gmail.com")
        self.assertEqual(u.role, "customer")
        self.assertIsNone(u.user_id)

    def test_user_str_format(self):
        u = User("rajiv", "hash123", "rajiv@gmail.com", user_id=5)
        self.assertEqual(str(u), "[CUSTOMER] rajiv (ID: 5)")

    def test_adminuser_forces_admin_role(self):
        a = AdminUser("admin", "hash456", "admin@gmail.com", user_id=2)
        self.assertEqual(a.role, "admin")

    def test_adminuser_is_instance_of_user(self):
        a = AdminUser("admin", "hash456", "admin@gmail.com")
        self.assertIsInstance(a, User)

    def test_plain_user_is_not_adminuser(self):
        u = User("rajiv", "hash123", "rajiv@gmail.com")
        self.assertNotIsInstance(u, AdminUser)


class TestProductModel(unittest.TestCase):

    def test_converts_price_and_stock_to_numbers(self):
        p = Product("Keyboard", "Mechanical", "1500", "10", "Electronics", 1)
        self.assertEqual(p.price, 1500.0)
        self.assertIsInstance(p.price, float)
        self.assertEqual(p.stock, 10)
        self.assertIsInstance(p.stock, int)

    def test_str_includes_price_formatted_to_two_decimals(self):
        p = Product("Mouse", "Wireless", 450, 5, "Electronics", 7)
        self.assertIn("₹450.00", str(p))


class TestCartItemModel(unittest.TestCase):

    def test_subtotal_computes_quantity_times_price(self):
        item = CartItem(cart_id=1, user_id=1, product_id=1, quantity=3, price=100)
        self.assertEqual(item.subtotal, 300)

    def test_subtotal_is_zero_when_price_missing(self):
        item = CartItem(cart_id=1, user_id=1, product_id=1, quantity=3)
        self.assertEqual(item.subtotal, 0)


class TestOrderModel(unittest.TestCase):

    def test_defaults_to_pending_status(self):
        o = Order(user_id=1, total_amount=500)
        self.assertEqual(o.status, "pending")


class TestOrderItemModel(unittest.TestCase):

    def test_subtotal_frozen_at_creation(self):
        item = OrderItem(order_id=1, product_id=1, quantity=2, unit_price=650)
        self.assertEqual(item.subtotal, 1300)


if __name__ == "__main__":
    unittest.main()