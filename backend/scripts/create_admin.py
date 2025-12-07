"""
Script para crear un usuario administrador en Firebase.
Ejecuta este script para crear el usuario admin@test.com con privilegios de administrador.
"""

import sys
import os

# Añadir el directorio raíz al path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from services.user_service import UserService


def create_admin_user():
    """
    Crea un usuario administrador en Firebase Realtime Database.
    """
    admin_email = "admin@test.com"
    admin_password = "admin123"  # Cambiar por una contraseña segura

    try:
        # Verificar si el usuario ya existe
        existing_user = UserService.get_user_by_email(admin_email, include_inactive=True)

        if existing_user:
            print(f"⚠️ Usuario ya existe con ID: {existing_user['user_id']}")

            # Actualizar para asegurarnos que sea admin y esté activo
            UserService.update_user(
                existing_user['user_id'],
                es_admin=True,
                activo=True
            )
            print(f"✅ Usuario actualizado como administrador")
            print(f"\n🎉 Usuario administrador actualizado exitosamente!")
            print(f"📧 Email: {admin_email}")
            print(f"🔑 Contraseña: {admin_password}")
            print(f"🆔 ID: {existing_user['user_id']}")
            print(f"⚙️ es_admin: True")
        else:
            # Crear nuevo usuario
            user = UserService.create_user(
                email=admin_email,
                password=admin_password,
                nombre="Admin",
                apellidos="Sistema",
                telefono=""
            )

            # Actualizar para establecerlo como admin
            UserService.update_user(user['user_id'], es_admin=True)

            print(f"✅ Usuario administrador creado")
            print(f"\n🎉 Usuario administrador creado exitosamente!")
            print(f"📧 Email: {admin_email}")
            print(f"🔑 Contraseña: {admin_password}")
            print(f"🆔 ID: {user['user_id']}")
            print(f"⚙️ es_admin: True")

    except Exception as e:
        print(f"❌ Error al crear usuario administrador: {e}")
        raise


if __name__ == "__main__":
    print("🚀 Creando usuario administrador...")
    print("-" * 50)
    create_admin_user()
    print("-" * 50)
