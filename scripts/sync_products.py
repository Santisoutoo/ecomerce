#!/usr/bin/env python3
"""
Script interactivo para sincronizar solo productos con Firebase.
Útil para actualizar solo los productos sin tocar otros datos.
"""

import sys
import json
from pathlib import Path

# Agregar el directorio backend al path
backend_path = Path(__file__).parent.parent / "backend"
sys.path.insert(0, str(backend_path))

from config.firebase_config import get_database


def preview_products(json_path: Path):
    """Muestra un preview de los productos a subir."""
    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    products = data.get('products', [])
    print(f"\n📦 Se encontraron {len(products)} productos:")
    print("=" * 60)

    for i, product in enumerate(products, 1):
        print(f"{i}. {product.get('name', 'Sin nombre')} - {product.get('price', 0)}€")
        print(f"   ID: {product.get('id', 'Sin ID')}")
        print(f"   Categoría: {product.get('category', 'N/A')} | Liga: {product.get('league', 'N/A')}")
        if 'images' in product:
            main_img = product['images'].get('main', '')
            if main_img:
                img_name = main_img.split('/')[-1]
                print(f"   Imagen: {img_name}")
            else:
                print(f"   Imagen: ❌ Sin imagen")
        print()

    print("=" * 60)


def sync_products_to_firebase(json_path: str, confirm: bool = True):
    """
    Sincroniza solo los productos a Firebase.

    Args:
        json_path: Ruta al archivo JSON
        confirm: Si es True, pide confirmación antes de subir
    """
    json_file = Path(json_path)

    if not json_file.exists():
        print(f"❌ Error: No se encontró el archivo {json_path}")
        return False

    # Mostrar preview
    preview_products(json_file)

    # Pedir confirmación
    if confirm:
        response = input("\n¿Deseas subir estos productos a Firebase? (sí/no): ").lower()
        if response not in ['sí', 'si', 's', 'yes', 'y']:
            print("❌ Operación cancelada")
            return False

    # Leer datos
    print("\n🔄 Leyendo archivo JSON...")
    with open(json_file, 'r', encoding='utf-8') as f:
        data = json.load(f)

    products = data.get('products', [])

    if not products:
        print("⚠️  No se encontraron productos en el JSON")
        return False

    # Conectar a Firebase
    print("🔗 Conectando a Firebase...")
    db = get_database()

    # Convertir array de productos a diccionario
    products_dict = {}
    for product in products:
        product_id = product.get('id')
        if product_id:
            products_dict[product_id] = product
        else:
            print(f"⚠️  Producto sin ID encontrado: {product.get('name', 'Sin nombre')}")

    # Subir productos
    print(f"📤 Subiendo {len(products_dict)} productos a Firebase...")
    db.child('products').set(products_dict)

    print("\n✅ ¡Productos sincronizados exitosamente!")
    print(f"📊 Total: {len(products_dict)} productos")
    print(f"🔗 URL: https://sportstyle-store-default-rtdb.firebaseio.com")

    return True


def main():
    """Función principal."""
    default_path = Path(__file__).parent.parent / "data" / "BBDD.json"

    # Filtrar flags de los argumentos
    args = [arg for arg in sys.argv[1:] if not arg.startswith('-')]
    json_path = args[0] if args else str(default_path)

    # Permitir modo sin confirmación con flag --yes
    confirm = '--yes' not in sys.argv and '-y' not in sys.argv

    try:
        success = sync_products_to_firebase(json_path, confirm)
        sys.exit(0 if success else 1)
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
