"""
Servicio de carrito de compras con Firebase Realtime Database.
Gestiona las operaciones CRUD del carrito de cada usuario.
"""

from typing import Optional, List, Dict
from datetime import datetime
import uuid
from firebase_admin import db
from backend.config.firebase_config import get_database
from backend.models.models import Cart, CartItem, CartItemCreate, CartItemUpdate, Personalization


class CartService:
    """
    Servicio para gestionar el carrito de compras en Firebase.

    Estructura en Firebase:
    /carts/{user_id}/
        items/
            {item_id}/
                product_id: str
                product_name: str
                product_image: str
                team: str
                quantity: int
                size: str
                unit_price: float
                personalization_price: float
                personalization: {nombre: str, numero: int}
                subtotal: float
                created_at: str
                updated_at: str
        total_items: int
        subtotal: float
        updated_at: str
    """

    @staticmethod
    def _get_cart_ref(user_id: str) -> db.Reference:
        """
        Obtiene la referencia al carrito de un usuario en Firebase.

        Args:
            user_id: ID del usuario

        Returns:
            db.Reference: Referencia al carrito del usuario
        """
        database = get_database()
        return database.child('carts').child(user_id)

    @staticmethod
    def _calculate_subtotal(unit_price: float, personalization_price: float, quantity: int) -> float:
        """
        Calcula el subtotal de un item del carrito.

        Args:
            unit_price: Precio unitario del producto
            personalization_price: Precio de personalización
            quantity: Cantidad

        Returns:
            float: Subtotal calculado
        """
        return (unit_price + personalization_price) * quantity

    @staticmethod
    def get_cart(user_id: str, user_email: str = None) -> Cart:
        """
        Obtiene el carrito completo de un usuario.

        Args:
            user_id: ID del usuario
            user_email: Email del usuario (opcional, se usa si el carrito está vacío)

        Returns:
            Cart: Carrito del usuario
        """
        cart_ref = CartService._get_cart_ref(user_id)
        cart_data = cart_ref.get()

        if not cart_data:
            # Carrito vacío - usar email proporcionado o placeholder
            return Cart(
                user_id=user_id,
                user_email=user_email or "unknown@email.com",
                items=[],
                total_items=0,
                subtotal=0.0,
                updated_at=datetime.utcnow()
            )

        # Convertir items de dict a lista
        items = []
        items_dict = cart_data.get('items', {})

        for item_id, item_data in items_dict.items():
            # Convertir personalization si existe
            personalization = None
            if item_data.get('personalization'):
                personalization = Personalization(**item_data['personalization'])

            # Crear CartItem
            cart_item = CartItem(
                id=item_id,
                user_id=user_id,
                product_id=item_data['product_id'],
                product_name=item_data['product_name'],
                product_image=item_data['product_image'],
                team=item_data['team'],
                quantity=item_data['quantity'],
                size=item_data['size'],
                unit_price=item_data['unit_price'],
                personalization_price=item_data.get('personalization_price', 0.0),
                personalization=personalization,
                subtotal=item_data['subtotal'],
                created_at=datetime.fromisoformat(item_data.get('created_at', datetime.utcnow().isoformat())),
                updated_at=datetime.fromisoformat(item_data.get('updated_at', datetime.utcnow().isoformat()))
            )
            items.append(cart_item)

        return Cart(
            user_id=user_id,
            user_email=cart_data.get('user_email', user_email or "unknown@email.com"),
            items=items,
            total_items=cart_data.get('total_items', len(items)),
            subtotal=cart_data.get('subtotal', 0.0),
            updated_at=datetime.fromisoformat(cart_data.get('updated_at', datetime.utcnow().isoformat()))
        )

    @staticmethod
    def add_item(user_id: str, item: CartItemCreate, product_data: Dict, user_email: str = None) -> CartItem:
        """
        Añade un item al carrito del usuario.

        Args:
            user_id: ID del usuario
            item: Datos del item a añadir
            product_data: Datos completos del producto
            user_email: Email del usuario (opcional)

        Returns:
            CartItem: Item añadido al carrito
        """
        cart_ref = CartService._get_cart_ref(user_id)

        # Generar ID único para el item
        item_id = f"cart_{uuid.uuid4().hex[:12]}"

        # Calcular precio de personalización
        personalization_price = 0.0
        if item.personalization and (item.personalization.nombre or item.personalization.numero):
            personalization_price = product_data.get('precio_personalizacion', 10.0)

        # Calcular subtotal
        unit_price = product_data['precio']
        subtotal = CartService._calculate_subtotal(unit_price, personalization_price, item.quantity)

        # Crear datos del item
        now = datetime.utcnow().isoformat()
        item_data = {
            'product_id': item.product_id,
            'product_name': product_data['name'],
            'product_image': product_data['imagen_url'],
            'team': product_data['equipo'],
            'quantity': item.quantity,
            'size': item.size,
            'unit_price': unit_price,
            'personalization_price': personalization_price,
            'personalization': item.personalization.dict() if item.personalization else None,
            'subtotal': subtotal,
            'created_at': now,
            'updated_at': now
        }

        # Guardar item en Firebase
        cart_ref.child('items').child(item_id).set(item_data)

        # Actualizar totales del carrito (incluye user_email)
        CartService._update_cart_totals(user_id, user_email)

        # Retornar CartItem creado
        return CartItem(
            id=item_id,
            user_id=user_id,
            product_id=item.product_id,
            product_name=product_data['name'],
            product_image=product_data['imagen_url'],
            team=product_data['equipo'],
            quantity=item.quantity,
            size=item.size,
            unit_price=unit_price,
            personalization_price=personalization_price,
            personalization=item.personalization,
            subtotal=subtotal,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow()
        )

    @staticmethod
    def update_item(user_id: str, item_id: str, updates: CartItemUpdate) -> Optional[CartItem]:
        """
        Actualiza un item del carrito.

        Args:
            user_id: ID del usuario
            item_id: ID del item a actualizar
            updates: Datos a actualizar

        Returns:
            Optional[CartItem]: Item actualizado o None si no existe
        """
        cart_ref = CartService._get_cart_ref(user_id)
        item_ref = cart_ref.child('items').child(item_id)

        # Verificar que el item existe
        item_data = item_ref.get()
        if not item_data:
            return None

        # Actualizar campos
        update_dict = {}
        if updates.quantity is not None:
            update_dict['quantity'] = updates.quantity
        if updates.size is not None:
            update_dict['size'] = updates.size
        if updates.personalization is not None:
            update_dict['personalization'] = updates.personalization.dict() if updates.personalization else None
            # Recalcular precio de personalización
            if updates.personalization and (updates.personalization.nombre or updates.personalization.numero):
                update_dict['personalization_price'] = 10.0  # Precio fijo por ahora
            else:
                update_dict['personalization_price'] = 0.0

        # Recalcular subtotal si cambió cantidad o personalización
        if update_dict:
            quantity = update_dict.get('quantity', item_data['quantity'])
            unit_price = item_data['unit_price']
            personalization_price = update_dict.get('personalization_price', item_data.get('personalization_price', 0.0))
            update_dict['subtotal'] = CartService._calculate_subtotal(unit_price, personalization_price, quantity)
            update_dict['updated_at'] = datetime.utcnow().isoformat()

            # Aplicar actualizaciones
            item_ref.update(update_dict)

            # Actualizar totales del carrito
            CartService._update_cart_totals(user_id)

            # Obtener item actualizado
            updated_data = item_ref.get()
            personalization = None
            if updated_data.get('personalization'):
                personalization = Personalization(**updated_data['personalization'])

            return CartItem(
                id=item_id,
                user_id=user_id,
                product_id=updated_data['product_id'],
                product_name=updated_data['product_name'],
                product_image=updated_data['product_image'],
                team=updated_data['team'],
                quantity=updated_data['quantity'],
                size=updated_data['size'],
                unit_price=updated_data['unit_price'],
                personalization_price=updated_data.get('personalization_price', 0.0),
                personalization=personalization,
                subtotal=updated_data['subtotal'],
                created_at=datetime.fromisoformat(updated_data.get('created_at', datetime.utcnow().isoformat())),
                updated_at=datetime.fromisoformat(updated_data['updated_at'])
            )

        return None

    @staticmethod
    def remove_item(user_id: str, item_id: str) -> bool:
        """
        Elimina un item del carrito.

        Args:
            user_id: ID del usuario
            item_id: ID del item a eliminar

        Returns:
            bool: True si se eliminó correctamente, False si no existía
        """
        cart_ref = CartService._get_cart_ref(user_id)
        item_ref = cart_ref.child('items').child(item_id)

        # Verificar que el item existe
        if not item_ref.get():
            return False

        # Eliminar item
        item_ref.delete()

        # Actualizar totales del carrito
        CartService._update_cart_totals(user_id)

        return True

    @staticmethod
    def clear_cart(user_id: str) -> bool:
        """
        Vacía completamente el carrito de un usuario.

        Args:
            user_id: ID del usuario

        Returns:
            bool: True si se limpió correctamente
        """
        cart_ref = CartService._get_cart_ref(user_id)
        cart_ref.delete()
        return True

    @staticmethod
    def _update_cart_totals(user_id: str, user_email: str = None):
        """
        Actualiza los totales del carrito (total_items y subtotal).

        Args:
            user_id: ID del usuario
            user_email: Email del usuario (opcional)
        """
        cart_ref = CartService._get_cart_ref(user_id)
        items_dict = cart_ref.child('items').get() or {}

        total_items = 0
        subtotal = 0.0

        for item_data in items_dict.values():
            total_items += item_data.get('quantity', 0)
            subtotal += item_data.get('subtotal', 0.0)

        # Preparar datos a actualizar
        update_data = {
            'total_items': total_items,
            'subtotal': round(subtotal, 2),
            'updated_at': datetime.utcnow().isoformat()
        }

        # Agregar user_email si se proporciona
        if user_email:
            update_data['user_email'] = user_email

        # Actualizar totales
        cart_ref.update(update_data)

    @staticmethod
    def get_cart_count(user_id: str) -> int:
        """
        Obtiene el número total de items en el carrito.

        Args:
            user_id: ID del usuario

        Returns:
            int: Número de items en el carrito
        """
        cart_ref = CartService._get_cart_ref(user_id)
        cart_data = cart_ref.get()

        if not cart_data:
            return 0

        return cart_data.get('total_items', 0)
