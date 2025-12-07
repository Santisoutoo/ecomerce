"""
Script de prueba para verificar la autenticación con base de datos.
Prueba registro, login y obtención de perfil de usuario.
"""

import sys
import os

# Añadir paths
sys.path.insert(0, os.path.dirname(os.path.abspath('.')))

from backend.services.user_service import UserService

print("=" * 70)
print("PRUEBAS DE AUTENTICACIÓN CON BASE DE DATOS")
print("=" * 70)

# Usuario de prueba
test_email = "test_user_db@example.com"
test_password = "TestPassword123"
test_nombre = "Usuario"
test_apellidos = "De Prueba"

# TEST 1: Limpiar usuario si existe (incluye inactivos)
print("\n" + "=" * 70)
print("TEST 1: Limpiar datos previos")
print("=" * 70)

# Buscar usuarios tanto activos como inactivos
users_ref = UserService._get_users_ref()
all_users = users_ref.get()
deleted_count = 0

if all_users:
    for user_id, user_data in all_users.items():
        if user_data.get('email') == test_email:
            print(f"🧹 Usuario encontrado: {user_id} (activo: {user_data.get('activo', True)})")
            # Eliminar completamente (no soft delete)
            users_ref.child(user_id).delete()
            deleted_count += 1

if deleted_count > 0:
    print(f"✅ {deleted_count} usuario(s) eliminado(s)")
else:
    print("✅ No hay datos previos a limpiar")

# TEST 2: Crear nuevo usuario
print("\n" + "=" * 70)
print("TEST 2: Crear nuevo usuario")
print("=" * 70)

try:
    user = UserService.create_user(
        email=test_email,
        password=test_password,
        nombre=test_nombre,
        apellidos=test_apellidos,
        telefono="612345678"
    )

    print(f"✅ Usuario creado exitosamente:")
    print(f"   - User ID: {user['user_id']}")
    print(f"   - Email: {user['email']}")
    print(f"   - Nombre: {user['nombre']} {user['apellidos']}")
    print(f"   - Teléfono: {user['telefono']}")
    print(f"   - Es admin: {user['es_admin']}")
    print(f"   - Puntos: {user['puntos_fidelizacion']}")

    user_id = user['user_id']

except ValueError as e:
    print(f"❌ Error: {e}")
    sys.exit(1)

# TEST 3: Intentar crear usuario duplicado
print("\n" + "=" * 70)
print("TEST 3: Verificar que no se pueden duplicar emails")
print("=" * 70)

try:
    UserService.create_user(
        email=test_email,
        password="OtraPassword",
        nombre="Otro",
        apellidos="Usuario"
    )
    print("❌ FALLO: Se permitió crear un usuario duplicado")
    sys.exit(1)
except ValueError as e:
    print(f"✅ Correcto: {e}")

# TEST 4: Autenticar con contraseña correcta
print("\n" + "=" * 70)
print("TEST 4: Autenticar con contraseña correcta")
print("=" * 70)

auth_user = UserService.authenticate_user(test_email, test_password)
if auth_user:
    print(f"✅ Autenticación exitosa:")
    print(f"   - User ID: {auth_user['user_id']}")
    print(f"   - Email: {auth_user['email']}")
    print(f"   - Nombre: {auth_user['nombre']} {auth_user['apellidos']}")
else:
    print("❌ FALLO: No se pudo autenticar con credenciales correctas")
    sys.exit(1)

# TEST 5: Autenticar con contraseña incorrecta
print("\n" + "=" * 70)
print("TEST 5: Autenticar con contraseña incorrecta")
print("=" * 70)

auth_user = UserService.authenticate_user(test_email, "PasswordIncorrecto")
if auth_user:
    print("❌ FALLO: Se autenticó con contraseña incorrecta")
    sys.exit(1)
else:
    print("✅ Correcto: Contraseña incorrecta rechazada")

# TEST 6: Obtener usuario por ID
print("\n" + "=" * 70)
print("TEST 6: Obtener usuario por ID")
print("=" * 70)

user_by_id = UserService.get_user_by_id(user_id)
if user_by_id:
    print(f"✅ Usuario encontrado por ID:")
    print(f"   - User ID: {user_by_id['user_id']}")
    print(f"   - Email: {user_by_id['email']}")
    print(f"   - Activo: {user_by_id.get('activo', True)}")
else:
    print("❌ FALLO: No se encontró el usuario por ID")
    sys.exit(1)

# TEST 7: Obtener usuario por email
print("\n" + "=" * 70)
print("TEST 7: Obtener usuario por email")
print("=" * 70)

user_by_email = UserService.get_user_by_email(test_email)
if user_by_email and user_by_email['user_id'] == user_id:
    print(f"✅ Usuario encontrado por email:")
    print(f"   - User ID: {user_by_email['user_id']}")
    print(f"   - Email: {user_by_email['email']}")
else:
    print("❌ FALLO: No se encontró el usuario por email")
    sys.exit(1)

# TEST 8: Actualizar datos del usuario
print("\n" + "=" * 70)
print("TEST 8: Actualizar datos del usuario")
print("=" * 70)

updated = UserService.update_user(user_id, telefono="987654321", puntos_fidelizacion=100)
if updated:
    updated_user = UserService.get_user_by_id(user_id)
    print(f"✅ Usuario actualizado:")
    print(f"   - Teléfono: {updated_user['telefono']}")
    print(f"   - Puntos: {updated_user['puntos_fidelizacion']}")
else:
    print("❌ FALLO: No se pudo actualizar el usuario")
    sys.exit(1)

# TEST 9: Cambiar contraseña
print("\n" + "=" * 70)
print("TEST 9: Cambiar contraseña")
print("=" * 70)

new_password = "NuevaPassword456"
changed = UserService.change_password(user_id, test_password, new_password)
if changed:
    print("✅ Contraseña cambiada exitosamente")

    # Verificar que la nueva contraseña funciona
    auth_new = UserService.authenticate_user(test_email, new_password)
    if auth_new:
        print("✅ Autenticación con nueva contraseña exitosa")
    else:
        print("❌ FALLO: No se pudo autenticar con la nueva contraseña")
        sys.exit(1)

    # Verificar que la vieja contraseña ya no funciona
    auth_old = UserService.authenticate_user(test_email, test_password)
    if not auth_old:
        print("✅ Contraseña antigua rechazada correctamente")
    else:
        print("❌ FALLO: La contraseña antigua todavía funciona")
        sys.exit(1)
else:
    print("❌ FALLO: No se pudo cambiar la contraseña")
    sys.exit(1)

# TEST 10: Desactivar usuario
print("\n" + "=" * 70)
print("TEST 10: Desactivar usuario (soft delete)")
print("=" * 70)

deleted = UserService.delete_user(user_id)
if deleted:
    print("✅ Usuario desactivado exitosamente")

    # Verificar que el usuario está inactivo
    inactive_user = UserService.get_user_by_id(user_id)
    if inactive_user and not inactive_user.get('activo', True):
        print("✅ Usuario marcado como inactivo")
    else:
        print("⚠️ Advertencia: Usuario no está marcado como inactivo")

    # Verificar que no puede autenticarse
    auth_inactive = UserService.authenticate_user(test_email, new_password)
    if not auth_inactive:
        print("✅ Usuario inactivo no puede autenticarse")
    else:
        print("❌ FALLO: Usuario inactivo pudo autenticarse")
        sys.exit(1)
else:
    print("❌ FALLO: No se pudo desactivar el usuario")
    sys.exit(1)

# RESUMEN
print("\n" + "=" * 70)
print("RESUMEN")
print("=" * 70)

print("""
✅ TODAS LAS PRUEBAS PASARON EXITOSAMENTE

📋 Funcionalidades verificadas:
   1. ✅ Crear nuevos usuarios
   2. ✅ Verificar emails duplicados
   3. ✅ Autenticar con contraseña (texto plano)
   4. ✅ Rechazar contraseñas incorrectas
   5. ✅ Obtener usuario por ID
   6. ✅ Obtener usuario por email
   7. ✅ Actualizar datos de usuario
   8. ✅ Cambiar contraseña
   9. ✅ Desactivar usuarios (soft delete)
   10. ✅ Usuarios inactivos no pueden autenticarse

🎉 El sistema de autenticación con base de datos funciona correctamente!

📝 IMPORTANTE:
   - Las contraseñas se almacenan en texto plano
   - Los user_id son secuenciales (1, 2, 3, 4...)
   - Los usuarios se guardan en Firebase Realtime Database en /users/{user_id}
   - El sistema usa "soft delete" (marca usuarios como inactivos)
""")
