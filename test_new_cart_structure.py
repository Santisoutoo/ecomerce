"""
Script para probar la nueva estructura del carrito.
Muestra cómo se ve el carrito con product_id como clave y campos simplificados.
"""

import sys
import os

# Añadir paths
sys.path.insert(0, os.path.dirname(os.path.abspath('.')))

from backend.services.cart_service import CartService
from backend.services.user_service import UserService
from backend.models.models import CartItemCreate, Personalization
from backend.config.firebase_config import get_database

print("=" * 70)
print("PRUEBA DE NUEVA ESTRUCTURA DEL CARRITO")
print("=" * 70)

# Crear usuario de prueba
test_email = "cart_test@example.com"
test_password = "test123"

# Limpiar usuario si existe
print("\n📋 Limpiando datos previos...")
existing_user = UserService.get_user_by_email(test_email, include_inactive=True)
if existing_user:
    users_ref = UserService._get_users_ref()
    users_ref.child(str(existing_user['user_id'])).delete()
    print(f"✅ Usuario eliminado: {existing_user['user_id']}")

# Crear usuario
print("\n👤 Creando usuario de prueba...")
user = UserService.create_user(
    email=test_email,
    password=test_password,
    nombre="Test",
    apellidos="Cart"
)
user_id = user['user_id']
print(f"✅ Usuario creado con ID: {user_id}")

# Limpiar carrito si existe
print("\n🛒 Limpiando carrito previo...")
CartService.clear_cart(user_id)
print("✅ Carrito limpiado")

# Añadir items al carrito
print("\n➕ Añadiendo items al carrito...")

# Obtener productos de prueba
database = get_database()
products_ref = database.child('products')
products = products_ref.get()

if not products:
    print("❌ No hay productos en la base de datos")
    sys.exit(1)

# Manejar tanto dict como list - tomar los primeros 2 productos
products_to_test = []
if isinstance(products, dict):
    products_to_test = list(products.items())[:2]
else:
    # Si es lista, filtrar None y tomar los primeros 2
    products_to_test = [(i, p) for i, p in enumerate(products) if p is not None][:2]

for i, (product_id, product_data) in enumerate(products_to_test):

    # Crear item
    personalization = None
    if i == 0:  # Solo el primero con personalización
        personalization = Personalization(nombre="TEST", numero=10)

    item = CartItemCreate(
        product_id=product_id,
        quantity=i + 1,
        size="M" if i == 0 else "L",
        personalization=personalization
    )

    CartService.add_item(user_id, item, product_data, test_email)
    print(f"✅ Item añadido: {product_data['name']} (cantidad: {i+1})")

# Mostrar estructura del carrito en Firebase
print("\n" + "=" * 70)
print("ESTRUCTURA EN FIREBASE")
print("=" * 70)

cart_ref = CartService._get_cart_ref(user_id)
cart_data = cart_ref.get()

print(f"\n📍 Ruta: /carts/{user_id}")
print(f"\n📊 Datos del carrito:")
print(f"   - user_email: {cart_data.get('user_email')}")
print(f"   - total_items: {cart_data.get('total_items')}")
print(f"   - subtotal: €{cart_data.get('subtotal')}")
print(f"   - updated_at: {cart_data.get('updated_at')}")

print(f"\n📦 Items:")
items_dict = cart_data.get('items', {})
# Manejar tanto dict como list
items_to_show = items_dict.items() if isinstance(items_dict, dict) else enumerate(items_dict) if items_dict else []
for product_id, item_data in items_to_show:
    # Saltar elementos None
    if item_data is None:
        continue
    print(f"\n   📍 {product_id}/")
    print(f"      - user_id: {item_data.get('user_id')}")
    print(f"      - size: {item_data.get('size')}")
    print(f"      - quantity: {item_data.get('quantity')}")
    print(f"      - subtotal: €{item_data.get('subtotal')}")
    print(f"      - personalization_price: €{item_data.get('personalization_price', 0.0)}")
    if item_data.get('personalization'):
        print(f"      - personalization: {item_data.get('personalization')}")

# Obtener carrito usando el servicio
print("\n" + "=" * 70)
print("CARRITO RECUPERADO CON DATOS DE PRODUCTOS")
print("=" * 70)

cart = CartService.get_cart(user_id, test_email)

print(f"\n📧 Usuario: {cart.user_email}")
print(f"📊 Total items: {cart.total_items}")
print(f"💰 Subtotal: €{cart.subtotal}")

print(f"\n📦 Items en el carrito:")
for item in cart.items:
    print(f"\n   🏷️ {item.product_name} ({item.team})")
    print(f"      - Product ID: {item.product_id}")
    print(f"      - Size: {item.size}")
    print(f"      - Quantity: {item.quantity}")
    print(f"      - Unit Price: €{item.unit_price}")
    if item.personalization:
        print(f"      - Personalization: {item.personalization.nombre} #{item.personalization.numero}")
        print(f"      - Personalization Price: €{item.personalization_price}")
    print(f"      - Subtotal: €{item.subtotal}")

print("\n" + "=" * 70)
print("VENTAJAS DE LA NUEVA ESTRUCTURA")
print("=" * 70)

print("""
✅ VENTAJAS:
   1. IDs más simples: Se usa el product_id directamente como clave
   2. Sin duplicados: No se puede tener el mismo producto dos veces
   3. Campos mínimos: Solo se guarda size, quantity, subtotal, user_id
   4. Datos actualizados: Los datos del producto se obtienen en tiempo real
   5. Menos espacio: No se duplica información del producto en el carrito
   6. Fácil mantenimiento: Si cambia el precio, se refleja automáticamente

📋 ESTRUCTURA SIMPLIFICADA:
   /carts/{user_id}/
       items/
           {product_id}/        ← ID del producto como clave
               user_id: "0"
               size: "M"
               quantity: 2
               subtotal: 89.98
               personalization_price: 10.0
               personalization: {nombre: "TEST", numero: 10}
       total_items: 3
       subtotal: 179.97
       user_email: "cart_test@example.com"
       updated_at: "2025-12-06T..."

🎯 DATOS QUE SE OBTIENEN DINÁMICAMENTE:
   - product_name (desde /products/{product_id}/name)
   - product_image (desde /products/{product_id}/imagen_url)
   - team (desde /products/{product_id}/equipo)
   - unit_price (desde /products/{product_id}/precio)
""")

print("\n✅ Prueba completada exitosamente!")
