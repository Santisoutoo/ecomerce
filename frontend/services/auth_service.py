"""
Servicio de autenticación para el frontend de Streamlit.
Gestiona las llamadas al backend de autenticación.
"""

import requests
from typing import Tuple, Optional, Dict
from config import AUTH_ENDPOINTS


class AuthService:
    """
    Servicio estático para gestionar autenticación con el backend.
    """

    @staticmethod
    def register(
        email: str,
        password: str,
        nombre: str,
        apellidos: str,
        telefono: Optional[str] = None
    ) -> Tuple[bool, Optional[Dict], Optional[str]]:
        """
        Registra un nuevo usuario en el sistema.

        Args:
            email: Email del usuario
            password: Contraseña
            nombre: Nombre del usuario
            apellidos: Apellidos del usuario
            telefono: Teléfono (opcional)

        Returns:
            Tuple[bool, Optional[Dict], Optional[str]]:
                - success: True si el registro fue exitoso
                - data: Datos de respuesta (token, user_id, etc.)
                - error: Mensaje de error si falló
        """
        try:
            response = requests.post(
                AUTH_ENDPOINTS["signup"],
                json={
                    "email": email,
                    "password": password,
                    "nombre": nombre,
                    "apellidos": apellidos,
                    "telefono": telefono
                },
                timeout=10
            )

            if response.status_code == 201:
                return True, response.json(), None
            else:
                error_detail = response.json().get("detail", "Error en el registro")
                return False, None, error_detail

        except requests.exceptions.ConnectionError:
            return False, None, "No se pudo conectar con el servidor. Verifica que el backend esté ejecutándose."

        except requests.exceptions.Timeout:
            return False, None, "La solicitud excedió el tiempo de espera."

        except Exception as e:
            return False, None, f"Error inesperado: {str(e)}"


    @staticmethod
    def login(email: str, password: str) -> Tuple[bool, Optional[Dict], Optional[str]]:
        """
        Inicia sesión con email y contraseña.

        Args:
            email: Email del usuario
            password: Contraseña

        Returns:
            Tuple[bool, Optional[Dict], Optional[str]]:
                - success: True si el login fue exitoso
                - data: Datos de respuesta (token, user_id, email)
                - error: Mensaje de error si falló
        """
        try:
            response = requests.post(
                AUTH_ENDPOINTS["signin"],
                json={
                    "email": email,
                    "password": password
                },
                timeout=10
            )

            if response.status_code == 200:
                return True, response.json(), None
            elif response.status_code == 401:
                return False, None, "Email o contraseña incorrectos"
            else:
                error_detail = response.json().get("detail", "Error al iniciar sesión")
                return False, None, error_detail

        except requests.exceptions.ConnectionError:
            return False, None, "No se pudo conectar con el servidor. Verifica que el backend esté ejecutándose."

        except requests.exceptions.Timeout:
            return False, None, "La solicitud excedió el tiempo de espera."

        except Exception as e:
            return False, None, f"Error inesperado: {str(e)}"


    @staticmethod
    def get_current_user(access_token: str) -> Tuple[bool, Optional[Dict], Optional[str]]:
        """
        Obtiene los datos del usuario actual usando el token de acceso.

        Args:
            access_token: Token JWT de autenticación

        Returns:
            Tuple[bool, Optional[Dict], Optional[str]]:
                - success: True si se obtuvo el usuario
                - data: Datos del usuario
                - error: Mensaje de error si falló
        """
        try:
            response = requests.get(
                AUTH_ENDPOINTS["me"],
                headers={"Authorization": f"Bearer {access_token}"},
                timeout=10
            )

            if response.status_code == 200:
                return True, response.json(), None
            elif response.status_code == 401:
                return False, None, "Sesión expirada. Por favor, inicia sesión nuevamente."
            else:
                error_detail = response.json().get("detail", "Error al obtener datos del usuario")
                return False, None, error_detail

        except requests.exceptions.ConnectionError:
            return False, None, "No se pudo conectar con el servidor."

        except requests.exceptions.Timeout:
            return False, None, "La solicitud excedió el tiempo de espera."

        except Exception as e:
            return False, None, f"Error inesperado: {str(e)}"


    @staticmethod
    def verify_token(access_token: str) -> bool:
        """
        Verifica si un token de acceso es válido.

        Args:
            access_token: Token JWT de autenticación

        Returns:
            bool: True si el token es válido, False en caso contrario
        """
        try:
            response = requests.post(
                AUTH_ENDPOINTS["verify_token"],
                headers={"Authorization": f"Bearer {access_token}"},
                timeout=5
            )

            return response.status_code == 200

        except Exception:
            return False


    @staticmethod
    def logout(access_token: str) -> Tuple[bool, Optional[str]]:
        """
        Cierra la sesión del usuario.

        Args:
            access_token: Token JWT de autenticación

        Returns:
            Tuple[bool, Optional[str]]:
                - success: True si el logout fue exitoso
                - error: Mensaje de error si falló
        """
        try:
            response = requests.post(
                AUTH_ENDPOINTS["signout"],
                headers={"Authorization": f"Bearer {access_token}"},
                timeout=5
            )

            if response.status_code == 200:
                return True, None
            else:
                return False, "Error al cerrar sesión"

        except Exception as e:
            # Aún si falla la llamada al backend, consideramos el logout exitoso
            # porque el token se eliminará del frontend de todas formas
            return True, None


    @staticmethod
    def upload_profile_picture(image_file, access_token: str) -> Tuple[bool, Optional[str], Optional[str]]:
        """
        Sube una foto de perfil al servidor.

        Args:
            image_file: Archivo de imagen (tipo UploadedFile de streamlit)
            access_token: Token JWT de autenticación

        Returns:
            Tuple[bool, Optional[str], Optional[str]]:
                - success: True si la subida fue exitosa
                - url: URL pública de la imagen
                - error: Mensaje de error si falló
        """
        try:
            files = {"file": (image_file.name, image_file, image_file.type)}

            response = requests.post(
                f"{AUTH_ENDPOINTS['signup'].rsplit('/', 1)[0]}/upload-profile-picture",
                files=files,
                headers={"Authorization": f"Bearer {access_token}"},
                timeout=30
            )

            if response.status_code == 200:
                data = response.json()
                return True, data.get("url"), None
            else:
                error_detail = response.json().get("detail", "Error al subir la imagen")
                return False, None, error_detail

        except requests.exceptions.ConnectionError:
            return False, None, "No se pudo conectar con el servidor."

        except requests.exceptions.Timeout:
            return False, None, "La solicitud excedió el tiempo de espera."

        except Exception as e:
            return False, None, f"Error inesperado: {str(e)}"
