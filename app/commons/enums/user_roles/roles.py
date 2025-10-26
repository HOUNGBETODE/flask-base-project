from enum import Enum

class UserRole(Enum):
    USER = "user"
    ENTERPRISE = "enterprise"
    ADMIN = "admin"
    SUPER_ADMIN = "super_admin"
    
    @classmethod
    def list(cls):
        """Returns a list of possible roles."""
        return [role.value for role in cls]
