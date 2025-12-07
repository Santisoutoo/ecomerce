"""
Script para verificar la configuración de Cloudinary.
"""

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from dotenv import load_dotenv

print("=" * 70)
print("VERIFICACIÓN DE CONFIGURACIÓN DE CLOUDINARY")
print("=" * 70)

# Cargar variables de entorno
load_dotenv()

# Leer variables
cloud_name = os.getenv("CLOUD_NAME")
api_key = os.getenv("API_KEY")
api_secret = os.getenv("API_SECRET")

print(f"\n📦 Variables de entorno:")
print(f"   CLOUD_NAME: {cloud_name}")
print(f"   API_KEY: {api_key}")
print(f"   API_SECRET: {api_secret}")

# Importar cloudinary y verificar configuración
print(f"\n🔧 Importando cloudinary...")
try:
    import cloudinary
    from backend.config.cloudinary_config import upload_image

    print(f"✅ Cloudinary importado correctamente")
    print(f"\n🔍 Configuración actual de Cloudinary:")
    print(f"   cloud_name: {cloudinary.config().cloud_name}")
    print(f"   api_key: {cloudinary.config().api_key}")
    print(f"   api_secret: {'*' * len(str(cloudinary.config().api_secret)) if cloudinary.config().api_secret else 'None'}")
    print(f"   secure: {cloudinary.config().secure}")

except Exception as e:
    print(f"❌ Error al importar cloudinary: {e}")
    import traceback
    traceback.print_exc()

print("\n" + "=" * 70)
