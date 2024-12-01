from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional


@dataclass
class Customer:
    """
    Customer class represents a customer in the ecommerce system.

    Attributes:
        full_name (str): The full name of the customer.
        username (str): The username of the customer.
        password (str): The password of the customer.
        age (int): The age of the customer.
        address (Optional[str]): The address of the customer. Defaults to None.
        gender (Optional[str]): The gender of the customer. Defaults to None.
        marital_status (Optional[str]): The marital status of the customer. Defaults to None.
        wallet_balance (float): The wallet balance of the customer. Defaults to 0.0.
        created_at (datetime): The datetime when the customer was created. Defaults to the current datetime.
        customer_id (Optional[int]): The unique identifier of the customer. Defaults to None.
    """
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
