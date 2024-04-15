from pydantic import BaseModel


class Product(BaseModel):
    """
    Clase que representa un producto.
    """
    id: int
    name: str
    description: str
    price: float
    unit: int


class ProductCreate(BaseModel):
    """
    Clase que representa un producto.
    """
    name: str
    description: str
    company: str
    price: float
    units: int
    subcategory_id: int
