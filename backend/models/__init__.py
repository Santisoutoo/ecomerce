"""
Modelos de la aplicación.
Exporta todos los modelos para facilitar las importaciones.
"""

from .auth import (
    SignUpRequest,
    SignInRequest,
    TokenResponse,
    UserResponse,
    MessageResponse as AuthMessageResponse
)

from .models import (
    # Enums
    CategoryEnum,
    LeagueEnum,
    SizeEnum,
    OrderStatusEnum,

    # Product Models
    ProductImages,
    Product,
    ProductCreate,
    ProductUpdate,

    # Category Models
    Category,

    # League Models
    League,

    # User Models
    User,
    UserCreate,
    UserUpdate,
    UserPublic,

    # Cart Models
    CartItem,
    CartItemCreate,
    CartItemUpdate,

    # Order Models
    OrderItem,
    ShippingAddress,
    Order,
    OrderCreate,
    OrderUpdate,

    # Response Models
    MessageResponse,
    PaginatedResponse
)

__all__ = [
    # Auth
    "SignUpRequest",
    "SignInRequest",
    "TokenResponse",
    "UserResponse",
    "AuthMessageResponse",

    # Enums
    "CategoryEnum",
    "LeagueEnum",
    "SizeEnum",
    "OrderStatusEnum",

    # Product Models
    "ProductImages",
    "Product",
    "ProductCreate",
    "ProductUpdate",

    # Category Models
    "Category",

    # League Models
    "League",

    # User Models
    "User",
    "UserCreate",
    "UserUpdate",
    "UserPublic",

    # Cart Models
    "CartItem",
    "CartItemCreate",
    "CartItemUpdate",

    # Order Models
    "OrderItem",
    "ShippingAddress",
    "Order",
    "OrderCreate",
    "OrderUpdate",

    # Response Models
    "MessageResponse",
    "PaginatedResponse",
]
