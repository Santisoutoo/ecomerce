"""
Servicio de pedidos (órdenes) con Firebase Realtime Database.
Gestiona la creación, actualización y consulta de pedidos.
"""

from typing import Optional, List
from datetime import datetime
import uuid
from firebase_admin import db
from config.firebase_config import get_database
from models.models import (
    Order, OrderItem, OrderCreate, OrderUpdate,
    OrderStatusEnum, ShippingAddress, Personalization
)


class OrderService:
    """
    Servicio para gestionar pedidos en Firebase.

    Estructura en Firebase:
    /orders/{order_id}/
        order_id: str (ORD-YYYYMMDD-XXXX)
        user_id: str
        user_email: str
        items: []
        subtotal: float
        shipping_cost: float
        tax: float
        total: float
        status: str
        shipping_address: {}
        payment_method: str
        created_at: str
        updated_at: str
    """

    @staticmethod
    def _generate_order_id() -> str:
        """
        Genera un ID único para el pedido con formato: ORD-YYYYMMDD-XXXX.

        Returns:
            str: ID del pedido
        """
        date_str = datetime.utcnow().strftime("%Y%m%d")
        unique_suffix = uuid.uuid4().hex[:4].upper()
        return f"ORD-{date_str}-{unique_suffix}"

    @staticmethod
    def _get_orders_ref() -> db.Reference:
        """
        Obtiene la referencia a la colección de órdenes en Firebase.

        Returns:
            db.Reference: Referencia a /orders
        """
        database = get_database()
        return database.child('orders')

    @staticmethod
    def create_order(
        user_id: str,
        user_email: str,
        order_data: OrderCreate
    ) -> Order:
        """
        Crea un nuevo pedido en Firebase.

        Args:
            user_id: ID del usuario en Firebase Auth
            user_email: Email del usuario
            order_data: Datos del pedido a crear

        Returns:
            Order: Pedido creado
        """
        # Generar ID único del pedido
        order_id = OrderService._generate_order_id()

        # Calcular totales
        subtotal = sum(item.subtotal for item in order_data.items)

        # Calcular costo de envío (gratis si >50€, sino 5€)
        shipping_cost = 0.0 if subtotal >= 50 else 5.0

        # Calcular IVA (21%)
        tax = round((subtotal + shipping_cost) * 0.21, 2)

        # Total
        total = round(subtotal + shipping_cost + tax, 2)

        # Timestamp
        now = datetime.utcnow().isoformat()

        # Preparar datos para Firebase
        order_dict = {
            'order_id': order_id,
            'user_id': user_id,
            'user_email': user_email,
            'items': [item.dict() for item in order_data.items],
            'subtotal': subtotal,
            'shipping_cost': shipping_cost,
            'tax': tax,
            'total': total,
            'status': OrderStatusEnum.PENDING.value,
            'shipping_address': order_data.shipping_address.dict(),
            'payment_method': order_data.payment_method,
            'created_at': now,
            'updated_at': now
        }

        # Guardar en Firebase usando order_id como clave
        orders_ref = OrderService._get_orders_ref()
        orders_ref.child(order_id).set(order_dict)

        # Retornar Order creado
        return Order(
            order_id=order_id,
            user_id=user_id,
            user_email=user_email,
            items=order_data.items,
            subtotal=subtotal,
            shipping_cost=shipping_cost,
            tax=tax,
            total=total,
            status=OrderStatusEnum.PENDING,
            shipping_address=order_data.shipping_address,
            payment_method=order_data.payment_method,
            created_at=datetime.fromisoformat(now),
            updated_at=datetime.fromisoformat(now)
        )

    @staticmethod
    def get_order(order_id: str) -> Optional[Order]:
        """
        Obtiene un pedido por su ID.

        Args:
            order_id: ID del pedido

        Returns:
            Optional[Order]: Pedido si existe, None si no
        """
        orders_ref = OrderService._get_orders_ref()
        order_data = orders_ref.child(order_id).get()

        if not order_data:
            return None

        # Convertir items
        items = []
        for item_data in order_data.get('items', []):
            # Convertir personalización si existe
            personalization = None
            if item_data.get('personalization'):
                personalization = Personalization(**item_data['personalization'])

            order_item = OrderItem(
                product_id=item_data['product_id'],
                product_name=item_data['product_name'],
                product_image=item_data['product_image'],
                team=item_data['team'],
                quantity=item_data['quantity'],
                size=item_data['size'],
                unit_price=item_data['unit_price'],
                personalization_price=item_data.get('personalization_price', 0.0),
                personalization=personalization,
                subtotal=item_data['subtotal']
            )
            items.append(order_item)

        # Convertir dirección de envío
        shipping_address = ShippingAddress(**order_data['shipping_address'])

        return Order(
            order_id=order_data['order_id'],
            user_id=order_data['user_id'],
            user_email=order_data['user_email'],
            items=items,
            subtotal=order_data['subtotal'],
            shipping_cost=order_data['shipping_cost'],
            tax=order_data['tax'],
            total=order_data['total'],
            status=OrderStatusEnum(order_data['status']),
            shipping_address=shipping_address,
            payment_method=order_data['payment_method'],
            created_at=datetime.fromisoformat(order_data['created_at']),
            updated_at=datetime.fromisoformat(order_data['updated_at'])
        )

    @staticmethod
    def get_user_orders(user_email: str) -> List[Order]:
        """
        Obtiene todos los pedidos de un usuario por su email.

        Args:
            user_email: Email del usuario

        Returns:
            List[Order]: Lista de pedidos del usuario
        """
        orders_ref = OrderService._get_orders_ref()
        all_orders = orders_ref.get()

        if not all_orders:
            return []

        user_orders = []
        for order_id, order_data in all_orders.items():
            if order_data.get('user_email') == user_email:
                order = OrderService.get_order(order_id)
                if order:
                    user_orders.append(order)

        # Ordenar por fecha de creación (más recientes primero)
        user_orders.sort(key=lambda x: x.created_at, reverse=True)

        return user_orders

    @staticmethod
    def update_order_status(order_id: str, new_status: OrderStatusEnum) -> Optional[Order]:
        """
        Actualiza el estado de un pedido.

        Args:
            order_id: ID del pedido
            new_status: Nuevo estado del pedido

        Returns:
            Optional[Order]: Pedido actualizado o None si no existe
        """
        orders_ref = OrderService._get_orders_ref()
        order_ref = orders_ref.child(order_id)

        # Verificar que el pedido existe
        if not order_ref.get():
            return None

        # Actualizar estado y timestamp
        order_ref.update({
            'status': new_status.value,
            'updated_at': datetime.utcnow().isoformat()
        })

        # Retornar pedido actualizado
        return OrderService.get_order(order_id)

    @staticmethod
    def get_all_orders(limit: Optional[int] = None) -> List[Order]:
        """
        Obtiene todos los pedidos (uso administrativo).

        Args:
            limit: Número máximo de pedidos a retornar

        Returns:
            List[Order]: Lista de todos los pedidos
        """
        orders_ref = OrderService._get_orders_ref()
        all_orders_data = orders_ref.get()

        if not all_orders_data:
            return []

        orders = []
        for order_id in all_orders_data.keys():
            order = OrderService.get_order(order_id)
            if order:
                orders.append(order)

        # Ordenar por fecha de creación (más recientes primero)
        orders.sort(key=lambda x: x.created_at, reverse=True)

        if limit:
            orders = orders[:limit]

        return orders

    @staticmethod
    def delete_order(order_id: str) -> bool:
        """
        Elimina un pedido (solo para administradores).

        Args:
            order_id: ID del pedido a eliminar

        Returns:
            bool: True si se eliminó, False si no existía
        """
        orders_ref = OrderService._get_orders_ref()
        order_ref = orders_ref.child(order_id)

        if not order_ref.get():
            return False

        order_ref.delete()
        return True
