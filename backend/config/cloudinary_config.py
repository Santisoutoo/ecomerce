"""
Configuración de Cloudinary para almacenamiento de imágenes.
"""

import cloudinary
import cloudinary.uploader
import cloudinary.api
import os
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

# Configurar Cloudinary con las credenciales desde .env
cloudinary.config(
    cloud_name=os.getenv("CLOUD_NAME"),
    api_key=os.getenv("API_KEY"),
    api_secret=os.getenv("API_SECRET"),
    secure=True
)


def upload_image(file_content: bytes, folder: str = "profile_pictures", public_id: str = None) -> dict:
    """
    Sube una imagen a Cloudinary.

    Args:
        file_content: Contenido del archivo en bytes
        folder: Carpeta en Cloudinary donde guardar la imagen
        public_id: ID público personalizado (opcional)

    Returns:
        dict: Respuesta de Cloudinary con URL y metadata
    """
    upload_options = {
        "folder": folder,
        "resource_type": "image",
        "overwrite": True,
        "transformation": [
            {"width": 500, "height": 500, "crop": "fill", "gravity": "face"},
            {"quality": "auto"},
            {"fetch_format": "auto"}
        ]
    }

    if public_id:
        upload_options["public_id"] = public_id

    result = cloudinary.uploader.upload(file_content, **upload_options)
    return result


def delete_image(public_id: str) -> dict:
    """
    Elimina una imagen de Cloudinary.

    Args:
        public_id: ID público de la imagen a eliminar

    Returns:
        dict: Resultado de la eliminación
    """
    result = cloudinary.uploader.destroy(public_id)
    return result


def get_cloudinary_url(public_id: str, transformations: dict = None) -> str:
    """
    Genera una URL de Cloudinary con transformaciones opcionales.

    Args:
        public_id: ID público de la imagen
        transformations: Transformaciones a aplicar (opcional)

    Returns:
        str: URL de la imagen
    """
    if transformations:
        return cloudinary.CloudinaryImage(public_id).build_url(**transformations)
    return cloudinary.CloudinaryImage(public_id).build_url()
