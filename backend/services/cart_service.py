"""
Servicio de carrito de compras con Firebase Realtime Database.
Gestiona las operaciones CRUD del carrito de cada usuario.
"""

from typing import Optional, List, Dict
from datetime import datetime
from firebase_admin import db
from backend.config.firebase_config import get_database
from backend.models.models import Cart, CartItem, CartItemCreate, CartItemUpdate, Personalization


class CartService:
    """
    Servicio para gestionar el carrito de compras en Firebase.

    Estructura en Firebase:
    /carts/{user_id}/
        items/
            {product_id}/
                size: str
                quantity: int
                subtotal: float
                user_id: str
                personalization_price: float
                personalization: {nombre: str, numero: int} (opcional)
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
        return database.child('carts').child(str(user_id))

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
    def _get_product_data(product_id) -> Optional[Dict]:
        """
        Obtiene los datos de un producto desde Firebase.

        Args:
            product_id: ID del producto (int o str)

        Returns:
            Optional[Dict]: Datos del producto o None si no existe
        """
        database = get_database()
        # Convertir a int si es string
        prod_id = int(product_id) if isinstance(product_id, str) else product_id
        product_ref = database.child('products').child(str(prod_id))
        return product_ref.get()

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

        # Manejar tanto dict como list
        items_to_process = items_dict.items() if isinstance(items_dict, dict) else enumerate(items_dict) if items_dict else []

        for product_id, item_data in items_to_process:
            # Saltar elementos None (pueden aparecer cuando Firebase convierte claves numéricas a lista)
            if item_data is None:
                continue

            # Convertir product_id a int
            product_id = int(product_id) if not isinstance(product_id, int) else product_id

            # Obtener datos del producto
            product_data = CartService._get_product_data(product_id)

            if not product_data:
                # Si el producto no existe, saltar este item
                continue

            # Convertir personalization si existe
            personalization = None
            if item_data.get('personalization'):
                personalization = Personalization(**item_data['personalization'])

            # Calcular unit_price desde el producto
            unit_price = product_data.get('price', 0.0)

            # Crear CartItem
            cart_item = CartItem(
                id=product_id,  # Ahora el ID es el product_id
                user_id=item_data.get('user_id', user_id),
                product_id=product_id,
                product_name=product_data.get('name', 'Producto desconocido'),
                product_image=product_data.get('images', {}).get('main', ''),
                team=product_data.get('team', ''),
                quantity=item_data['quantity'],
                size=item_data['size'],
                unit_price=unit_price,
                personalization_price=item_data.get('personalization_price', 0.0),
                personalization=personalization,
                subtotal=item_data['subtotal'],
                created_at=datetime.utcnow(),
                updated_at=datetime.utcnow()
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

        # Calcular precio de personalización
        personalization_price = 0.0
        if item.personalization and (item.personalization.nombre or item.personalization.numero):
            personalization_price = product_data.get('personalization_price', 10.0)

        # Calcular subtotal
        unit_price = product_data['price']
        subtotal = CartService._calculate_subtotal(unit_price, personalization_price, item.quantity)

        # Crear datos del item (estructura simplificada)
        item_data = {
            'user_id': user_id,
            'size': item.size,
            'quantity': item.quantity,
            'subtotal': subtotal,
            'personalization_price': personalization_price,
            'personalization': item.personalization.dict() if item.personalization else None
        }

        # Guardar item en Firebase usando product_id como clave (convertir a string)
        cart_ref.child('items').child(str(item.product_id)).set(item_data)

        # Actualizar totales del carrito (incluye user_email)
        CartService._update_cart_totals(user_id, user_email)

        # Retornar CartItem creado
        return CartItem(
            id=item.product_id,  # ID es el product_id
            user_id=user_id,
            product_id=item.product_id,
            product_name=product_data['name'],
            product_image=product_data.get('images', {}).get('main', ''),
            team=product_data.get('team', ''),
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
    def update_item(user_id, product_id, updates: CartItemUpdate) -> Optional[CartItem]:
        """
        Actualiza un item del carrito.

        Args:
            user_id: ID del usuario (int o str)
            product_id: ID del producto (int o str)
            updates: Datos a actualizar

        Returns:
            Optional[CartItem]: Item actualizado o None si no existe
        """
        # Convertir IDs a int si es necesario
        prod_id = int(product_id) if isinstance(product_id, str) else product_id

        cart_ref = CartService._get_cart_ref(user_id)
        item_ref = cart_ref.child('items').child(str(prod_id))

        # Verificar que el item existe
        item_data = item_ref.get()
        if not item_data:
            return None

        # Obtener datos del producto
        product_data = CartService._get_product_data(prod_id)
        if not product_data:
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
                update_dict['personalization_price'] = product_data.get('personalization_price', 10.0)
            else:
                update_dict['personalization_price'] = 0.0

        # Recalcular subtotal si cambió cantidad o personalización
        if update_dict:
            quantity = update_dict.get('quantity', item_data['quantity'])
            unit_price = product_data.get('price', 0.0)
            personalization_price = update_dict.get('personalization_price', item_data.get('personalization_price', 0.0))
            update_dict['subtotal'] = CartService._calculate_subtotal(unit_price, personalization_price, quantity)

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
                id=prod_id,
                user_id=updated_data.get('user_id', user_id),
                product_id=prod_id,
                product_name=product_data.get('name', 'Producto desconocido'),
                product_image=product_data.get('images', {}).get('main', ''),
                team=product_data.get('team', ''),
                quantity=updated_data['quantity'],
                size=updated_data['size'],
                unit_price=unit_price,
                personalization_price=updated_data.get('personalization_price', 0.0),
                personalization=personalization,
                subtotal=updated_data['subtotal'],
                created_at=datetime.utcnow(),
                updated_at=datetime.utcnow()
            )

        return None

    @staticmethod
    def remove_item(user_id, product_id) -> bool:
        """
        Elimina un item del carrito.

        Args:
            user_id: ID del usuario (int o str)
            product_id: ID del producto a eliminar (int o str)

        Returns:
            bool: True si se eliminó correctamente, False si no existía
        """
        # Convertir a int si es necesario
        prod_id = int(product_id) if isinstance(product_id, str) else product_id

        cart_ref = CartService._get_cart_ref(user_id)
        item_ref = cart_ref.child('items').child(str(prod_id))

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

        # Manejar tanto dict como list
        items_values = items_dict.values() if isinstance(items_dict, dict) else items_dict if items_dict else []

        for item_data in items_values:
            # Saltar elementos None (pueden aparecer cuando Firebase convierte claves numéricas a lista)
            if item_data is None:
                continue

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
