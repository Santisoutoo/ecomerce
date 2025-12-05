"""Script para verificar información de un usuario en Firebase."""

from backend.config.firebase_config import get_database

# Buscar en Firebase si existe un usuario con este ID
db = get_database()

# Verificar en la colección de usuarios
user_id = 'fZlBToT35rPVcuUg3SO1oTuXwM22'

print(f"🔍 Buscando información para User ID: {user_id}\n")

# Buscar en usuarios
user_data = db.child('users').child(user_id).get()
if user_data:
    print(f'✅ Usuario encontrado en Firebase:')
    print(f'   - User ID: {user_id}')
    for key, value in user_data.items():
        if key != 'password_hash':  # No mostrar contraseña
            print(f'   - {key}: {value}')
else:
    print(f'❌ No se encontró usuario con ID: {user_id}')

# Buscar en carritos
cart_data = db.child('carts').child(user_id).get()
if cart_data:
    print(f'\n🛒 Carrito encontrado:')
    print(f'   - Total items: {cart_data.get("total_items", 0)}')
    print(f'   - Subtotal: €{cart_data.get("subtotal", 0)}')
    items = cart_data.get("items", {})
    print(f'   - Número de items: {len(items)}')

    if items:
        print(f'\n   Items en el carrito:')
        for item_id, item_data in items.items():
            print(f'   - {item_id}:')
            print(f'     * Producto: {item_data.get("product_name")}')
            print(f'     * Cantidad: {item_data.get("quantity")}')
            print(f'     * Talla: {item_data.get("size")}')
            print(f'     * Subtotal: €{item_data.get("subtotal")}')
            pers = item_data.get('personalization')
            if pers:
                nombre = pers.get('nombre', '')
                numero = pers.get('numero', '')
                print(f'     * Personalización: {nombre} #{numero}')
else:
    print(f'\n🛒 No hay carrito para este usuario')

# Buscar en órdenes/pedidos (si existe)
orders_data = db.child('orders').child(user_id).get()
if orders_data:
    print(f'\n📦 Pedidos encontrados: {len(orders_data)}')
else:
    print(f'\n📦 No hay pedidos para este usuario')
