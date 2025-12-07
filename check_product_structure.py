"""
Script para verificar la estructura detallada de los productos en Firebase.
"""

import sys
import os
import json

sys.path.insert(0, os.path.dirname(os.path.abspath('.')))

from backend.config.firebase_config import get_database

print("=" * 70)
print("VERIFICACIÓN DE ESTRUCTURA DE PRODUCTOS")
print("=" * 70)

database = get_database()
products_ref = database.child('products')
products = products_ref.get()

if not products:
    print("\n❌ No hay productos en la base de datos")
    sys.exit(0)

# Verificar el primer producto en detalle
if isinstance(products, dict):
    first_product_id = list(products.keys())[0]
    first_product = products[first_product_id]
elif isinstance(products, list):
    first_product_id = 1
    first_product = products[1] if len(products) > 1 else None
else:
    print("❌ Tipo de datos desconocido")
    sys.exit(1)

print(f"\n📦 Primer producto (ID: {first_product_id}):")
print("=" * 70)
print(json.dumps(first_product, indent=2, ensure_ascii=False))
print("=" * 70)

# Verificar campos clave
required_fields = ['id', 'name', 'price', 'images', 'team', 'sizes', 'category']
print(f"\n🔍 Verificando campos requeridos:")
for field in required_fields:
    if field in first_product:
        print(f"   ✅ {field}: {type(first_product[field]).__name__}")
    else:
        print(f"   ❌ {field}: FALTANTE")
