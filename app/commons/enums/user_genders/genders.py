from enum import Enum

class UserGender(Enum):
    MALE = "male"
    FEMALE = "female"
    
    @classmethod
    def list(cls):
        """Returns a list of possible genders."""
        return [gender.value for gender in cls]
