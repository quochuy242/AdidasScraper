from pydantic import BaseModel
from typing import List, Dict


# Class to store product information
class Product(BaseModel):
    name: str = ""
    category: str = ""
    price: int = 0
    url: str = ""
    image_url: Dict[str, str] = {}
    size: List[str] = []
