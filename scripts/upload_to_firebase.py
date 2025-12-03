#!/usr/bin/env python3
"""
Script para subir los datos del JSON a Firebase Realtime Database.
Uso: python scripts/upload_to_firebase.py
"""

import sys
import json
from pathlib import Path

# Agregar el directorio backend al path
backend_path = Path(__file__).parent.parent / "backend"
sys.path.insert(0, str(backend_path))

from config.firebase_config import get_database


def upload_json_to_firebase(json_file_path: str):
    """
    Lee el archivo JSON y sube los datos a Firebase Realtime Database.

    Args:
        json_file_path: Ruta al archivo JSON con los datos
    """
    print("🔄 Iniciando carga de datos a Firebase...")

    # Leer el archivo JSON
    json_path = Path(json_file_path)
    if not json_path.exists():
        print(f"❌ Error: No se encontró el archivo {json_file_path}")
        return

    print(f"📖 Leyendo datos de {json_path}...")
    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    # Obtener referencia a la base de datos
    print("🔗 Conectando a Firebase Realtime Database...")
    db = get_database()

    # Subir cada colección por separado
    collections = ['products', 'categories', 'leagues', 'users', 'orders', 'cart_items']

    for collection in collections:
        if collection in data:
            print(f"📤 Subiendo {collection}...")

            # Para arrays, crear un diccionario con IDs como claves
            if isinstance(data[collection], list):
                # Convertir array a diccionario usando el ID como clave
                collection_dict = {}
                for item in data[collection]:
                    if 'id' in item:
                        collection_dict[item['id']] = item
                    else:
                        # Si no hay ID, usar el índice
                        collection_dict[f"item_{len(collection_dict)}"] = item

                db.child(collection).set(collection_dict)
                print(f"   ✅ {len(collection_dict)} {collection} subidos")
            else:
                db.child(collection).set(data[collection])
                print(f"   ✅ {collection} subido")
        else:
            print(f"   ⚠️  {collection} no encontrado en el JSON")

    print("\n🎉 ¡Datos subidos exitosamente a Firebase!")
    print(f"🔗 Base de datos: https://sportstyle-store-default-rtdb.europe-west1.firebasedatabase.app")


def main():
    """Función principal del script."""
    # Ruta por defecto al archivo JSON
    default_json_path = Path(__file__).parent.parent / "data" / "BBDD.json"

    # Permitir ruta personalizada como argumento
    json_path = sys.argv[1] if len(sys.argv) > 1 else str(default_json_path)

    try:
        upload_json_to_firebase(json_path)
    except Exception as e:
        print(f"\n❌ Error durante la carga: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
