class Order:
    def __init__(self, user_id, total_amount, status='pending',
                 order_id=None, ordered_at=None):
        self.order_id = order_id
        self.user_id = user_id
        self.total_amount = total_amount
        self.status = status
        self.ordered_at = ordered_at

    def __str__(self):
        return f"Order #{self.order_id} | ₹{self.total_amount:.2f} | {self.status} | {self.ordered_at}"