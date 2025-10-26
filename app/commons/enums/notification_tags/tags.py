from enum import Enum

class NotificationTag(Enum):
    SEND_MESSAGE = "send-message"
    
    @classmethod
    def list(cls):
        """Returns a list of possible tags."""
        return [tag.value for tag in cls]
