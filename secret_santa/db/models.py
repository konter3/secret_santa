from dataclasses import dataclass

@dataclass
class Profile:
    user_id: int
    name: str
    wishes: str
    dislikes: str
    delivery_type: str
    address: str
    locked: bool
