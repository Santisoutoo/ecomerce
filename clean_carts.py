"""
Script para limpiar todos los carritos después de la migración de IDs de productos.
"""

import sys
import os

# Añadir paths
sys.path.insert(0, os.path.dirname(os.path.abspath('.')))

from backend.config.firebase_config import get_database

print("=" * 70)
print("LIMPIEZA DE CARRITOS")
print("=" * 70)

database = get_database()
carts_ref = database.child('carts')

# Obtener todos los carritos
print("\n🛒 Obteniendo carritos...")
all_carts = carts_ref.get()

if not all_carts:
    print("✅ No hay carritos para limpiar")
    sys.exit(0)

# Contar carritos
if isinstance(all_carts, dict):
    cart_count = len(all_carts)
    cart_items = list(all_carts.items())
else:
    cart_count = len(all_carts)
    cart_items = list(enumerate(all_carts))

print(f"📊 Se encontraron {cart_count} carrito(s)")

# Mostrar carritos
for user_id, cart_data in cart_items:
    items_count = 0
    if cart_data and 'items' in cart_data:
        items_dict = cart_data.get('items', {})
        if isinstance(items_dict, dict):
            items_count = len(items_dict)
        else:
            items_count = len(items_dict) if items_dict else 0

    print(f"   - Usuario {user_id}: {items_count} item(s)")

# Confirmar limpieza
print("\n⚠️  ¿Deseas limpiar todos los carritos? (si/no): ", end="")
response = input()

if response.lower() not in ['si', 's', 'yes', 'y']:
    print("❌ Limpieza cancelada")
    sys.exit(0)

# Limpiar carritos
print("\n🧹 Limpiando carritos...")
carts_ref.delete()

print("\n✅ Todos los carritos han sido limpiados")
print("=" * 70)
