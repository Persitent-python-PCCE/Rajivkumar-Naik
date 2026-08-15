from service.user_service import UserService
from service.file_service import FileService


class UserController:

    def __init__(self):
        self.user_service = UserService()
        self.file_service = FileService()

    def register(self):
        username = input("Enter username: ").strip()
        password = input("Enter password: ")
        email = input("Enter email: ").strip()

        try:
            user_id = self.user_service.register(
                username,
                password,
                email
            )

            print(f"Registration successful! User ID: {user_id}")

            self.file_service.write_log(
                user_id,
                'REGISTER',
                f"username={username}"
            )

        except ValueError as e:
            print(f" {e}")

        except RuntimeError as e:
            print(f" {e}")

        except Exception as e:
            print(f" Unexpected error: {e}")

    def login(self):
        username = input("Enter username: ").strip()
        password = input("Enter password: ")

        try:
            user = self.user_service.login(
                username,
                password
            )

            print(f"Login successful! Welcome, {user.username}.")

            self.file_service.write_log(
                user.user_id,
                'LOGIN',
                f"username={username}"
            )

            return user

        except ValueError as e:
            print(f" {e}")
            return None

        except RuntimeError as e:
            print(f" {e}")
            return None

        except Exception as e:
            print(f" Unexpected error: {e}")
            return None