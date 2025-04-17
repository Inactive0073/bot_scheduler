from dataclasses import dataclass


@dataclass
class NotifyAlert:
    id: str
    desc: str
    
@dataclass
class TgChannel:
    id: int
    fullname: str
    username: str
    link: str