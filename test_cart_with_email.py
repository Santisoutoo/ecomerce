"""
Script de prueba para verificar que el email del usuario se guarda en el carrito.
"""

import sys
import os

# Añadir paths
sys.path.insert(0, os.path.dirname(os.path.abspath('.')))

from backend.services.cart_service import CartService
from backend.models.models import CartItemCreate, Personalization
from backend.config.firebase_config import get_database

# Datos del usuario
user_id = "fZlBToT35rPVcuUg3SO1oTuXwM22"
user_email = "hola@gmail.com"

# Producto de prueba
test_product = {
    'id': 'prod_001',
    'name': 'Camiseta FC Barcelona',
    'precio': 89.99,
    'imagen_url': 'https://res.cloudinary.com/dlrrvenn1/image/upload/v1764772154/camiseta_barcelona_lgranp.jpg',
    'equipo': 'Barcelona',
    'precio_personalizacion': 10.0
}

print("=" * 60)
print("TEST: Verificar email en carrito de Firebase")
print("=" * 60)

# Limpiar carrito existente
print(f"\n🧹 Limpiando carrito de {user_email}...")
CartService.clear_cart(user_id)

# Crear item
print(f"\n🔄 Añadiendo item al carrito con email...")
item = CartItemCreate(
    product_id='prod_001',
    quantity=1,
    size='M',
    personalization=Personalization(nombre='MESSI', numero=10)
)

# Añadir a Firebase CON email
added = CartService.add_item(user_id, item, test_product, user_email)
print(f"✅ Item añadido: {added.id}")

# Verificar en Firebase directamente
print(f"\n🔍 Verificando datos en Firebase...")
db = get_database()
cart_data = db.child('carts').child(user_id).get()

if cart_data:
    print(f"\n✅ Carrito encontrado en Firebase:")
    print(f"   📧 user_email: {cart_data.get('user_email', '❌ NO ENCONTRADO')}")
    print(f"   🆔 user_id: {user_id}")
    print(f"   📦 Total items: {cart_data.get('total_items')}")
    print(f"   💰 Subtotal: €{cart_data.get('subtotal')}")

    # Verificar items
    items = cart_data.get('items', {})
    print(f"\n   Items en carrito:")
    for item_id, item_data in items.items():
        print(f"   - {item_id}:")
        print(f"     * Producto: {item_data.get('product_name')}")
        print(f"     * Equipo: {item_data.get('team')}")
        pers = item_data.get('personalization')
        if pers:
            print(f"     * Personalización: {pers.get('nombre')} #{pers.get('numero')}")

    # Verificar que el email está presente
    if cart_data.get('user_email') == user_email:
        print(f"\n🎉 ÉXITO: El email '{user_email}' se guardó correctamente en el carrito")
    else:
        print(f"\n❌ ERROR: El email no coincide o no está presente")
        print(f"   Esperado: {user_email}")
        print(f"   Encontrado: {cart_data.get('user_email')}")
else:
    print(f"❌ No se encontró el carrito en Firebase")

# Limpiar
print(f"\n🧹 Limpiando carrito de prueba...")
CartService.clear_cart(user_id)
print("✅ Limpieza completada")
