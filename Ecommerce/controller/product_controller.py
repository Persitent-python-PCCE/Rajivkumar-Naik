from service.product_service import ProductService
from model.product import Product


class ProductController:

    def __init__(self):
        self.product_service = ProductService()

    def add_product(self, current_user):
        name = input("Enter product name: ").strip()
        description = input("Enter description: ").strip()
        price = float(input("Enter price: "))
        stock = int(input("Enter stock: "))
        category = input("Enter category: ").strip()

        product = Product(
            name,
            description,
            price,
            stock,
            category
        )

        try:
            product_id = self.product_service.add_product(
                current_user,
                product
            )

            print(f"Product added successfully! ID: {product_id}")

        except (ValueError, PermissionError) as e:
            print(f" {e}")

        except RuntimeError as e:
            print(f" {e}")

        except Exception as e:
            print(f" Unexpected error: {e}")

    def _prompt_filters(self):
        print("\n--- Filter products (press Enter to skip any) ---")

        category = input("Category: ").strip() or None
        search = input("Search by name: ").strip() or None

        min_input = input("Min price: ").strip()
        max_input = input("Max price: ").strip()

        try:
            min_price = float(min_input) if min_input else None
            max_price = float(max_input) if max_input else None

        except ValueError:
            print("❌ Invalid price entered — ignoring price filter.")
            min_price = None
            max_price = None

        return category, search, min_price, max_price

    def list_products(self):
        page = 1
        page_size = 10

        category, search, min_price, max_price = self._prompt_filters()

        while True:
            try:
                result = self.product_service.list_products(
                    page=page,
                    page_size=page_size,
                    category=category,
                    min_price=min_price,
                    max_price=max_price,
                    search=search
                )

                products = result['products']
                page = result['page']

                if not products:
                    print("No products found matching your filters.")
                    return

                print(
                    f"\nPage {result['page']} of {result['total_pages']} "
                    f"(Total: {result['total_count']} products)"
                )
                print("-" * 60)

                for product in products:
                    print(product)

                print("-" * 60)
                print(
                    "[N] Next page   [P] Previous page   "
                    "[F] Change filters   [Q] Back to menu"
                )

                nav = input("Choice: ").strip().lower()

                if nav == 'n':
                    if page < result['total_pages']:
                        page += 1
                    else:
                        print("Already on the last page.")

                elif nav == 'p':
                    if page > 1:
                        page -= 1
                    else:
                        print("Already on the first page.")

                elif nav == 'f':
                    category, search, min_price, max_price = (
                        self._prompt_filters()
                    )
                    page = 1

                elif nav == 'q':
                    return

                else:
                    print("Invalid choice.")

            except RuntimeError as e:
                print(f"❌ {e}")
                return

            except Exception as e:
                print(f"❌ Unexpected error: {e}")
                return

    def get_product(self):
        product_id = int(input("Enter product ID: "))

        try:
            product = self.product_service.get_product(product_id)

            if not product:
                print("Product not found.")
                return

            print(product)

        except RuntimeError as e:
            print(f" {e}")

        except Exception as e:
            print(f" Unexpected error: {e}")

    def update_product(self, current_user):
        product_id = int(input("Enter product ID: "))
        name = input("Enter new name: ").strip()
        description = input("Enter new description: ").strip()
        price = float(input("Enter new price: "))
        stock = int(input("Enter new stock: "))
        category = input("Enter new category: ").strip()

        product = Product(
            name,
            description,
            price,
            stock,
            category,
            product_id
        )

        try:
            self.product_service.update_product(
                current_user,
                product
            )

            print("Product updated successfully.")

        except (ValueError, PermissionError) as e:
            print(f" {e}")

        except RuntimeError as e:
            print(f" {e}")

        except Exception as e:
            print(f" Unexpected error: {e}")

    def delete_product(self, current_user):
        product_id = int(input("Enter product ID: "))

        try:
            self.product_service.delete_product(
                current_user,
                product_id
            )

            print("Product deleted successfully.")

        except (ValueError, PermissionError) as e:
            print(f" {e}")

        except RuntimeError as e:
            print(f" {e}")

        except Exception as e:
            print(f" Unexpected error: {e}")