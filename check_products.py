"""
Script para verificar el estado actual de los productos en Firebase.
"""

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath('.')))

from backend.config.firebase_config import get_database

print("=" * 70)
print("VERIFICACIÓN DE PRODUCTOS EN FIREBASE")
print("=" * 70)

database = get_database()
products_ref = database.child('products')
products = products_ref.get()

if not products:
    print("\n❌ No hay productos en la base de datos")
    sys.exit(0)

print(f"\n📦 Estructura de datos: {type(products).__name__}")

# Manejar tanto dict como list
if isinstance(products, dict):
    products_list = list(products.items())
else:
    products_list = [(i, p) for i, p in enumerate(products) if p is not None]

print(f"✅ Total de productos: {len(products_list)}\n")

print("📋 Lista de productos:")
for product_id, product_data in products_list:
    if product_data:
        id_interno = product_data.get('id', 'N/A')
        nombre = product_data.get('name', 'Sin nombre')
        print(f"   - Clave: {product_id} (tipo: {type(product_id).__name__})")
        print(f"     Campo 'id': {id_interno} (tipo: {type(id_interno).__name__})")
        print(f"     Nombre: {nombre}")
        print()
