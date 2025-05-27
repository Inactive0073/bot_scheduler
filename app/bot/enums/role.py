from enum import Enum

class UserType(str, Enum):
    WAITER = "waiter"
    MANAGER = "manager"
    ADMIN = "admin"
    OWNER = "owner"