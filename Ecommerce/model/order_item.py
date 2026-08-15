class OrderItem:
    def __init__(self, order_id, product_id, quantity, unit_price, item_id=None):
        self.item_id = item_id
        self.order_id = order_id
        self.product_id = product_id
        self.quantity = quantity
        self.unit_price = unit_price
        self.subtotal = quantity * unit_price