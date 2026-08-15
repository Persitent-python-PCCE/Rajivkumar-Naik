class User:
    def __init__(self, username, password, email, role='customer', user_id=None):
        self.user_id = user_id
        self.username = username
        self.password = password
        self.email = email
        self.role = role

    def __str__(self):
        return f"[{self.role.upper()}] {self.username} (ID: {self.user_id})"


class AdminUser(User):
    def __init__(self, username, password, email, user_id=None):
        super().__init__(
            username,
            password,
            email,
            role='admin',
            user_id=user_id
        )



# if __name__ == "__main__":
#     user = User("rajiv", "hash123", "rajiv@gmail.com")
#     admin = AdminUser("admin", "hash456", "admin@gmail.com", 2)

#     print(user)
#     print(admin)

#     print(isinstance(user, User))
#     print(isinstance(admin, User))
#     print(isinstance(admin, AdminUser))