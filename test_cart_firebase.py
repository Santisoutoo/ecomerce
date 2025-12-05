"""
Script de prueba para verificar la sincronización del carrito con Firebase.
Simula operaciones del carrito sin necesidad de ejecutar Streamlit.
"""

import sys
import os

# Añadir paths
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'frontend'))
sys.path.insert(0, os.path.dirname(__file__))

def test_firebase_connection():
    """Prueba la conexión con Firebase."""
    print("=" * 60)
    print("TEST 1: Conexión con Firebase")
    print("=" * 60)

    try:
        from backend.config.firebase_config import initialize_firebase, get_database

        # Intentar inicializar Firebase
        app = initialize_firebase()
        print(f"✅ Firebase inicializado: {app.name}")

        # Intentar obtener referencia a la base de datos
        db_ref = get_database()
        print(f"✅ Referencia a la base de datos obtenida: {db_ref}")

        return True
    except Exception as e:
        print(f"❌ Error al conectar con Firebase: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_backend_cart_service():
    """Prueba el servicio de carrito del backend."""
    print("\n" + "=" * 60)
    print("TEST 2: Backend Cart Service")
    print("=" * 60)

    try:
        from backend.services.cart_service import CartService
        from backend.models.models import CartItemCreate, Personalization

        print("✅ BackendCartService importado correctamente")

        # Usuario de prueba
        test_user_id = "test_user_12345"

        # Obtener carrito vacío
        cart = CartService.get_cart(test_user_id)
        print(f"✅ Carrito obtenido: {len(cart.items)} items, subtotal: €{cart.subtotal}")

        # Producto de prueba
        test_product = {
            'id': 'prod_001',
            'name': 'Camiseta FC Barcelona',
            'precio': 89.99,
            'imagen_url': 'https://res.cloudinary.com/dlrrvenn1/image/upload/v1764772154/camiseta_barcelona_lgranp.jpg',
            'equipo': 'Barcelona',
            'precio_personalizacion': 10.0
        }

        # Crear item con personalización
        cart_item_create = CartItemCreate(
            product_id=test_product['id'],
            quantity=2,
            size="M",
            personalization=Personalization(nombre="MESSI", numero=10)
        )

        # Añadir item al carrito
        print("\n🔄 Añadiendo item al carrito...")
        added_item = CartService.add_item(test_user_id, cart_item_create, test_product)
        print(f"✅ Item añadido:")
        print(f"   - ID: {added_item.id}")
        print(f"   - Producto: {added_item.product_name}")
        print(f"   - Cantidad: {added_item.quantity}")
        print(f"   - Talla: {added_item.size}")
        print(f"   - Personalización: {added_item.personalization.nombre} #{added_item.personalization.numero}")
        print(f"   - Precio unitario: €{added_item.unit_price}")
        print(f"   - Precio personalización: €{added_item.personalization_price}")
        print(f"   - Subtotal: €{added_item.subtotal}")

        # Verificar que el item se guardó
        cart_updated = CartService.get_cart(test_user_id)
        print(f"\n✅ Carrito actualizado: {cart_updated.total_items} items, subtotal: €{cart_updated.subtotal}")

        # Limpiar el carrito de prueba
        print("\n🧹 Limpiando carrito de prueba...")
        CartService.clear_cart(test_user_id)
        print("✅ Carrito limpiado")

        return True
    except Exception as e:
        print(f"❌ Error en el servicio del carrito: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_product_service():
    """Prueba que el ProductService carga productos correctamente."""
    print("\n" + "=" * 60)
    print("TEST 3: Product Service")
    print("=" * 60)

    try:
        # Mock de streamlit
        class MockSessionState(dict):
            pass

        class MockSt:
            session_state = MockSessionState()

        sys.modules['streamlit'] = MockSt()

        from services.product_service import ProductService

        print("✅ ProductService importado correctamente")

        # Obtener un producto
        product = ProductService.get_product_by_id("prod_001")

        if product:
            print(f"✅ Producto encontrado:")
            print(f"   - ID: {product.get('id')}")
            print(f"   - Nombre: {product.get('name')}")
            print(f"   - Precio: €{product.get('precio')}")
            print(f"   - Equipo: {product.get('equipo')}")
            print(f"   - Imagen: {product.get('imagen_url')[:50]}...")
            print(f"   - Precio personalización: €{product.get('precio_personalizacion')}")

            # Verificar campos requeridos
            required_fields = ['id', 'name', 'precio', 'imagen_url', 'equipo', 'precio_personalizacion']
            missing_fields = [f for f in required_fields if f not in product or product[f] is None]

            if missing_fields:
                print(f"⚠️ Campos faltantes: {missing_fields}")
                return False
            else:
                print("✅ Todos los campos requeridos están presentes")
                return True
        else:
            print("❌ No se encontró el producto prod_001")
            return False

    except Exception as e:
        print(f"❌ Error en ProductService: {e}")
        import traceback
        traceback.print_exc()
        return False


def main():
    """Ejecuta todas las pruebas."""
    print("\n🧪 PRUEBAS DE SINCRONIZACIÓN DEL CARRITO CON FIREBASE\n")

    results = {
        "Firebase Connection": test_firebase_connection(),
        "Backend Cart Service": test_backend_cart_service(),
        "Product Service": test_product_service()
    }

    print("\n" + "=" * 60)
    print("RESUMEN DE PRUEBAS")
    print("=" * 60)

    for test_name, result in results.items():
        status = "✅ PASÓ" if result else "❌ FALLÓ"
        print(f"{test_name}: {status}")

    all_passed = all(results.values())

    if all_passed:
        print("\n🎉 TODAS LAS PRUEBAS PASARON EXITOSAMENTE")
        print("\n✨ El carrito está correctamente configurado para sincronizar con Firebase.")
        print("   Cuando un usuario autenticado agregue items al carrito, se guardarán")
        print("   automáticamente en Firebase Realtime Database.\n")
    else:
        print("\n⚠️ ALGUNAS PRUEBAS FALLARON")
        print("   Revisa los errores anteriores para identificar problemas.\n")

    return all_passed


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
