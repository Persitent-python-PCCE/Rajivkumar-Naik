from controller.user_controller import UserController
from controller.product_controller import ProductController
from controller.cart_controller import CartController
from controller.order_controller import OrderController
from service.file_service import FileService
from model.user import AdminUser


def customer_menu(current_user):

    product_controller = ProductController()
    cart_controller = CartController(current_user)
    order_controller = OrderController(current_user)

    while True:

        print("\n==============================")
        print("       CUSTOMER MENU")
        print("==============================")
        print("1. View all products")
        print("2. View product")
        print("3. Add to cart")
        print("4. View cart")
        print("5. Update cart quantity")
        print("6. Remove from cart")
        print("7. Checkout")
        print("8. My orders")
        print("9. View order detail")
        print("10. Cancel order")
        print("11. Logout")
        print("==============================")

        choice = input("Enter choice: ")

        if choice == "1":
            product_controller.list_products()

        elif choice == "2":
            product_controller.get_product()

        elif choice == "3":
            cart_controller.add_to_cart()

        elif choice == "4":
            cart_controller.view_cart()

        elif choice == "5":
            cart_controller.update_quantity()

        elif choice == "6":
            cart_controller.remove_from_cart()

        elif choice == "7":
            order_controller.place_order()

        elif choice == "8":
            order_controller.view_order_history()

        elif choice == "9":
            order_controller.view_order_detail()

        elif choice == "10":
            order_controller.cancel_order()

        elif choice == "11":
            print("Logged out.")
            break

        else:
            print("Invalid choice.")


def admin_menu(current_user):

    product_controller = ProductController()
    cart_controller = CartController(current_user)
    order_controller = OrderController(current_user)
    file_service = FileService()

    while True:

        print("\n==============================")
        print("          ADMIN MENU")
        print("==============================")
        print("1. View all products")
        print("2. View product")
        print("3. Add product")
        print("4. Update product")
        print("5. Delete product")
        print("6. Add to cart")
        print("7. View cart")
        print("8. Update cart quantity")
        print("9. Remove from cart")
        print("10. Checkout")
        print("11. My orders")
        print("12. View order detail")
        print("13. Cancel order")
        print("14. View Activity Logs")
        print("15. Backup Orders to JSON")
        print("16. Logout")
        print("==============================")

        choice = input("Enter choice: ")

        if choice == "1":
            product_controller.list_products()

        elif choice == "2":
            product_controller.get_product()

        elif choice == "3":
            product_controller.add_product(current_user)

        elif choice == "4":
            product_controller.update_product(current_user)

        elif choice == "5":
            product_controller.delete_product(current_user)

        elif choice == "6":
            cart_controller.add_to_cart()

        elif choice == "7":
            cart_controller.view_cart()

        elif choice == "8":
            cart_controller.update_quantity()

        elif choice == "9":
            cart_controller.remove_from_cart()

        elif choice == "10":
            order_controller.place_order()

        elif choice == "11":
            order_controller.view_order_history()

        elif choice == "12":
            order_controller.view_order_detail()

        elif choice == "13":
            order_controller.cancel_order()

        elif choice == "14":
            logs = file_service.read_logs()

            if not logs:
                print("No logs found.")
            else:
                print(
                    f"\n{'Timestamp':<20} "
                    f"{'User ID':<10} "
                    f"{'Action':<18} "
                    f"{'Details'}"
                )
                print("-" * 70)

                for log in logs[-20:]:
                    print(
                        f"{log['timestamp']:<20} "
                        f"{log['user_id']:<10} "
                        f"{log['action']:<18} "
                        f"{log['details']}"
                    )

        elif choice == "15":
            file_service.backup_orders_json()
            print("Orders backed up to logs/order_backup.json")

        elif choice == "16":
            print("Logged out.")
            break

        else:
            print("Invalid choice.")


def main():

    user_controller = UserController()

    while True:

        print("\n==============================")
        print("       E-COMMERCE APP")
        print("==============================")
        print("1. Register")
        print("2. Login")
        print("3. Exit")
        print("==============================")

        choice = input("Enter choice: ")

        if choice == "1":

            user_controller.register()

        elif choice == "2":

            current_user = user_controller.login()

            if current_user:

                print("\nLogged in as:", current_user.username)
                print("Role:", current_user.role)

                if isinstance(current_user, AdminUser):
                    admin_menu(current_user)

                else:
                    customer_menu(current_user)

        elif choice == "3":

            print("Goodbye!")
            break

        else:

            print("Invalid choice.")


if __name__ == "__main__":
    main()