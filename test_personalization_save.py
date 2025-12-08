"""
Script de prueba para verificar que la personalización se guarda correctamente en Firebase.
"""
import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from backend.services.cart_service import CartService
from backend.models.models import CartItemCreate, Personalization

# ID de usuario de prueba
TEST_USER_ID = "test_user_123"
TEST_EMAIL = "test@example.com"

def test_add_item_with_personalization():
    """Prueba añadir un item con personalización al carrito."""

    print("🧪 Iniciando prueba de personalización...")

    # Limpiar carrito de prueba primero
    print(f"\n1️⃣ Limpiando carrito de {TEST_USER_ID}...")
    CartService.clear_cart(TEST_USER_ID)

    # Obtener datos de un producto (producto ID 2)
    print("\n2️⃣ Obteniendo datos del producto ID 2...")
    product_data = CartService._get_product_data(2)
    if not product_data:
        print("❌ Error: Producto no encontrado")
        return

    print(f"✅ Producto encontrado: {product_data.get('name')}")

    # Crear personalización con nombre y número
    personalization = Personalization(
        nombre="MESSI",
        numero=10
    )

    print(f"\n3️⃣ Creando personalización:")
    print(f"   - Nombre: {personalization.nombre}")
    print(f"   - Número: {personalization.numero}")
    print(f"   - Dict: {personalization.dict()}")

    # Crear item del carrito
    item_create = CartItemCreate(
        product_id=2,
        quantity=1,
        size="M",
        personalization=personalization
    )

    print(f"\n4️⃣ Añadiendo item al carrito con personalización...")
    result = CartService.add_item(TEST_USER_ID, item_create, product_data, TEST_EMAIL)

    print(f"\n✅ Item añadido:")
    print(f"   - ID del item: {result.id}")
    print(f"   - Producto: {result.product_name}")
    print(f"   - Talla: {result.size}")
    print(f"   - Precio personalización: €{result.personalization_price}")
    print(f"   - Personalización:")
    if result.personalization:
        print(f"     * Nombre: {result.personalization.nombre}")
        print(f"     * Número: {result.personalization.numero}")
    else:
        print("     ❌ No hay personalización guardada!")

    # Verificar leyendo el carrito
    print(f"\n5️⃣ Verificando lectura del carrito...")
    cart = CartService.get_cart(TEST_USER_ID, TEST_EMAIL)

    print(f"\n📦 Carrito recuperado:")
    print(f"   - Total items: {cart.total_items}")
    print(f"   - Subtotal: €{cart.subtotal}")

    if cart.items:
        for item in cart.items:
            print(f"\n   📝 Item {item.id}:")
            print(f"      - Producto: {item.product_name}")
            print(f"      - Cantidad: {item.quantity}")
            print(f"      - Talla: {item.size}")
            print(f"      - Precio unit: €{item.unit_price}")
            print(f"      - Precio personalización: €{item.personalization_price}")
            if item.personalization:
                print(f"      - Personalización:")
                print(f"        * Nombre: {item.personalization.nombre}")
                print(f"        * Número: {item.personalization.numero}")
            else:
                print(f"      - ❌ Personalización: No guardada")
            print(f"      - Subtotal: €{item.subtotal}")

    # Verificar directamente en Firebase
    print(f"\n6️⃣ Verificando datos RAW en Firebase...")
    from backend.config.firebase_config import get_database
    database = get_database()
    cart_ref = database.child('carts').child(TEST_USER_ID)
    raw_cart_data = cart_ref.get()

    if raw_cart_data and 'items' in raw_cart_data:
        print("\n📊 Datos RAW en Firebase:")
        import json
        print(json.dumps(raw_cart_data['items'], indent=2, ensure_ascii=False))

    print("\n✅ Prueba completada!")

if __name__ == "__main__":
    test_add_item_with_personalization()
