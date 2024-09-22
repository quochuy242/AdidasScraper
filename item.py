from pydantic import BaseModel


class Item(BaseModel):
    id: str
    title: str
    subtitle: str
    division: str
    price: int
    link: str
