"""
Script de prueba para el servicio de pedidos (OrderService).
Verifica la creación y gestión de pedidos en Firebase.
"""

import sys
import os

# Añadir paths
sys.path.insert(0, os.path.join(os.path.dirname(__file__)))

def test_create_order():
    """Prueba la creación de un pedido."""
    print("=" * 60)
    print("TEST 1: Crear un pedido")
    print("=" * 60)

    try:
        from backend.services.order_service import OrderService
        from backend.models.models import (
            OrderCreate, OrderItem, ShippingAddress, Personalization
        )

        # Datos del usuario
        user_id = "fZlBToT35rPVcuUg3SO1oTuXwM22"
        user_email = "hola@gmail.com"

        # Crear items del pedido
        items = [
            OrderItem(
                product_id="prod_001",
                product_name="Camiseta FC Barcelona",
                product_image="https://res.cloudinary.com/dlrrvenn1/image/upload/v1764772154/camiseta_barcelona_lgranp.jpg",
                team="Barcelona",
                quantity=2,
                size="L",
                unit_price=89.99,
                personalization_price=10.00,
                personalization=Personalization(nombre="MESSI", numero=10),
                subtotal=199.98
            ),
            OrderItem(
                product_id="prod_002",
                product_name="Camiseta Atlético de Madrid",
                product_image="https://res.cloudinary.com/dlrrvenn1/image/upload/v1764772154/camiseta_atletico_jce6ol.jpg",
                team="Atlético Madrid",
                quantity=1,
                size="M",
                unit_price=84.99,
                personalization_price=0.00,
                personalization=None,
                subtotal=84.99
            )
        ]

        # Dirección de envío
        shipping_address = ShippingAddress(
            street="Calle Ejemplo 123",
            city="Madrid",
            state="Madrid",
            postal_code="28001",
            country="España"
        )

        # Crear objeto OrderCreate
        order_create = OrderCreate(
            items=items,
            shipping_address=shipping_address,
            payment_method="credit_card"
        )

        # Crear el pedido
        print(f"\n🔄 Creando pedido para {user_email}...")
        order = OrderService.create_order(user_id, user_email, order_create)

        print(f"\n✅ Pedido creado exitosamente:")
        print(f"   - Order ID: {order.order_id}")
        print(f"   - User Email: {order.user_email}")
        print(f"   - Items: {len(order.items)}")
        print(f"   - Subtotal: €{order.subtotal}")
        print(f"   - Envío: €{order.shipping_cost}")
        print(f"   - IVA: €{order.tax}")
        print(f"   - Total: €{order.total}")
        print(f"   - Estado: {order.status.value}")
        print(f"   - Creado: {order.created_at}")

        print(f"\n   Detalles de items:")
        for i, item in enumerate(order.items, 1):
            print(f"   {i}. {item.product_name}")
            print(f"      - Cantidad: {item.quantity} x €{item.unit_price}")
            if item.personalization:
                print(f"      - Personalización: {item.personalization.nombre} #{item.personalization.numero} (+€{item.personalization_price})")
            print(f"      - Subtotal: €{item.subtotal}")

        return order.order_id

    except Exception as e:
        print(f"❌ Error al crear el pedido: {e}")
        import traceback
        traceback.print_exc()
        return None


def test_get_order(order_id: str):
    """Prueba la obtención de un pedido."""
    print("\n" + "=" * 60)
    print("TEST 2: Obtener un pedido")
    print("=" * 60)

    try:
        from backend.services.order_service import OrderService

        print(f"\n🔄 Obteniendo pedido {order_id}...")
        order = OrderService.get_order(order_id)

        if order:
            print(f"\n✅ Pedido encontrado:")
            print(f"   - Order ID: {order.order_id}")
            print(f"   - Usuario: {order.user_email}")
            print(f"   - Total: €{order.total}")
            print(f"   - Estado: {order.status.value}")
            return True
        else:
            print(f"❌ No se encontró el pedido {order_id}")
            return False

    except Exception as e:
        print(f"❌ Error al obtener el pedido: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_get_user_orders(user_email: str):
    """Prueba la obtención de pedidos de un usuario."""
    print("\n" + "=" * 60)
    print("TEST 3: Obtener pedidos de un usuario")
    print("=" * 60)

    try:
        from backend.services.order_service import OrderService

        print(f"\n🔄 Obteniendo pedidos de {user_email}...")
        orders = OrderService.get_user_orders(user_email)

        print(f"\n✅ Encontrados {len(orders)} pedidos:")
        for order in orders:
            print(f"   - {order.order_id}: €{order.total} - {order.status.value}")

        return len(orders) > 0

    except Exception as e:
        print(f"❌ Error al obtener pedidos del usuario: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_update_order_status(order_id: str):
    """Prueba la actualización del estado de un pedido."""
    print("\n" + "=" * 60)
    print("TEST 4: Actualizar estado del pedido")
    print("=" * 60)

    try:
        from backend.services.order_service import OrderService
        from backend.models.models import OrderStatusEnum

        print(f"\n🔄 Actualizando estado del pedido {order_id} a PROCESSING...")
        updated_order = OrderService.update_order_status(order_id, OrderStatusEnum.PROCESSING)

        if updated_order:
            print(f"\n✅ Estado actualizado:")
            print(f"   - Order ID: {updated_order.order_id}")
            print(f"   - Nuevo estado: {updated_order.status.value}")
            print(f"   - Actualizado: {updated_order.updated_at}")
            return True
        else:
            print(f"❌ No se pudo actualizar el pedido")
            return False

    except Exception as e:
        print(f"❌ Error al actualizar el estado: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_cleanup(order_id: str):
    """Limpia el pedido de prueba."""
    print("\n" + "=" * 60)
    print("LIMPIEZA: Eliminar pedido de prueba")
    print("=" * 60)

    try:
        from backend.services.order_service import OrderService

        print(f"\n🧹 Eliminando pedido {order_id}...")
        deleted = OrderService.delete_order(order_id)

        if deleted:
            print(f"✅ Pedido eliminado correctamente")
            return True
        else:
            print(f"⚠️ El pedido no existía")
            return False

    except Exception as e:
        print(f"❌ Error al eliminar el pedido: {e}")
        import traceback
        traceback.print_exc()
        return False


def main():
    """Ejecuta todas las pruebas."""
    print("\n🧪 PRUEBAS DEL SERVICIO DE PEDIDOS (OrderService)\n")

    # Test 1: Crear pedido
    order_id = test_create_order()

    if not order_id:
        print("\n❌ FALLO: No se pudo crear el pedido. Abortando pruebas.")
        return False

    # Test 2: Obtener pedido
    test_2 = test_get_order(order_id)

    # Test 3: Obtener pedidos de usuario
    test_3 = test_get_user_orders("hola@gmail.com")

    # Test 4: Actualizar estado
    test_4 = test_update_order_status(order_id)

    # Limpieza
    cleanup = test_cleanup(order_id)

    # Resumen
    print("\n" + "=" * 60)
    print("RESUMEN DE PRUEBAS")
    print("=" * 60)

    results = {
        "Crear pedido": order_id is not None,
        "Obtener pedido": test_2,
        "Obtener pedidos de usuario": test_3,
        "Actualizar estado": test_4,
        "Limpieza": cleanup
    }

    for test_name, result in results.items():
        status = "✅ PASÓ" if result else "❌ FALLÓ"
        print(f"{test_name}: {status}")

    all_passed = all(results.values())

    if all_passed:
        print("\n🎉 TODAS LAS PRUEBAS PASARON EXITOSAMENTE")
        print("\n✨ El servicio de pedidos está correctamente configurado.")
        print(f"   - Los pedidos usan order_id como identificador (ej: {order_id})")
        print("   - Cada pedido incluye el email del usuario")
        print("   - Los items incluyen personalización cuando aplica\n")
    else:
        print("\n⚠️ ALGUNAS PRUEBAS FALLARON")
        print("   Revisa los errores anteriores para identificar problemas.\n")

    return all_passed


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
