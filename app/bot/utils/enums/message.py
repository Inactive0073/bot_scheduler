from enum import Enum


class MediaType(str, Enum):
    PHOTO = "photo"
    VIDEO = "video"
    
class PostStatus(str, Enum):
    SCHEDULED = "scheduled"
    SENT ="sent"
    CANCELED = "cancelled"
    FAILED = "failed"