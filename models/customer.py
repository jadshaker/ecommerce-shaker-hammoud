from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional


@dataclass
class Customer:
    full_name: str
    username: str
    password: str
    age: int
    address: Optional[str] = None
    gender: Optional[str] = None
    marital_status: Optional[str] = None
    wallet_balance: float = 0.0
    created_at: datetime = field(default_factory=datetime.now)
    customer_id: Optional[int] = None
