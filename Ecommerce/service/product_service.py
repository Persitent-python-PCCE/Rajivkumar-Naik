import math

from dao.product_dao import ProductDAO
from model.product import Product
from model.user import AdminUser


class ProductService:

    def __init__(self):
        self.product_dao = ProductDAO()

    def _require_admin(self, requester):
        if not isinstance(requester, AdminUser):
            raise PermissionError("Admin access required.")

    def add_product(self, requester, product):
        self._require_admin(requester)

        if product.price <= 0:
            raise ValueError("Price must be greater than 0.")

        if product.stock < 0:
            raise ValueError("Stock cannot be negative.")

        return self.product_dao.insert(product)

    def list_products(self, page=1, page_size=10, category=None,
                       min_price=None, max_price=None, search=None):
        try:
            if page < 1:
                raise ValueError("Page must be 1 or greater.")

            if page_size < 1:
                raise ValueError("Page size must be at least 1.")

            if min_price is not None and min_price < 0:
                raise ValueError("Minimum price cannot be negative.")

            if max_price is not None and max_price < 0:
                raise ValueError("Maximum price cannot be negative.")

            if (min_price is not None and max_price is not None
                    and min_price > max_price):
                raise ValueError(
                    "Minimum price cannot exceed maximum price."
                )

            total_count = self.product_dao.count_products(
                category, min_price, max_price, search
            )

            total_pages = (
                math.ceil(total_count / page_size) if total_count else 1
            )

            # Clamp to the last valid page instead of returning nothing.
            if page > total_pages:
                page = total_pages

            products = self.product_dao.get_paginated(
                page, page_size, category, min_price, max_price, search
            )

            return {
                'products': products,
                'page': page,
                'page_size': page_size,
                'total_count': total_count,
                'total_pages': total_pages
            }

        except ValueError:
            raise

        except RuntimeError:
            raise

        except Exception as e:
            raise RuntimeError(
                f"[ProductService.list_products] Unexpected error: {e}"
            )

    def get_product(self, product_id):
        return self.product_dao.get_by_id(product_id)

    def update_product(self, requester, product):
        self._require_admin(requester)

        if product.price <= 0:
            raise ValueError("Price must be greater than 0.")

        if product.stock < 0:
            raise ValueError("Stock cannot be negative.")

        self.product_dao.update(product)

    def delete_product(self, requester, product_id):
        self._require_admin(requester)

        self.product_dao.delete(product_id)