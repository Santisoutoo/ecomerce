"""
Servicio de carrito de compras para el frontend.
Gestiona el carrito sincronizándolo con Firebase Realtime Database.
"""

import streamlit as st
from typing import Optional, Dict, List
import sys
import os

# Agregar path del backend para importar modelos y servicios
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

try:
    from backend.services.cart_service import CartService as BackendCartService
    from backend.models.models import CartItemCreate, Personalization
    FIREBASE_AVAILABLE = True
except Exception as e:
    print(f"⚠️ Firebase no disponible: {e}")
    FIREBASE_AVAILABLE = False

from services.product_service import ProductService


class CartService:
    """
    Servicio de carrito para el frontend.
    Sincroniza con Firebase Realtime Database cuando el usuario está autenticado.
    """

    CART_KEY = "cart"
    CART_COUNT_KEY = "cart_count"
    CART_TOTAL_KEY = "cart_total"

    @staticmethod
    def _get_user_id() -> Optional[str]:
        """Obtiene el ID del usuario autenticado."""
        return st.session_state.get('user_id')

    @staticmethod
    def _sync_with_firebase(user_id: str):
        """
        Sincroniza el carrito local con Firebase.

        Args:
            user_id: ID del usuario
        """
        if not FIREBASE_AVAILABLE:
            return

        try:
            # Obtener carrito de Firebase
            firebase_cart = BackendCartService.get_cart(user_id)

            # Actualizar session_state con datos de Firebase
            st.session_state[CartService.CART_KEY] = [
                {
                    'id': item.id,
                    'product_id': item.product_id,
                    'product_name': item.product_name,
                    'product_image': item.product_image,
                    'team': item.team,
                    'quantity': item.quantity,
                    'size': item.size,
                    'unit_price': item.unit_price,
                    'personalization_price': item.personalization_price,
                    'personalization': item.personalization.dict() if item.personalization else None,
                    'subtotal': item.subtotal
                }
                for item in firebase_cart.items
            ]
            st.session_state[CartService.CART_COUNT_KEY] = firebase_cart.total_items
            st.session_state[CartService.CART_TOTAL_KEY] = firebase_cart.subtotal
        except Exception as e:
            print(f"Error al sincronizar con Firebase: {e}")

    @staticmethod
    def initialize_cart():
        """Inicializa el carrito desde Firebase o session_state."""
        if CartService.CART_KEY not in st.session_state:
            st.session_state[CartService.CART_KEY] = []
        if CartService.CART_COUNT_KEY not in st.session_state:
            st.session_state[CartService.CART_COUNT_KEY] = 0
        if CartService.CART_TOTAL_KEY not in st.session_state:
            st.session_state[CartService.CART_TOTAL_KEY] = 0.0

        # Sincronizar con Firebase si el usuario está autenticado
        user_id = CartService._get_user_id()
        if user_id and FIREBASE_AVAILABLE:
            CartService._sync_with_firebase(user_id)

    @staticmethod
    def get_cart() -> List[Dict]:
        """
        Obtiene todos los items del carrito.

        Returns:
            List[Dict]: Lista de items en el carrito
        """
        CartService.initialize_cart()
        return st.session_state[CartService.CART_KEY]

    @staticmethod
    def get_cart_count() -> int:
        """
        Obtiene el número total de items en el carrito.

        Returns:
            int: Número de items
        """
        CartService.initialize_cart()
        return st.session_state[CartService.CART_COUNT_KEY]

    @staticmethod
    def get_cart_total() -> float:
        """
        Obtiene el total del carrito.

        Returns:
            float: Total en euros
        """
        CartService.initialize_cart()
        return st.session_state[CartService.CART_TOTAL_KEY]

    @staticmethod
    def add_to_cart(
        product_id: str,
        quantity: int = 1,
        size: str = "M",
        personalization: Optional[Dict] = None
    ) -> Dict:
        """
        Añade un producto al carrito y sincroniza con Firebase.

        Args:
            product_id: ID del producto
            quantity: Cantidad a añadir
            size: Talla seleccionada
            personalization: Datos de personalización (nombre, numero)

        Returns:
            Dict: Item añadido al carrito
        """
        CartService.initialize_cart()

        # Obtener datos del producto
        product = ProductService.get_product_by_id(product_id)
        if not product:
            raise ValueError(f"Producto {product_id} no encontrado")

        # Calcular precios
        unit_price = product['precio']
        personalization_price = 0.0

        if personalization and (personalization.get('nombre') or personalization.get('numero') is not None):
            personalization_price = product.get('precio_personalizacion', 10.0)

        subtotal = (unit_price + personalization_price) * quantity

        # Crear item del carrito
        cart_item = {
            'product_id': product_id,
            'product_name': product['name'],
            'product_image': product['imagen_url'],
            'team': product['equipo'],
            'quantity': quantity,
            'size': size,
            'unit_price': unit_price,
            'personalization_price': personalization_price,
            'personalization': personalization,
            'subtotal': subtotal
        }

        # Sincronizar con Firebase si el usuario está autenticado
        user_id = CartService._get_user_id()
        if user_id and FIREBASE_AVAILABLE:
            try:
                # Crear personalización si existe
                pers_obj = None
                if personalization:
                    pers_obj = Personalization(
                        nombre=personalization.get('nombre'),
                        numero=personalization.get('numero')
                    )

                # Añadir a Firebase
                item_create = CartItemCreate(
                    product_id=product_id,
                    quantity=quantity,
                    size=size,
                    personalization=pers_obj
                )

                firebase_item = BackendCartService.add_item(user_id, item_create, product)

                # Actualizar el item local con el ID de Firebase
                cart_item['id'] = firebase_item.id

                # Sincronizar carrito completo
                CartService._sync_with_firebase(user_id)

            except Exception as e:
                print(f"Error al añadir a Firebase: {e}")
                # Continuar con carrito local
                st.session_state[CartService.CART_KEY].append(cart_item)
                CartService._update_totals()
        else:
            # Sin Firebase, usar solo session_state
            st.session_state[CartService.CART_KEY].append(cart_item)
            CartService._update_totals()

        return cart_item

    @staticmethod
    def update_item(index: int, quantity: Optional[int] = None, size: Optional[str] = None):
        """
        Actualiza un item del carrito por su índice.

        Args:
            index: Índice del item en el carrito
            quantity: Nueva cantidad (opcional)
            size: Nueva talla (opcional)
        """
        CartService.initialize_cart()
        cart = st.session_state[CartService.CART_KEY]

        if 0 <= index < len(cart):
            item = cart[index]

            # Sincronizar con Firebase si está disponible
            user_id = CartService._get_user_id()
            if user_id and FIREBASE_AVAILABLE and 'id' in item:
                try:
                    from backend.models.models import CartItemUpdate

                    update_data = CartItemUpdate(
                        quantity=quantity,
                        size=size
                    )

                    BackendCartService.update_item(user_id, item['id'], update_data)
                    CartService._sync_with_firebase(user_id)
                    return
                except Exception as e:
                    print(f"Error al actualizar en Firebase: {e}")

            # Actualización local si Firebase no está disponible
            if quantity is not None:
                item['quantity'] = quantity

            if size is not None:
                item['size'] = size

            # Recalcular subtotal
            item['subtotal'] = (item['unit_price'] + item['personalization_price']) * item['quantity']

            # Actualizar totales
            CartService._update_totals()

    @staticmethod
    def remove_item(index: int):
        """
        Elimina un item del carrito por su índice.

        Args:
            index: Índice del item a eliminar
        """
        CartService.initialize_cart()
        cart = st.session_state[CartService.CART_KEY]

        if 0 <= index < len(cart):
            item = cart[index]

            # Sincronizar con Firebase si está disponible
            user_id = CartService._get_user_id()
            if user_id and FIREBASE_AVAILABLE and 'id' in item:
                try:
                    BackendCartService.remove_item(user_id, item['id'])
                    CartService._sync_with_firebase(user_id)
                    return
                except Exception as e:
                    print(f"Error al eliminar de Firebase: {e}")

            # Eliminación local si Firebase no está disponible
            cart.pop(index)
            CartService._update_totals()

    @staticmethod
    def clear_cart():
        """Vacía completamente el carrito."""
        user_id = CartService._get_user_id()
        if user_id and FIREBASE_AVAILABLE:
            try:
                BackendCartService.clear_cart(user_id)
            except Exception as e:
                print(f"Error al limpiar carrito en Firebase: {e}")

        # Limpiar local
        st.session_state[CartService.CART_KEY] = []
        st.session_state[CartService.CART_COUNT_KEY] = 0
        st.session_state[CartService.CART_TOTAL_KEY] = 0.0

    @staticmethod
    def _update_totals():
        """Actualiza los totales del carrito (count y total)."""
        cart = st.session_state[CartService.CART_KEY]

        total_items = sum(item['quantity'] for item in cart)
        total_price = sum(item['subtotal'] for item in cart)

        st.session_state[CartService.CART_COUNT_KEY] = total_items
        st.session_state[CartService.CART_TOTAL_KEY] = round(total_price, 2)

    @staticmethod
    def find_similar_item(product_id: str, size: str, personalization: Optional[Dict]) -> Optional[int]:
        """
        Busca si existe un item similar en el carrito.

        Args:
            product_id: ID del producto
            size: Talla
            personalization: Datos de personalización

        Returns:
            Optional[int]: Índice del item si existe, None si no
        """
        CartService.initialize_cart()
        cart = st.session_state[CartService.CART_KEY]

        for i, item in enumerate(cart):
            if (item['product_id'] == product_id and
                item['size'] == size and
                item['personalization'] == personalization):
                return i

        return None

    @staticmethod
    def add_or_update_item(
        product_id: str,
        quantity: int = 1,
        size: str = "M",
        personalization: Optional[Dict] = None
    ) -> Dict:
        """
        Añade un producto al carrito o actualiza la cantidad si ya existe uno similar.

        Args:
            product_id: ID del producto
            quantity: Cantidad a añadir
            size: Talla seleccionada
            personalization: Datos de personalización

        Returns:
            Dict: Item añadido o actualizado
        """
        # Buscar item similar
        similar_index = CartService.find_similar_item(product_id, size, personalization)

        if similar_index is not None:
            # Actualizar cantidad
            cart = st.session_state[CartService.CART_KEY]
            cart[similar_index]['quantity'] += quantity
            CartService.update_item(similar_index, quantity=cart[similar_index]['quantity'])
            return cart[similar_index]
        else:
            # Añadir nuevo item
            return CartService.add_to_cart(product_id, quantity, size, personalization)

    @staticmethod
    def get_cart_summary() -> Dict:
        """
        Obtiene un resumen del carrito.

        Returns:
            Dict: Resumen con items, count, subtotal, shipping, tax y total
        """
        CartService.initialize_cart()

        cart = st.session_state[CartService.CART_KEY]
        subtotal = st.session_state[CartService.CART_TOTAL_KEY]

        # Calcular envío (gratis si >50€, sino 5€)
        shipping = 0.0 if subtotal >= 50 else 5.0

        # Calcular IVA (21%)
        tax = round((subtotal + shipping) * 0.21, 2)

        # Total
        total = round(subtotal + shipping + tax, 2)

        return {
            'items': cart,
            'count': st.session_state[CartService.CART_COUNT_KEY],
            'subtotal': subtotal,
            'shipping': shipping,
            'tax': tax,
            'total': total
        }
