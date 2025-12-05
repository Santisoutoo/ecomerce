"""
Modelos Pydantic para autenticación y registro de usuarios.
Define esquemas de validación para requests y responses.
"""

from pydantic import BaseModel, EmailStr, Field, validator
from typing import Optional


class SignUpRequest(BaseModel):
    """
    Modelo para solicitud de registro de nuevo usuario.
    """
    email: EmailStr = Field(..., description="Email del usuario")
    password: str = Field(..., min_length=6, description="Contraseña (mínimo 6 caracteres)")
    nombre: str = Field(..., min_length=1, max_length=50, description="Nombre del usuario")
    apellidos: str = Field(..., min_length=1, max_length=100, description="Apellidos del usuario")
    telefono: Optional[str] = Field(None, description="Teléfono de contacto")
    foto_perfil: Optional[str] = Field(None, description="URL de la foto de perfil")

    @validator('telefono')
    def validate_phone(cls, v):
        """Valida formato de teléfono español (opcional)."""
        if v and len(v) != 9:
            raise ValueError('El teléfono debe tener 9 dígitos')
        return v

    class Config:
        json_schema_extra = {
            "example": {
                "email": "usuario@example.com",
                "password": "Password123",
                "nombre": "Juan",
                "apellidos": "Pérez García",
                "telefono": "612345678",
                "foto_perfil": "https://storage.googleapis.com/bucket/profile.jpg"
            }
        }


class SignInRequest(BaseModel):
    """
    Modelo para solicitud de inicio de sesión.
    """
    email: EmailStr = Field(..., description="Email del usuario")
    password: str = Field(..., description="Contraseña")

    class Config:
        json_schema_extra = {
            "example": {
                "email": "usuario@example.com",
                "password": "Password123"
            }
        }


class TokenResponse(BaseModel):
    """
    Modelo para respuesta con token de acceso.
    """
    access_token: str = Field(..., description="Token JWT de acceso")
    token_type: str = Field(default="bearer", description="Tipo de token")
    user_id: str = Field(..., description="ID del usuario")
    email: str = Field(..., description="Email del usuario")

    class Config:
        json_schema_extra = {
            "example": {
                "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
                "token_type": "bearer",
                "user_id": "abc123def456",
                "email": "usuario@example.com"
            }
        }


class UserResponse(BaseModel):
    """
    Modelo para respuesta con información del usuario.
    """
    uid: str = Field(..., description="ID único del usuario")
    email: str = Field(..., description="Email del usuario")
    nombre: Optional[str] = Field(None, description="Nombre del usuario")
    apellidos: Optional[str] = Field(None, description="Apellidos del usuario")
    telefono: Optional[str] = Field(None, description="Teléfono")
    foto_perfil: Optional[str] = Field(None, description="URL de la foto de perfil")
    puntos_fidelizacion: int = Field(default=0, description="Puntos acumulados")
    es_admin: bool = Field(default=False, description="Si es administrador")

    class Config:
        json_schema_extra = {
            "example": {
                "uid": "abc123def456",
                "email": "usuario@example.com",
                "nombre": "Juan",
                "apellidos": "Pérez García",
                "telefono": "612345678",
                "foto_perfil": "https://storage.googleapis.com/bucket/profile.jpg",
                "puntos_fidelizacion": 500,
                "es_admin": False
            }
        }


class MessageResponse(BaseModel):
    """
    Modelo genérico para respuestas con mensaje.
    """
    message: str = Field(..., description="Mensaje de respuesta")

    class Config:
        json_schema_extra = {
            "example": {
                "message": "Operación exitosa"
            }
        }
