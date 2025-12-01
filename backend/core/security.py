"""
Módulo de seguridad para manejo de autenticación y autorización.
Implementa JWT tokens y validación con Firebase Authentication.
"""

from datetime import datetime, timedelta
from typing import Optional
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import JWTError, jwt
from config.settings import SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES
from config.firebase_config import get_auth_client


# Esquema de seguridad HTTP Bearer
security = HTTPBearer()


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    """
    Crea un token JWT con los datos del usuario.

    Args:
        data: Diccionario con información del usuario (user_id, email, etc.)
        expires_delta: Tiempo de expiración del token (opcional)

    Returns:
        str: Token JWT codificado
    """
    to_encode = data.copy()

    # Establecer tiempo de expiración
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    to_encode.update({"exp": expire})

    # Codificar el token
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def decode_access_token(token: str) -> dict:
    """
    Decodifica un token JWT y valida su autenticidad.

    Args:
        token: Token JWT a decodificar

    Returns:
        dict: Datos del payload del token

    Raises:
        HTTPException: Si el token es inválido o expiró
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    """
    Obtiene el usuario actual desde el token JWT.
    Valida el token contra Firebase Authentication.

    Args:
        credentials: Credenciales HTTP Bearer del header Authorization

    Returns:
        dict: Información del usuario actual

    Raises:
        HTTPException: Si el token es inválido o el usuario no existe
    """
    token = credentials.credentials

    # Decodificar JWT
    payload = decode_access_token(token)

    user_id: str = payload.get("sub")
    if user_id is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials"
        )

    # Validar usuario en Firebase
    try:
        auth_client = get_auth_client()
        user = auth_client.get_user(user_id)

        return {
            "uid": user.uid,
            "email": user.email,
            "display_name": user.display_name,
            "email_verified": user.email_verified
        }

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found or token expired"
        )


async def verify_firebase_token(token: str) -> dict:
    """
    Verifica un token de Firebase Authentication directamente.
    Útil para validar tokens generados por el SDK de Firebase en el cliente.

    Args:
        token: ID token de Firebase

    Returns:
        dict: Información del usuario decodificada

    Raises:
        HTTPException: Si el token es inválido
    """
    try:
        auth_client = get_auth_client()
        decoded_token = auth_client.verify_id_token(token)
        return decoded_token
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Invalid Firebase token: {str(e)}"
        )
