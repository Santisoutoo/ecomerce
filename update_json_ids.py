"""
Script para actualizar los IDs en BBDD.json de "prod_XXX" a números enteros.
"""

import json
from pathlib import Path

print("=" * 70)
print("ACTUALIZACIÓN DE IDs EN BBDD.JSON")
print("=" * 70)

# Leer el archivo JSON
json_path = Path("data/BBDD.json")

print(f"\n📖 Leyendo {json_path}...")
with open(json_path, 'r', encoding='utf-8') as f:
    data = json.load(f)

# Actualizar IDs de productos
if 'products' in data and isinstance(data['products'], list):
    print(f"📦 Actualizando {len(data['products'])} productos...")

    for index, product in enumerate(data['products']):
        old_id = product.get('id', 'N/A')
        new_id = index + 1  # Empezar desde 1
        product['id'] = new_id
        print(f"   ✅ {old_id} → {new_id}: {product.get('name', 'Sin nombre')}")

    print(f"\n✅ {len(data['products'])} productos actualizados")
else:
    print("⚠️ No se encontró la sección 'products' o no es una lista")

# Guardar el archivo actualizado
print(f"\n💾 Guardando cambios en {json_path}...")
with open(json_path, 'w', encoding='utf-8') as f:
    json.dump(data, f, indent=2, ensure_ascii=False)

print("\n" + "=" * 70)
print("✅ ARCHIVO JSON ACTUALIZADO EXITOSAMENTE")
print("=" * 70)

print("""
⚠️  IMPORTANTE:
   - El archivo BBDD.json ahora tiene IDs numéricos (1, 2, 3...)
   - Si ejecutas scripts/upload_to_firebase.py, sobrescribirá Firebase
   - Asegúrate de actualizar ese script para que use IDs como strings en Firebase
""")
