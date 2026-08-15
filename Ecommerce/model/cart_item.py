class CartItem:
    def __init__(self, cart_id, user_id, product_id, quantity,
                 product_name=None, price=None):
        self.cart_id = cart_id
        self.user_id = user_id
        self.product_id = product_id
        self.quantity = quantity
        self.product_name = product_name
        self.price = price

    @property
    def subtotal(self):
        return self.quantity * self.price if self.price else 0