class Product:
    def __init__(self, name, description, price, stock, category,
                 product_id=None, created_at=None):
        self.product_id = product_id
        self.name = name
        self.description = description
        self.price = float(price)
        self.stock = int(stock)
        self.category = category
        self.created_at = created_at

    def __str__(self):
        return f"[{self.product_id}] {self.name} | ₹{self.price:.2f} | Stock: {self.stock} | {self.category}"




# if __name__ == "__main__":
#     product = Product(
#         "Keyboard",
#         "Mechanical keyboard",
#         "1500",
#         "10",
#         "Electronics",
#         1
#     )

#     print(product)
#     print(product.price)
#     print(type(product.price))
#     print(type(product.stock))    