"""
Script para convertir los IDs de productos y usuarios de string a int en el campo 'id'.
Nota: Las claves en Firebase seguirán siendo strings, pero el valor del campo 'id' será int.
"""

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath('.')))

from backend.config.firebase_config import get_database

print("=" * 70)
print("CONVERSIÓN DE IDs A TIPO INT")
print("=" * 70)

database = get_database()

# Convertir IDs de productos
print("\n📦 Convirtiendo IDs de productos...")
products_ref = database.child('products')
products = products_ref.get()

if products:
    count = 0
    if isinstance(products, dict):
        for product_id, product_data in products.items():
            if product_data and 'id' in product_data:
                # Convertir el campo 'id' a int
                current_id = product_data['id']
                if isinstance(current_id, str):
                    product_data['id'] = int(current_id)
                    products_ref.child(product_id).update({'id': int(current_id)})
                    count += 1
                    print(f"   ✅ Producto {product_id}: id '{current_id}' (str) → {int(current_id)} (int)")
    else:
        for i, product_data in enumerate(products):
            if product_data and 'id' in product_data:
                current_id = product_data['id']
                if isinstance(current_id, str):
                    product_data['id'] = int(current_id)
                    products_ref.child(i).update({'id': int(current_id)})
                    count += 1
                    print(f"   ✅ Producto {i}: id '{current_id}' (str) → {int(current_id)} (int)")

    print(f"\n✅ {count} productos actualizados")
else:
    print("   ⚠️ No hay productos")

# Convertir IDs de usuarios
print("\n👤 Convirtiendo IDs de usuarios...")
users_ref = database.child('users')
users = users_ref.get()

if users:
    # Los usuarios no tienen un campo 'id' interno, solo la clave
    # Pero podemos verificar la estructura
    if isinstance(users, dict):
        print(f"   📊 {len(users)} usuarios encontrados (claves como dict)")
        print(f"   ℹ️ Las claves ya son tratadas como int en el código")
    else:
        print(f"   📊 {len(users)} usuarios encontrados (almacenados como lista)")
        print(f"   ℹ️ Firebase convertirá claves numéricas a lista automáticamente")
else:
    print("   ⚠️ No hay usuarios")

print("\n" + "=" * 70)
print("✅ CONVERSIÓN COMPLETADA")
print("=" * 70)

# Verificar
print("\n🔍 Verificando conversión...")
products = products_ref.get()
if products:
    if isinstance(products, dict):
        sample = list(products.items())[:3]
    else:
        sample = [(i, p) for i, p in enumerate(products) if p is not None][:3]

    print("\n📦 Muestra de productos:")
    for prod_id, prod_data in sample:
        if prod_data:
            print(f"   - Clave: {prod_id} (tipo: {type(prod_id).__name__})")
            print(f"     Campo 'id': {prod_data.get('id')} (tipo: {type(prod_data.get('id')).__name__})")
            print(f"     Nombre: {prod_data.get('name')}")
            print()

print("=" * 70)
print("📊 RESUMEN")
print("=" * 70)
print("""
✅ Conversión completada

🔑 Estructura de IDs:
   - Claves en Firebase: Siempre strings (requerido por Firebase)
   - Campo 'id' en productos: Ahora son int
   - user_id en código: Se manejan como int

📋 Ejemplo de producto:
   /products/
       "1"/              ← Clave (string, requerido por Firebase)
           id: 1         ← Campo (int)
           name: "..."
           price: 89.99

💡 IMPORTANTE:
   - El código ya está preparado para manejar IDs como int
   - Firebase requiere claves como string, pero los valores pueden ser int
   - Todos los métodos convierten automáticamente entre str e int según sea necesario
""")
