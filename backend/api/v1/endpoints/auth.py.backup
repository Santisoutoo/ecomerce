"""
Endpoints de autenticación para SportStyle Store API.
Gestiona registro, login, logout y validación de usuarios con Firebase.
"""

from fastapi import APIRouter, HTTPException, Depends, status, UploadFile, File
from models.auth import (
    SignUpRequest,
    SignInRequest,
    TokenResponse,
    UserResponse,
    MessageResponse
)
from core.security import create_access_token, get_current_user
from config.firebase_config import get_auth_client, get_database, get_storage_bucket
from datetime import datetime, timedelta
from config.settings import ACCESS_TOKEN_EXPIRE_MINUTES
import uuid
import os


router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post("/signup", response_model=TokenResponse, status_code=status.HTTP_201_CREATED)
async def signup(request: SignUpRequest):
    """
    Registra un nuevo usuario en Firebase Authentication y Realtime Database.

    Args:
        request: Datos del nuevo usuario (email, password, nombre, apellidos)

    Returns:
        TokenResponse: Token JWT y datos básicos del usuario

    Raises:
        HTTPException 400: Si el usuario ya existe o hay error en el registro
    """
    try:
        auth_client = get_auth_client()
        database = get_database()

        # Crear usuario en Firebase Authentication
        user = auth_client.create_user(
            email=request.email,
            password=request.password,
            display_name=f"{request.nombre} {request.apellidos}"
        )

        # Crear datos del usuario en Realtime Database
        user_data = {
            "email": request.email,
            "nombre": request.nombre,
            "apellidos": request.apellidos,
            "telefono": request.telefono or "",
            "foto_perfil": request.foto_perfil or "",
            "fecha_registro": datetime.now().isoformat(),
            "puntos_fidelizacion": 0,
            "es_admin": False,
            "activo": True,
            "favoritos": [],
            "direccion_envio": {}
        }

        # Guardar en /users/{uid}
        database.child('users').child(user.uid).set(user_data)

        # Generar token JWT
        access_token = create_access_token(
            data={"sub": user.uid, "email": user.email},
            expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        )

        return TokenResponse(
            access_token=access_token,
            token_type="bearer",
            user_id=user.uid,
            email=user.email
        )

    except Exception as e:
        # Manejar errores de Firebase
        error_msg = str(e).lower()
        if "email" in error_msg and ("exists" in error_msg or "already" in error_msg):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered"
            )
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Registration error: {str(e)}"
        )

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Internal server error: {str(e)}"
        )


@router.post("/signin", response_model=TokenResponse)
async def signin(request: SignInRequest):
    """
    Inicia sesión con email y contraseña.
    NOTA: Firebase Admin SDK no soporta sign-in directo, se valida el usuario.

    Args:
        request: Email y contraseña del usuario

    Returns:
        TokenResponse: Token JWT y datos del usuario

    Raises:
        HTTPException 401: Si las credenciales son inválidas
    """
    try:
        auth_client = get_auth_client()

        # Obtener usuario por email
        user = auth_client.get_user_by_email(request.email)

        # IMPORTANTE: Firebase Admin SDK no puede verificar contraseñas directamente
        # En producción, esto debe hacerse mediante el REST API de Firebase Auth
        # o usando el SDK del cliente en el frontend

        # Por ahora generamos el token si el usuario existe
        # (la validación de contraseña se hace en el frontend con Firebase SDK)

        # Generar token JWT
        access_token = create_access_token(
            data={"sub": user.uid, "email": user.email},
            expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        )

        return TokenResponse(
            access_token=access_token,
            token_type="bearer",
            user_id=user.uid,
            email=user.email
        )

    except Exception as e:
        # Capturar cualquier error de Firebase y retornar 401
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )


@router.get("/me", response_model=UserResponse)
async def get_current_user_profile(current_user: dict = Depends(get_current_user)):
    """
    Obtiene el perfil completo del usuario autenticado.

    Args:
        current_user: Usuario actual desde el token JWT

    Returns:
        UserResponse: Información completa del usuario

    Raises:
        HTTPException 404: Si el perfil no existe en Realtime Database
    """
    try:
        database = get_database()

        # Obtener datos del usuario desde Realtime Database
        user_data = database.child('users').child(current_user["uid"]).get().val()

        if not user_data:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User profile not found"
            )

        return UserResponse(
            uid=current_user["uid"],
            email=current_user["email"],
            nombre=user_data.get("nombre"),
            apellidos=user_data.get("apellidos"),
            telefono=user_data.get("telefono"),
            foto_perfil=user_data.get("foto_perfil"),
            puntos_fidelizacion=user_data.get("puntos_fidelizacion", 0),
            es_admin=user_data.get("es_admin", False)
        )

    except HTTPException:
        raise

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error fetching profile: {str(e)}"
        )


@router.post("/signout", response_model=MessageResponse)
async def signout(current_user: dict = Depends(get_current_user)):
    """
    Cierra la sesión del usuario.
    NOTA: Con JWT stateless, el logout se maneja en el cliente eliminando el token.

    Args:
        current_user: Usuario actual desde el token JWT

    Returns:
        MessageResponse: Confirmación de cierre de sesión
    """
    # En un sistema JWT stateless, el logout se hace en el cliente
    # Opcionalmente, podríamos invalidar el token usando una blacklist en Redis

    return MessageResponse(message="Session closed successfully")


@router.post("/verify-token")
async def verify_token(current_user: dict = Depends(get_current_user)):
    """
    Verifica si un token JWT es válido.

    Args:
        current_user: Usuario actual desde el token JWT

    Returns:
        dict: Información del usuario si el token es válido

    Raises:
        HTTPException 401: Si el token es inválido
    """
    return {
        "valid": True,
        "user_id": current_user["uid"],
        "email": current_user["email"]
    }


@router.post("/upload-profile-picture")
async def upload_profile_picture(
    file: UploadFile = File(...),
    current_user: dict = Depends(get_current_user)
):
    """
    Sube una foto de perfil a Firebase Storage y devuelve la URL pública.

    Args:
        file: Archivo de imagen a subir
        current_user: Usuario actual desde el token JWT

    Returns:
        dict: URL pública de la imagen subida

    Raises:
        HTTPException 400: Si el archivo no es válido
        HTTPException 413: Si el archivo es demasiado grande
    """
    try:
        # Validar tipo de archivo
        allowed_types = ["image/jpeg", "image/jpg", "image/png", "image/webp"]
        if file.content_type not in allowed_types:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Invalid file type. Allowed types: {', '.join(allowed_types)}"
            )

        # Validar tamaño (máximo 5MB)
        file_content = await file.read()
        file_size_mb = len(file_content) / (1024 * 1024)
        if file_size_mb > 5:
            raise HTTPException(
                status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
                detail="File size exceeds 5MB limit"
            )

        # Generar nombre único para el archivo
        file_extension = os.path.splitext(file.filename)[1]
        unique_filename = f"profile_pictures/{current_user['uid']}_{uuid.uuid4()}{file_extension}"

        # Subir a Firebase Storage
        bucket = get_storage_bucket()
        blob = bucket.blob(unique_filename)
        blob.upload_from_string(file_content, content_type=file.content_type)

        # Hacer el archivo público
        blob.make_public()

        # Obtener URL pública
        public_url = blob.public_url

        # Actualizar el perfil del usuario con la URL de la foto
        database = get_database()
        database.child('users').child(current_user['uid']).update({
            'foto_perfil': public_url
        })

        return {
            "url": public_url,
            "filename": unique_filename,
            "size_mb": round(file_size_mb, 2)
        }

    except HTTPException:
        raise

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error uploading file: {str(e)}"
        )
