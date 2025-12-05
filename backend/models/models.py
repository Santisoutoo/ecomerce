"""
Modelos Pydantic para la aplicación SportStyle Store.
Define esquemas de validación para productos, usuarios, pedidos, etc.
"""

from pydantic import BaseModel, EmailStr, Field, validator
from typing import Optional, List, Dict
from datetime import datetime
from enum import Enum


# ============================================================================
# ENUMS
# ============================================================================

class CategoryEnum(str, Enum):
    """Categorías de productos disponibles."""
    FUTBOL = "futbol"
    FORMULA1 = "formula1"
    BALONCESTO = "baloncesto"


class LeagueEnum(str, Enum):
    """Ligas deportivas disponibles."""
    LALIGA = "laliga"
    F1 = "f1"
    ACB = "acb"


class SizeEnum(str, Enum):
    """Tallas disponibles."""
    S = "S"
    M = "M"
    L = "L"
    XL = "XL"
    XXL = "XXL"


class OrderStatusEnum(str, Enum):
    """Estados de pedidos."""
    PENDING = "pending"
    PROCESSING = "processing"
    SHIPPED = "shipped"
    DELIVERED = "delivered"
    CANCELLED = "cancelled"


# ============================================================================
# PRODUCT MODELS
# ============================================================================

class ProductImages(BaseModel):
    """Modelo para las imágenes de un producto."""
    main: str = Field(..., description="URL de la imagen principal")
    gallery: List[str] = Field(default_factory=list, description="URLs de las imágenes de la galería")

    class Config:
        json_schema_extra = {
            "example": {
                "main": "https://example.com/image.jpg",
                "gallery": ["https://example.com/image1.jpg", "https://example.com/image2.jpg"]
            }
        }


class Product(BaseModel):
    """Modelo completo de un producto."""
    id: str = Field(..., description="ID único del producto")
    name: str = Field(..., min_length=1, max_length=200, description="Nombre del producto")
    description: str = Field(..., min_length=1, description="Descripción del producto")
    price: float = Field(..., gt=0, description="Precio del producto")
    currency: str = Field(default="EUR", description="Moneda del precio")
    category: CategoryEnum = Field(..., description="Categoría del producto")
    league: LeagueEnum = Field(..., description="Liga deportiva")
    team: str = Field(..., min_length=1, description="Equipo deportivo")
    images: ProductImages = Field(..., description="Imágenes del producto")
    sizes: List[SizeEnum] = Field(..., min_items=1, description="Tallas disponibles")
    stock: Dict[str, int] = Field(..., description="Stock por talla")
    featured: bool = Field(default=False, description="Producto destacado")
    active: bool = Field(default=True, description="Producto activo")

    @validator('stock')
    def validate_stock(cls, v, values):
        """Valida que el stock tenga las mismas tallas que sizes."""
        if 'sizes' in values:
            sizes = [size.value for size in values['sizes']]
            stock_sizes = list(v.keys())
            if set(sizes) != set(stock_sizes):
                raise ValueError('Las tallas del stock deben coincidir con las tallas disponibles')
        return v

    class Config:
        json_schema_extra = {
            "example": {
                "id": "prod_001",
                "name": "Camiseta FC Barcelona",
                "description": "Camiseta oficial del FC Barcelona temporada 2024",
                "price": 89.99,
                "currency": "EUR",
                "category": "futbol",
                "league": "laliga",
                "team": "Barcelona",
                "images": {
                    "main": "https://example.com/barcelona.jpg",
                    "gallery": ["https://example.com/barcelona1.jpg"]
                },
                "sizes": ["S", "M", "L", "XL", "XXL"],
                "stock": {
                    "S": 12,
                    "M": 18,
                    "L": 22,
                    "XL": 15,
                    "XXL": 7
                },
                "featured": True,
                "active": True
            }
        }


class ProductCreate(BaseModel):
    """Modelo para crear un nuevo producto."""
    name: str = Field(..., min_length=1, max_length=200)
    description: str = Field(..., min_length=1)
    price: float = Field(..., gt=0)
    currency: str = Field(default="EUR")
    category: CategoryEnum
    league: LeagueEnum
    team: str = Field(..., min_length=1)
    images: ProductImages
    sizes: List[SizeEnum] = Field(..., min_items=1)
    stock: Dict[str, int]
    featured: bool = Field(default=False)
    active: bool = Field(default=True)


class ProductUpdate(BaseModel):
    """Modelo para actualizar un producto existente."""
    name: Optional[str] = Field(None, min_length=1, max_length=200)
    description: Optional[str] = Field(None, min_length=1)
    price: Optional[float] = Field(None, gt=0)
    currency: Optional[str] = None
    category: Optional[CategoryEnum] = None
    league: Optional[LeagueEnum] = None
    team: Optional[str] = Field(None, min_length=1)
    images: Optional[ProductImages] = None
    sizes: Optional[List[SizeEnum]] = None
    stock: Optional[Dict[str, int]] = None
    featured: Optional[bool] = None
    active: Optional[bool] = None


# ============================================================================
# CATEGORY MODELS
# ============================================================================

class Category(BaseModel):
    """Modelo de categoría de productos."""
    id: str = Field(..., description="ID único de la categoría")
    name: str = Field(..., description="Nombre interno de la categoría")
    display_name: str = Field(..., description="Nombre para mostrar")
    description: str = Field(..., description="Descripción de la categoría")
    active: bool = Field(default=True, description="Categoría activa")

    class Config:
        json_schema_extra = {
            "example": {
                "id": "cat_001",
                "name": "futbol",
                "display_name": "Fútbol",
                "description": "Camisetas oficiales de equipos de fútbol",
                "active": True
            }
        }


# ============================================================================
# LEAGUE MODELS
# ============================================================================

class League(BaseModel):
    """Modelo de liga deportiva."""
    id: str = Field(..., description="ID único de la liga")
    name: str = Field(..., description="Nombre interno de la liga")
    display_name: str = Field(..., description="Nombre para mostrar")
    category: str = Field(..., description="Categoría a la que pertenece")
    country: str = Field(..., description="País de la liga")
    active: bool = Field(default=True, description="Liga activa")

    class Config:
        json_schema_extra = {
            "example": {
                "id": "league_001",
                "name": "laliga",
                "display_name": "LaLiga",
                "category": "futbol",
                "country": "España",
                "active": True
            }
        }


# ============================================================================
# USER MODELS
# ============================================================================

class User(BaseModel):
    """Modelo completo de usuario."""
    id: str = Field(..., description="ID único del usuario")
    nombre: str = Field(..., min_length=1, max_length=50, description="Nombre del usuario")
    apellido: str = Field(..., min_length=1, max_length=100, description="Apellido del usuario")
    email: EmailStr = Field(..., description="Email del usuario")
    tlf: Optional[str] = Field(None, description="Teléfono del usuario")
    password: str = Field(..., description="Contraseña hasheada")
    avatar: Optional[str] = Field(None, description="URL del avatar")

    @validator('tlf')
    def validate_phone(cls, v):
        """Valida formato de teléfono internacional."""
        if v and not v.startswith('+'):
            raise ValueError('El teléfono debe incluir el código de país (ej: +34)')
        return v

    class Config:
        json_schema_extra = {
            "example": {
                "id": "user_001",
                "nombre": "Juan",
                "apellido": "Pérez García",
                "email": "juan.perez@example.com",
                "tlf": "+34 610 123 456",
                "password": "$2b$10$N9qo8uLOickgx2ZMRZoMyeIjZAgcfl7p92ldGxad68LJZdL17lhWy",
                "avatar": "https://res.cloudinary.com/dlrrvenn1/image/upload/v1734567890/avatars/default_avatar.jpg"
            }
        }


class UserCreate(BaseModel):
    """Modelo para crear un nuevo usuario."""
    nombre: str = Field(..., min_length=1, max_length=50)
    apellido: str = Field(..., min_length=1, max_length=100)
    email: EmailStr
    tlf: Optional[str] = None
    password: str = Field(..., min_length=6)
    avatar: Optional[str] = None


class UserUpdate(BaseModel):
    """Modelo para actualizar un usuario existente."""
    nombre: Optional[str] = Field(None, min_length=1, max_length=50)
    apellido: Optional[str] = Field(None, min_length=1, max_length=100)
    email: Optional[EmailStr] = None
    tlf: Optional[str] = None
    avatar: Optional[str] = None


class UserPublic(BaseModel):
    """Modelo público de usuario (sin password)."""
    id: str
    nombre: str
    apellido: str
    email: EmailStr
    tlf: Optional[str] = None
    avatar: Optional[str] = None


# ============================================================================
# CART MODELS
# ============================================================================

class Personalization(BaseModel):
    """Modelo de personalización de producto."""
    nombre: Optional[str] = Field(None, max_length=15, description="Nombre a personalizar (máx 15 caracteres)")
    numero: Optional[int] = Field(None, ge=0, le=99, description="Número a personalizar (0-99)")

    class Config:
        json_schema_extra = {
            "example": {
                "nombre": "RONALDO",
                "numero": 7
            }
        }


class CartItem(BaseModel):
    """Modelo de item del carrito de compras."""
    id: str = Field(..., description="ID único del item del carrito")
    user_id: str = Field(..., description="ID del usuario")
    product_id: str = Field(..., description="ID del producto")
    product_name: str = Field(..., description="Nombre del producto")
    product_image: str = Field(..., description="URL de la imagen del producto")
    team: str = Field(..., description="Equipo del producto")
    quantity: int = Field(..., gt=0, description="Cantidad del producto")
    size: str = Field(..., description="Talla seleccionada")
    unit_price: float = Field(..., gt=0, description="Precio unitario del producto")
    personalization_price: float = Field(default=0, ge=0, description="Precio de personalización")
    personalization: Optional[Personalization] = Field(None, description="Datos de personalización")
    subtotal: float = Field(..., gt=0, description="Subtotal del item (precio × cantidad)")
    created_at: Optional[datetime] = Field(default_factory=datetime.utcnow, description="Fecha de creación")
    updated_at: Optional[datetime] = Field(default_factory=datetime.utcnow, description="Fecha de actualización")

    class Config:
        json_schema_extra = {
            "example": {
                "id": "cart_001",
                "user_id": "user_001",
                "product_id": "prod_001",
                "product_name": "Camiseta FC Barcelona",
                "product_image": "https://example.com/image.jpg",
                "team": "Barcelona",
                "quantity": 2,
                "size": "L",
                "unit_price": 89.99,
                "personalization_price": 10.00,
                "personalization": {
                    "nombre": "MESSI",
                    "numero": 10
                },
                "subtotal": 199.98,
                "created_at": "2024-12-05T10:30:00",
                "updated_at": "2024-12-05T10:30:00"
            }
        }


class CartItemCreate(BaseModel):
    """Modelo para añadir un item al carrito."""
    product_id: str = Field(..., description="ID del producto")
    quantity: int = Field(default=1, gt=0, description="Cantidad")
    size: str = Field(..., description="Talla")
    personalization: Optional[Personalization] = Field(None, description="Datos de personalización")


class CartItemUpdate(BaseModel):
    """Modelo para actualizar un item del carrito."""
    quantity: Optional[int] = Field(None, gt=0)
    size: Optional[str] = None
    personalization: Optional[Personalization] = None


class Cart(BaseModel):
    """Modelo completo del carrito de compras."""
    user_id: str = Field(..., description="ID del usuario en Firebase Auth")
    user_email: EmailStr = Field(..., description="Email del usuario en texto plano")
    items: List[CartItem] = Field(default_factory=list, description="Items del carrito")
    total_items: int = Field(default=0, ge=0, description="Total de items en el carrito")
    subtotal: float = Field(default=0, ge=0, description="Subtotal del carrito")
    updated_at: Optional[datetime] = Field(default_factory=datetime.utcnow, description="Fecha de actualización")

    class Config:
        json_schema_extra = {
            "example": {
                "user_id": "fZlBToT35rPVcuUg3SO1oTuXwM22",
                "user_email": "hola@gmail.com",
                "items": [
                    {
                        "id": "cart_001",
                        "user_id": "fZlBToT35rPVcuUg3SO1oTuXwM22",
                        "product_id": "prod_001",
                        "product_name": "Camiseta FC Barcelona",
                        "product_image": "https://example.com/image.jpg",
                        "team": "Barcelona",
                        "quantity": 2,
                        "size": "L",
                        "unit_price": 89.99,
                        "personalization_price": 10.00,
                        "personalization": {"nombre": "MESSI", "numero": 10},
                        "subtotal": 199.98
                    }
                ],
                "total_items": 2,
                "subtotal": 199.98,
                "updated_at": "2024-12-05T10:30:00"
            }
        }


# ============================================================================
# ORDER MODELS
# ============================================================================

class OrderItem(BaseModel):
    """Modelo de item dentro de un pedido."""
    product_id: str = Field(..., description="ID del producto")
    product_name: str = Field(..., description="Nombre del producto")
    product_image: str = Field(..., description="URL de la imagen del producto")
    team: str = Field(..., description="Equipo del producto")
    quantity: int = Field(..., gt=0, description="Cantidad")
    size: str = Field(..., description="Talla")
    unit_price: float = Field(..., gt=0, description="Precio unitario")
    personalization_price: float = Field(default=0, ge=0, description="Precio de personalización")
    personalization: Optional[Personalization] = Field(None, description="Datos de personalización")
    subtotal: float = Field(..., gt=0, description="Subtotal (precio × cantidad)")


class ShippingAddress(BaseModel):
    """Modelo de dirección de envío."""
    street: str = Field(..., description="Calle y número")
    city: str = Field(..., description="Ciudad")
    state: str = Field(..., description="Provincia/Estado")
    postal_code: str = Field(..., description="Código postal")
    country: str = Field(default="España", description="País")


class Order(BaseModel):
    """Modelo completo de pedido."""
    order_id: str = Field(..., description="ID único del pedido (ej: ORD-20241205-001)")
    user_id: str = Field(..., description="ID del usuario en Firebase Auth")
    user_email: EmailStr = Field(..., description="Email del usuario como identificador del pedido")
    items: List[OrderItem] = Field(..., min_items=1, description="Items del pedido")
    subtotal: float = Field(..., gt=0, description="Subtotal de productos")
    shipping_cost: float = Field(default=0, ge=0, description="Costo de envío")
    tax: float = Field(default=0, ge=0, description="Impuestos")
    total: float = Field(..., gt=0, description="Total del pedido")
    status: OrderStatusEnum = Field(default=OrderStatusEnum.PENDING, description="Estado del pedido")
    shipping_address: ShippingAddress = Field(..., description="Dirección de envío")
    payment_method: str = Field(..., description="Método de pago")
    created_at: datetime = Field(default_factory=datetime.utcnow, description="Fecha de creación")
    updated_at: datetime = Field(default_factory=datetime.utcnow, description="Fecha de actualización")

    class Config:
        json_schema_extra = {
            "example": {
                "order_id": "ORD-20241205-001",
                "user_id": "fZlBToT35rPVcuUg3SO1oTuXwM22",
                "user_email": "hola@gmail.com",
                "items": [
                    {
                        "product_id": "prod_001",
                        "product_name": "Camiseta FC Barcelona",
                        "product_image": "https://res.cloudinary.com/dlrrvenn1/image/upload/v1764772154/camiseta_barcelona_lgranp.jpg",
                        "team": "Barcelona",
                        "quantity": 2,
                        "size": "L",
                        "unit_price": 89.99,
                        "personalization_price": 10.00,
                        "personalization": {
                            "nombre": "MESSI",
                            "numero": 10
                        },
                        "subtotal": 199.98
                    }
                ],
                "subtotal": 199.98,
                "shipping_cost": 5.00,
                "tax": 43.05,
                "total": 248.03,
                "status": "pending",
                "shipping_address": {
                    "street": "Calle Ejemplo 123",
                    "city": "Barcelona",
                    "state": "Barcelona",
                    "postal_code": "08001",
                    "country": "España"
                },
                "payment_method": "credit_card",
                "created_at": "2024-12-05T10:30:00",
                "updated_at": "2024-12-05T10:30:00"
            }
        }


class OrderCreate(BaseModel):
    """Modelo para crear un nuevo pedido."""
    items: List[OrderItem] = Field(..., min_items=1)
    shipping_address: ShippingAddress
    payment_method: str = Field(..., description="Método de pago")


class OrderUpdate(BaseModel):
    """Modelo para actualizar un pedido."""
    status: Optional[OrderStatusEnum] = None
    shipping_address: Optional[ShippingAddress] = None


# ============================================================================
# RESPONSE MODELS
# ============================================================================

class MessageResponse(BaseModel):
    """Respuesta genérica con mensaje."""
    message: str

    class Config:
        json_schema_extra = {
            "example": {
                "message": "Operación exitosa"
            }
        }


class PaginatedResponse(BaseModel):
    """Respuesta paginada genérica."""
    items: List[BaseModel]
    total: int = Field(..., description="Total de items")
    page: int = Field(..., ge=1, description="Página actual")
    page_size: int = Field(..., ge=1, le=100, description="Tamaño de página")
    total_pages: int = Field(..., description="Total de páginas")
