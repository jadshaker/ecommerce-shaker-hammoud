from datetime import datetime
from dataclasses import dataclass, field
from typing import Optional

@dataclass
class Customer:
    full_name: str
    username: str
    password: str
    age: int
    address: Optional[str] = None
    gender: Optional[str] = None
    wallet_balance: float = 0.0
    created_at: datetime = field(default_factory=datetime.utcnow)  # Ensure it's a datetime object
    customer_id: Optional[int] = None
