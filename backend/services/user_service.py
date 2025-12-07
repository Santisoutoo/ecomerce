"""
Servicio de usuarios con Firebase Realtime Database.
Gestiona autenticación, registro y operaciones de usuarios SIN Firebase Authentication.
"""

from typing import Optional
from datetime import datetime
from firebase_admin import db
from backend.config.firebase_config import get_database


class UserService:
    """
    Servicio para gestionar usuarios en Firebase Realtime Database.

    Estructura en Firebase:
    /users/
        {user_id}/
            email: str
            password: str  # Contraseña en texto plano
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
    def _generate_user_id() -> int:
        """
        Genera un ID secuencial para el usuario (1, 2, 3, 4...).

        Returns:
            int: ID secuencial del usuario
        """
        users_ref = UserService._get_users_ref()
        all_users = users_ref.get()

        if not all_users:
            return 1

        # Si es una lista, el siguiente ID es el largo de la lista
        if isinstance(all_users, list):
            # Contar elementos no-None
            count = sum(1 for item in all_users if item is not None)
            return count + 1

        # Si es un diccionario, obtener todos los IDs numéricos y encontrar el máximo
        numeric_ids = []
        for user_id in all_users.keys():
            try:
                numeric_ids.append(int(user_id))
            except ValueError:
                # Ignorar IDs no numéricos (por si hay datos legacy)
                continue

        if not numeric_ids:
            return 1

        # Retornar el siguiente ID
        return max(numeric_ids) + 1

    @staticmethod
    def _verify_password(password: str, stored_password: str) -> bool:
        """
        Verifica si una contraseña coincide con la almacenada.

        Args:
            password: Contraseña ingresada
            stored_password: Contraseña almacenada

        Returns:
            bool: True si coincide, False si no
        """
        return password == stored_password

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
        Verifica si un email ya está registrado por un usuario activo.

        Args:
            email: Email a verificar

        Returns:
            bool: True si existe y está activo, False si no
        """
        users_ref = UserService._get_users_ref()
        all_users = users_ref.get()

        if not all_users:
            return False

        # Manejar tanto dict como list
        users_values = all_users.values() if isinstance(all_users, dict) else all_users

        # Buscar email solo en usuarios activos
        for user_data in users_values:
            # Saltar elementos None (pueden aparecer cuando Firebase convierte claves numéricas a lista)
            if user_data is None:
                continue
            if user_data.get('email') == email and user_data.get('activo', True):
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

        # Generar ID único secuencial
        user_id = UserService._generate_user_id()

        # Preparar datos del usuario
        user_data = {
            "id": user_id,  # ID como int
            "email": email,
            "password": password,  # Contraseña en texto plano
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

        # Guardar en Firebase (convertir ID a string para Firebase)
        users_ref = UserService._get_users_ref()
        users_ref.child(str(user_id)).set(user_data)

        # Retornar datos sin el password
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

        # Manejar tanto dict como list
        users_to_check = all_users.items() if isinstance(all_users, dict) else enumerate(all_users)

        # Buscar usuario por email
        for user_id, user_data in users_to_check:
            # Saltar elementos None (pueden aparecer cuando Firebase convierte claves numéricas a lista)
            if user_data is None:
                continue
            if user_data.get('email') == email:
                # Verificar que el usuario esté activo
                if not user_data.get('activo', True):
                    return None

                # Verificar contraseña
                stored_password = user_data.get('password')
                if stored_password and UserService._verify_password(password, stored_password):
                    # Convertir user_id a int si es necesario
                    user_id_int = int(user_id) if isinstance(user_id, str) else user_id

                    # Retornar datos del usuario (sin password)
                    return {
                        "user_id": user_id_int,
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
    def get_user_by_id(user_id) -> Optional[dict]:
        """
        Obtiene un usuario por su ID.

        Args:
            user_id: ID del usuario (int o str)

        Returns:
            Optional[dict]: Datos del usuario (sin password) si existe, None si no
        """
        users_ref = UserService._get_users_ref()
        user_data = users_ref.child(str(user_id)).get()

        if not user_data:
            return None

        # Convertir a int si es necesario
        user_id_int = int(user_id) if isinstance(user_id, str) else user_id

        # Retornar datos sin password
        return {
            "user_id": user_id_int,
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
    def get_user_by_email(email: str, include_inactive: bool = False) -> Optional[dict]:
        """
        Obtiene un usuario por su email.

        Args:
            email: Email del usuario
            include_inactive: Si True, incluye usuarios inactivos. Por defecto solo activos.

        Returns:
            Optional[dict]: Datos del usuario si existe, None si no
        """
        users_ref = UserService._get_users_ref()
        all_users = users_ref.get()

        if not all_users:
            return None

        # Manejar tanto dict como list
        users_to_check = all_users.items() if isinstance(all_users, dict) else enumerate(all_users)

        # Buscar usuario por email (solo activos por defecto)
        for user_id, user_data in users_to_check:
            # Saltar elementos None (pueden aparecer cuando Firebase convierte claves numéricas a lista)
            if user_data is None:
                continue
            if user_data.get('email') == email:
                # Si no incluimos inactivos, verificar que esté activo
                if not include_inactive and not user_data.get('activo', True):
                    continue

                return {
                    "user_id": int(user_id) if isinstance(user_id, str) else user_id,
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
    def update_user(user_id, **kwargs) -> bool:
        """
        Actualiza los datos de un usuario.

        Args:
            user_id: ID del usuario
            **kwargs: Campos a actualizar

        Returns:
            bool: True si se actualizó, False si el usuario no existe
        """
        users_ref = UserService._get_users_ref()
        user_ref = users_ref.child(str(user_id))

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
    def change_password(user_id, old_password: str, new_password: str) -> bool:
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
        user_data = users_ref.child(str(user_id)).get()

        if not user_data:
            return False

        # Verificar contraseña actual
        stored_password = user_data.get('password')
        if not stored_password or not UserService._verify_password(old_password, stored_password):
            return False

        # Actualizar en Firebase con nueva contraseña
        users_ref.child(str(user_id)).update({
            'password': new_password
        })

        return True

    @staticmethod
    def delete_user(user_id) -> bool:
        """
        Desactiva un usuario (soft delete).

        Args:
            user_id: ID del usuario

        Returns:
            bool: True si se desactivó, False si no existe
        """
        users_ref = UserService._get_users_ref()
        user_ref = users_ref.child(str(user_id))

        if not user_ref.get():
            return False

        # Marcar como inactivo en lugar de eliminar
        user_ref.update({'activo': False})
        return True
