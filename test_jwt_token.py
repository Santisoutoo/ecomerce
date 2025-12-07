"""
Script para probar la generación y validación de tokens JWT.
"""

import sys
import os
from datetime import timedelta

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from backend.core.security import create_access_token, decode_access_token
from backend.config.settings import SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES

print("=" * 70)
print("PRUEBA DE TOKENS JWT")
print("=" * 70)

# Mostrar configuración
print(f"\n🔑 SECRET_KEY: {SECRET_KEY}")
print(f"🔐 ALGORITHM: {ALGORITHM}")
print(f"⏰ EXPIRE_MINUTES: {ACCESS_TOKEN_EXPIRE_MINUTES}")

# Crear un token de prueba (sub debe ser string)
user_data = {
    "sub": str(1),  # user_id como string (requerido por JWT)
    "email": "test@example.com"
}

print(f"\n📦 Datos del usuario:")
print(f"   user_id (sub): {user_data['sub']} (tipo: {type(user_data['sub']).__name__})")
print(f"   email: {user_data['email']}")

# Generar token
print(f"\n🔨 Generando token...")
token = create_access_token(
    data=user_data,
    expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
)

print(f"✅ Token generado:")
print(f"   {token[:50]}...")

# Decodificar token directamente con jose
print(f"\n🔓 Decodificando token directamente con jose.jwt...")
try:
    from jose import jwt
    payload_direct = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    print(f"✅ Token decodificado directamente:")
    print(f"   sub: {payload_direct.get('sub')} (tipo: {type(payload_direct.get('sub')).__name__})")
    print(f"   email: {payload_direct.get('email')}")
    print(f"   exp: {payload_direct.get('exp')}")
except Exception as e:
    print(f"❌ Error al decodificar directamente: {e}")
    import traceback
    traceback.print_exc()

# Decodificar token usando la función decode_access_token
print(f"\n🔓 Decodificando token con decode_access_token()...")
try:
    payload = decode_access_token(token)
    print(f"✅ Token decodificado exitosamente:")
    print(f"   sub: {payload.get('sub')} (tipo: {type(payload.get('sub')).__name__})")
    print(f"   email: {payload.get('email')}")
    print(f"   exp: {payload.get('exp')}")
except Exception as e:
    print(f"❌ Error al decodificar: {e}")
    import traceback
    traceback.print_exc()

print("\n" + "=" * 70)
