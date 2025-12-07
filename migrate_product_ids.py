"""
Script para migrar los IDs de productos de "prod_001", "prod_002"... a "0", "1", "2"...
ADVERTENCIA: Este script modificará la base de datos de productos.
"""

import sys
import os

# Añadir paths
sys.path.insert(0, os.path.dirname(os.path.abspath('.')))

from backend.config.firebase_config import get_database

print("=" * 70)
print("MIGRACIÓN DE IDS DE PRODUCTOS")
print("=" * 70)

database = get_database()
products_ref = database.child('products')

# Obtener todos los productos actuales
print("\n📦 Obteniendo productos actuales...")
current_products = products_ref.get()

if not current_products:
    print("❌ No hay productos en la base de datos")
    sys.exit(1)

# Convertir a lista si es necesario
if isinstance(current_products, dict):
    products_list = list(current_products.items())
else:
    products_list = list(enumerate(current_products))

print(f"✅ Se encontraron {len(products_list)} productos")

# Mostrar productos actuales
print("\n📋 Productos actuales:")
for old_id, product_data in products_list:
    print(f"   - {old_id}: {product_data.get('name', 'Sin nombre')}")

# Confirmar migración
print("\n" + "=" * 70)
print("⚠️  ADVERTENCIA: Esta operación modificará los IDs de todos los productos")
print("=" * 70)
response = input("\n¿Deseas continuar con la migración? (si/no): ")

if response.lower() not in ['si', 's', 'yes', 'y']:
    print("❌ Migración cancelada")
    sys.exit(0)

# Realizar migración
print("\n🔄 Iniciando migración...")

# 1. Guardar productos con nuevos IDs
new_products = {}
for new_id, (old_id, product_data) in enumerate(products_list):
    # Actualizar el campo 'id' interno
    product_data['id'] = str(new_id)

    # Guardar con nuevo ID
    new_products[str(new_id)] = product_data
    print(f"   ✅ {old_id} → {new_id}: {product_data.get('name')}")

# 2. Eliminar todos los productos antiguos
print("\n🗑️  Eliminando productos antiguos...")
products_ref.delete()

# 3. Guardar productos con nuevos IDs
print("\n💾 Guardando productos con nuevos IDs...")
for new_id, product_data in new_products.items():
    products_ref.child(new_id).set(product_data)

print("\n" + "=" * 70)
print("✅ MIGRACIÓN COMPLETADA EXITOSAMENTE")
print("=" * 70)

# Verificar migración
print("\n🔍 Verificando migración...")
migrated_products = products_ref.get()

if isinstance(migrated_products, dict):
    migrated_list = list(migrated_products.items())
else:
    migrated_list = list(enumerate(migrated_products))

print(f"\n📦 Productos después de la migración:")
for product_id, product_data in migrated_list:
    print(f"   - ID: {product_id}")
    print(f"     Campo 'id': {product_data.get('id')}")
    print(f"     Nombre: {product_data.get('name')}")
    print()

print("=" * 70)
print("RESUMEN")
print("=" * 70)
print(f"""
✅ Migración completada

📊 Estadísticas:
   - Productos migrados: {len(new_products)}
   - IDs antiguos: prod_001, prod_002, prod_003...
   - IDs nuevos: 0, 1, 2, 3...

⚠️  IMPORTANTE:
   - Los carritos existentes pueden tener referencias a IDs antiguos
   - Los favoritos de usuarios pueden tener IDs antiguos
   - Considera vaciar los carritos si hay productos agregados

🔄 Próximos pasos:
   1. Verifica que los productos se muestren correctamente en el frontend
   2. Limpia los carritos de los usuarios si es necesario
   3. Actualiza los favoritos de usuarios si los hay
""")
