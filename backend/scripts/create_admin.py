"""
Script para crear un usuario administrador en Firebase.
Ejecuta este script para crear el usuario admin@test.com con privilegios de administrador.
"""

import sys
import os

# Añadir el directorio raíz al path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config.firebase_config import get_auth_client, get_database
from datetime import datetime


def create_admin_user():
    """
    Crea un usuario administrador en Firebase.
    """
    admin_email = "admin@test.com"
    admin_password = "admin123"  # Cambiar por una contraseña segura

    try:
        auth_client = get_auth_client()
        database = get_database()

        # Intentar crear el usuario en Authentication
        try:
            user = auth_client.create_user(
                email=admin_email,
                password=admin_password,
                display_name="Administrador"
            )
            print(f"✅ Usuario creado en Authentication: {user.uid}")
        except Exception as e:
            # Si el usuario ya existe, obtenerlo
            if "EMAIL_EXISTS" in str(e) or "already" in str(e).lower():
                print(f"⚠️ Usuario ya existe en Authentication")
                user = auth_client.get_user_by_email(admin_email)
                print(f"✅ Usuario obtenido: {user.uid}")
            else:
                raise e

        # Crear/actualizar datos en Realtime Database
        user_data = {
            "email": admin_email,
            "nombre": "Admin",
            "apellidos": "Sistema",
            "telefono": "",
            "foto_perfil": "",
            "fecha_registro": datetime.now().isoformat(),
            "puntos_fidelizacion": 0,
            "es_admin": True,  # ⭐ IMPORTANTE: Establecer como admin
            "activo": True,
            "favoritos": [],
            "direccion_envio": {}
        }

        database.child('users').child(user.uid).set(user_data)
        print(f"✅ Datos guardados en Realtime Database")
        print(f"\n🎉 Usuario administrador creado exitosamente!")
        print(f"📧 Email: {admin_email}")
        print(f"🔑 Contraseña: {admin_password}")
        print(f"🆔 UID: {user.uid}")
        print(f"⚙️ es_admin: True")

    except Exception as e:
        print(f"❌ Error al crear usuario administrador: {e}")
        raise


if __name__ == "__main__":
    print("🚀 Creando usuario administrador...")
    print("-" * 50)
    create_admin_user()
    print("-" * 50)
