import hashlib

from dao.user_dao import UserDAO
from model.user import User, AdminUser


class UserService:

    def __init__(self):
        self.user_dao = UserDAO()

    def _hash_password(self, password):
        return hashlib.sha256(password.encode()).hexdigest()

    def register(self, username, password, email, role='customer'):
        try:
            if len(username) < 3 or len(username) > 20:
                raise ValueError("Username must be 3–20 characters.")

            if len(password) < 6:
                raise ValueError("Password must be at least 6 characters.")

            if '@' not in email or '.' not in email:
                raise ValueError("Invalid email format.")

            if role not in ('customer', 'admin'):
                raise ValueError("Role must be 'customer' or 'admin'.")

            if self.user_dao.find_by_username(username):
                raise ValueError(
                    f"Username '{username}' is already taken."
                )

            hashed = self._hash_password(password)

            user = User(
                username,
                hashed,
                email,
                role
            )

            return self.user_dao.insert_user(user)

        except ValueError:
            raise

        except RuntimeError:
            raise

        except Exception as e:
            raise RuntimeError(
                f"[UserService.register] Unexpected error: {e}"
            )

    def login(self, username, password):
        try:
            row = self.user_dao.find_by_username(username)

            if not row:
                raise ValueError("User not found.")

            hashed = self._hash_password(password)

            if hashed != row['password']:
                raise ValueError("Incorrect password.")

            if row['role'] == 'admin':
                return AdminUser(
                    row['username'],
                    row['password'],
                    row['email'],
                    row['user_id']
                )

            return User(
                row['username'],
                row['password'],
                row['email'],
                row['role'],
                row['user_id']
            )

        except ValueError:
            raise

        except RuntimeError:
            raise

        except Exception as e:
            raise RuntimeError(
                f"[UserService.login] Unexpected error: {e}"
            )

    def change_password(self, user_id, old_password, new_password):
        try:
            row = self.user_dao.find_by_id(user_id)

            if not row:
                raise ValueError("User not found.")

            old_hash = self._hash_password(old_password)

            if old_hash != row['password']:
                raise ValueError("Current password is incorrect.")

            if len(new_password) < 6:
                raise ValueError(
                    "New password must be at least 6 characters."
                )

            new_hash = self._hash_password(new_password)

            self.user_dao.update_password(user_id, new_hash)

        except ValueError:
            raise

        except RuntimeError:
            raise

        except Exception as e:
            raise RuntimeError(
                f"[UserService.change_password] Unexpected error: {e}"
            )