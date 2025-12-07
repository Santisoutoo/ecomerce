"""
Script para probar la subida de una imagen de prueba a Cloudinary.
"""

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from backend.config.cloudinary_config import upload_image

print("=" * 70)
print("PRUEBA DE SUBIDA A CLOUDINARY")
print("=" * 70)

# Crear una imagen de prueba (1x1 pixel PNG)
# PNG mínimo válido
test_image_bytes = bytes([
    0x89, 0x50, 0x4E, 0x47, 0x0D, 0x0A, 0x1A, 0x0A,
    0x00, 0x00, 0x00, 0x0D, 0x49, 0x48, 0x44, 0x52,
    0x00, 0x00, 0x00, 0x01, 0x00, 0x00, 0x00, 0x01,
    0x08, 0x06, 0x00, 0x00, 0x00, 0x1F, 0x15, 0xC4,
    0x89, 0x00, 0x00, 0x00, 0x0A, 0x49, 0x44, 0x41,
    0x54, 0x78, 0x9C, 0x63, 0x00, 0x01, 0x00, 0x00,
    0x05, 0x00, 0x01, 0x0D, 0x0A, 0x2D, 0xB4, 0x00,
    0x00, 0x00, 0x00, 0x49, 0x45, 0x4E, 0x44, 0xAE,
    0x42, 0x60, 0x82
])

print(f"\n📸 Imagen de prueba:")
print(f"   Tamaño: {len(test_image_bytes)} bytes")

print(f"\n☁️  Subiendo imagen a Cloudinary...")
try:
    result = upload_image(
        file_content=test_image_bytes,
        folder="test",
        public_id="test_image"
    )

    print(f"✅ Imagen subida exitosamente:")
    print(f"   URL: {result.get('secure_url') or result.get('url')}")
    print(f"   Public ID: {result.get('public_id')}")
    print(f"   Width: {result.get('width')}")
    print(f"   Height: {result.get('height')}")
    print(f"   Format: {result.get('format')}")

except Exception as e:
    print(f"❌ Error al subir imagen: {e}")
    import traceback
    traceback.print_exc()

print("\n" + "=" * 70)
