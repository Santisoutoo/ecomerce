"""
Servicio de usuarios con Firebase Realtime Database.
Gestiona autenticación, registro y operaciones de usuarios SIN Firebase Authentication.
"""

from typing import Optional
from datetime import datetime
import uuid
import bcrypt
from firebase_admin import db
from config.firebase_config import get_database


class UserService:
    """
    Servicio para gestionar usuarios en Firebase Realtime Database.

    Estructura en Firebase:
    /users/
        {user_id}/
            email: str
            password_hash: str  # Contraseña hasheada con bcrypt
            nombre: str
            apellidos: str
            telefono: str
            foto_perfil: str
            fecha_registro: str (ISO format)
            puntos_fidelizacion: int
            es_admin: bool
            activo: bool
            favoritos: []
            direccion_envio: {}
    """

    @staticmethod
    def _generate_user_id() -> str:
        """
        Genera un ID único para el usuario con formato similar a Firebase Auth.

        Returns:
            str: ID único del usuario (28 caracteres)
        """
        # Generar un ID similar a los de Firebase Auth (28 caracteres alfanuméricos)
        return uuid.uuid4().hex[:14] + uuid.uuid4().hex[:14]

    @staticmethod
    def _hash_password(password: str) -> str:
        """
        Hashea una contraseña usando bcrypt.

        Args:
            password: Contraseña en texto plano

        Returns:
            str: Contraseña hasheada
        """
        # Generar salt y hashear
        salt = bcrypt.gensalt()
        hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
        return hashed.decode('utf-8')

    @staticmethod
    def _verify_password(password: str, password_hash: str) -> bool:
        """
        Verifica si una contraseña coincide con el hash.

        Args:
            password: Contraseña en texto plano
            password_hash: Hash almacenado

        Returns:
            bool: True si coincide, False si no
        """
        return bcrypt.checkpw(password.encode('utf-8'), password_hash.encode('utf-8'))

    @staticmethod
    def _get_users_ref() -> db.Reference:
        """
        Obtiene la referencia a la colección de usuarios en Firebase.

        Returns:
            db.Reference: Referencia a /users
        """
        database = get_database()
        return database.child('users')

    @staticmethod
    def email_exists(email: str) -> bool:
        """
        Verifica si un email ya está registrado.

        Args:
            email: Email a verificar

        Returns:
            bool: True si existe, False si no
        """
        users_ref = UserService._get_users_ref()
        all_users = users_ref.get()

        if not all_users:
            return False

        # Buscar email en todos los usuarios
        for user_data in all_users.values():
            if user_data.get('email') == email:
                return True

        return False

    @staticmethod
    def create_user(
        email: str,
        password: str,
        nombre: str,
        apellidos: str,
        telefono: Optional[str] = None,
        foto_perfil: Optional[str] = None
    ) -> dict:
        """
        Crea un nuevo usuario en Firebase Realtime Database.

        Args:
            email: Email del usuario
            password: Contraseña en texto plano
            nombre: Nombre del usuario
            apellidos: Apellidos del usuario
            telefono: Teléfono (opcional)
            foto_perfil: URL de la foto de perfil (opcional)

        Returns:
            dict: Datos del usuario creado (sin password_hash)

        Raises:
            ValueError: Si el email ya existe
        """
        # Verificar si el email ya existe
        if UserService.email_exists(email):
            raise ValueError("Email already registered")

        # Generar ID único
        user_id = UserService._generate_user_id()

        # Hashear contraseña
        password_hash = UserService._hash_password(password)

        # Preparar datos del usuario
        user_data = {
            "email": email,
            "password_hash": password_hash,
            "nombre": nombre,
            "apellidos": apellidos,
            "telefono": telefono or "",
            "foto_perfil": foto_perfil or "",
            "fecha_registro": datetime.utcnow().isoformat(),
            "puntos_fidelizacion": 0,
            "es_admin": False,
            "activo": True,
            "favoritos": [],
            "direccion_envio": {}
        }

        # Guardar en Firebase
        users_ref = UserService._get_users_ref()
        users_ref.child(user_id).set(user_data)

        # Retornar datos sin el password_hash
        return {
            "user_id": user_id,
            "email": email,
            "nombre": nombre,
            "apellidos": apellidos,
            "telefono": telefono or "",
            "foto_perfil": foto_perfil or "",
            "puntos_fidelizacion": 0,
            "es_admin": False
        }

    @staticmethod
    def authenticate_user(email: str, password: str) -> Optional[dict]:
        """
        Autentica un usuario verificando email y contraseña.

        Args:
            email: Email del usuario
            password: Contraseña en texto plano

        Returns:
            Optional[dict]: Datos del usuario si las credenciales son válidas, None si no
        """
        users_ref = UserService._get_users_ref()
        all_users = users_ref.get()

        if not all_users:
            return None

        # Buscar usuario por email
        for user_id, user_data in all_users.items():
            if user_data.get('email') == email:
                # Verificar que el usuario esté activo
                if not user_data.get('activo', True):
                    return None

                # Verificar contraseña
                password_hash = user_data.get('password_hash')
                if password_hash and UserService._verify_password(password, password_hash):
                    # Retornar datos del usuario (sin password_hash)
                    return {
                        "user_id": user_id,
                        "email": user_data.get('email'),
                        "nombre": user_data.get('nombre'),
                        "apellidos": user_data.get('apellidos'),
                        "telefono": user_data.get('telefono', ''),
                        "foto_perfil": user_data.get('foto_perfil', ''),
                        "puntos_fidelizacion": user_data.get('puntos_fidelizacion', 0),
                        "es_admin": user_data.get('es_admin', False)
                    }

        return None

    @staticmethod
    def get_user_by_id(user_id: str) -> Optional[dict]:
        """
        Obtiene un usuario por su ID.

        Args:
            user_id: ID del usuario

        Returns:
            Optional[dict]: Datos del usuario (sin password_hash) si existe, None si no
        """
        users_ref = UserService._get_users_ref()
        user_data = users_ref.child(user_id).get()

        if not user_data:
            return None

        # Retornar datos sin password_hash
        return {
            "user_id": user_id,
            "email": user_data.get('email'),
            "nombre": user_data.get('nombre'),
            "apellidos": user_data.get('apellidos'),
            "telefono": user_data.get('telefono', ''),
            "foto_perfil": user_data.get('foto_perfil', ''),
            "puntos_fidelizacion": user_data.get('puntos_fidelizacion', 0),
            "es_admin": user_data.get('es_admin', False),
            "activo": user_data.get('activo', True)
        }

    @staticmethod
    def get_user_by_email(email: str) -> Optional[dict]:
        """
        Obtiene un usuario por su email.

        Args:
            email: Email del usuario

        Returns:
            Optional[dict]: Datos del usuario si existe, None si no
        """
        users_ref = UserService._get_users_ref()
        all_users = users_ref.get()

        if not all_users:
            return None

        # Buscar usuario por email
        for user_id, user_data in all_users.items():
            if user_data.get('email') == email:
                return {
                    "user_id": user_id,
                    "email": user_data.get('email'),
                    "nombre": user_data.get('nombre'),
                    "apellidos": user_data.get('apellidos'),
                    "telefono": user_data.get('telefono', ''),
                    "foto_perfil": user_data.get('foto_perfil', ''),
                    "puntos_fidelizacion": user_data.get('puntos_fidelizacion', 0),
                    "es_admin": user_data.get('es_admin', False),
                    "activo": user_data.get('activo', True)
                }

        return None

    @staticmethod
    def update_user(user_id: str, **kwargs) -> bool:
        """
        Actualiza los datos de un usuario.

        Args:
            user_id: ID del usuario
            **kwargs: Campos a actualizar

        Returns:
            bool: True si se actualizó, False si el usuario no existe
        """
        users_ref = UserService._get_users_ref()
        user_ref = users_ref.child(user_id)

        if not user_ref.get():
            return False

        # Filtrar campos permitidos para actualizar
        allowed_fields = ['nombre', 'apellidos', 'telefono', 'foto_perfil',
                         'puntos_fidelizacion', 'es_admin', 'activo', 'direccion_envio']

        update_data = {k: v for k, v in kwargs.items() if k in allowed_fields}

        if update_data:
            user_ref.update(update_data)
            return True

        return False

    @staticmethod
    def change_password(user_id: str, old_password: str, new_password: str) -> bool:
        """
        Cambia la contraseña de un usuario.

        Args:
            user_id: ID del usuario
            old_password: Contraseña actual
            new_password: Nueva contraseña

        Returns:
            bool: True si se cambió correctamente, False si no
        """
        users_ref = UserService._get_users_ref()
        user_data = users_ref.child(user_id).get()

        if not user_data:
            return False

        # Verificar contraseña actual
        password_hash = user_data.get('password_hash')
        if not password_hash or not UserService._verify_password(old_password, password_hash):
            return False

        # Hashear nueva contraseña
        new_password_hash = UserService._hash_password(new_password)

        # Actualizar en Firebase
        users_ref.child(user_id).update({
            'password_hash': new_password_hash
        })

        return True

    @staticmethod
    def delete_user(user_id: str) -> bool:
        """
        Desactiva un usuario (soft delete).

        Args:
            user_id: ID del usuario

        Returns:
            bool: True si se desactivó, False si no existe
        """
        users_ref = UserService._get_users_ref()
        user_ref = users_ref.child(user_id)

        if not user_ref.get():
            return False

        # Marcar como inactivo en lugar de eliminar
        user_ref.update({'activo': False})
        return True
