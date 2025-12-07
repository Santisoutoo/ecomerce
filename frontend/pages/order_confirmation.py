"""
Página de confirmación de pedido.
Muestra los detalles del pedido confirmado y opciones de navegación.
"""

import streamlit as st
from datetime import datetime
from config import SESSION_KEYS
from services.cart_service import CartService


def render_order_confirmation_page():
    """
    Renderiza la página de confirmación de pedido.
    """
    # Obtener número de orden
    order_number = st.session_state.get('last_order_number')

    if not order_number:
        st.error("❌ No se encontró información del pedido")
        if st.button("🏠 Volver al inicio", type="primary"):
            st.session_state[SESSION_KEYS["current_page"]] = "home"
            st.rerun()
        return

    # Buscar orden en el historial
    orders = st.session_state.get('orders', [])
    order = next((o for o in orders if o.get('order_number') == order_number), None)

    if not order:
        st.error("❌ No se encontró el pedido")
        if st.button("🏠 Volver al inicio", type="primary"):
            st.session_state[SESSION_KEYS["current_page"]] = "home"
            st.rerun()
        return

    # Mostrar confirmación exitosa
    render_success_header(order_number)

    # Botones de acción principales
    render_action_buttons()

    st.markdown("---")

    # Layout de 2 columnas
    col_left, col_right = st.columns([2, 1], gap="large")

    with col_left:
        render_order_details(order)

    with col_right:
        render_order_summary(order)


def render_success_header(order_number: str):
    """
    Renderiza el header de confirmación exitosa.

    Args:
        order_number: Número de pedido
    """
    st.markdown("""
    <style>
        .success-container {
            background: linear-gradient(135deg, #10b981 0%, #059669 100%);
            border-radius: 16px;
            padding: 2rem;
            text-align: center;
            margin-bottom: 2rem;
            box-shadow: 0 8px 24px rgba(16, 185, 129, 0.3);
        }
        .success-icon {
            font-size: 4rem;
            margin-bottom: 1rem;
            animation: checkmark 0.6s ease-in-out;
        }
        @keyframes checkmark {
            0% { transform: scale(0); }
            50% { transform: scale(1.2); }
            100% { transform: scale(1); }
        }
        .success-title {
            color: #ffffff;
            font-size: 2rem;
            font-weight: 700;
            margin: 0 0 0.5rem 0;
        }
        .success-subtitle {
            color: #d1fae5;
            font-size: 1rem;
            margin: 0;
        }
    </style>
    """, unsafe_allow_html=True)

    st.markdown(f"""
    <div class="success-container">
        <div class="success-icon">✅</div>
        <h1 class="success-title">¡Pedido Confirmado!</h1>
        <p class="success-subtitle">Tu pedido ha sido procesado exitosamente</p>
        <p class="success-subtitle" style="font-weight: 600; font-size: 1.2rem; margin-top: 1rem;">
            Número de pedido: <strong>{order_number}</strong>
        </p>
    </div>
    """, unsafe_allow_html=True)

    # Mostrar animación de éxito
    st.balloons()


def render_order_details(order: dict):
    """
    Renderiza los detalles del pedido.

    Args:
        order: Diccionario con información del pedido
    """
    st.markdown("### 📦 Detalles del Pedido")

    # Información general
    st.markdown(f"""
    <div style="
        background: #181633;
        border: 1px solid #2d2d3a;
        border-radius: 12px;
        padding: 1.5rem;
        margin-bottom: 1.5rem;
    ">
        <div style="display: flex; justify-content: space-between; margin-bottom: 1rem;">
            <div>
                <p style="color: #9ca3af; font-size: 0.875rem; margin: 0;">Número de pedido</p>
                <p style="color: #ffffff; font-weight: 600; margin: 0.25rem 0 0 0;">{order.get('order_number')}</p>
            </div>
            <div style="text-align: right;">
                <p style="color: #9ca3af; font-size: 0.875rem; margin: 0;">Estado</p>
                <p style="color: #10b981; font-weight: 600; margin: 0.25rem 0 0 0;">
                    ✓ {order.get('status', 'Confirmado').capitalize()}
                </p>
            </div>
        </div>

        <div style="border-top: 1px solid #2d2d3a; padding-top: 1rem;">
            <div style="display: flex; justify-content: space-between;">
                <div>
                    <p style="color: #9ca3af; font-size: 0.875rem; margin: 0;">Fecha de pedido</p>
                    <p style="color: #d1d5db; margin: 0.25rem 0 0 0;">{datetime.fromisoformat(order.get('date', datetime.now().isoformat())).strftime('%d/%m/%Y %H:%M')}</p>
                </div>
                <div style="text-align: right;">
                    <p style="color: #9ca3af; font-size: 0.875rem; margin: 0;">Método de pago</p>
                    <p style="color: #d1d5db; margin: 0.25rem 0 0 0;">{order.get('payment_method', 'Tarjeta de crédito')}</p>
                </div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Dirección de envío
    shipping = order.get('shipping_address', {})
    if shipping:
        st.markdown("#### 🏠 Dirección de Envío")
        st.markdown(f"""
        <div style="
            background: #1e1b4b;
            border-left: 3px solid #a78bfa;
            border-radius: 8px;
            padding: 1rem;
            margin-bottom: 1.5rem;
        ">
            <p style="color: #ffffff; margin: 0; font-weight: 600;">{shipping.get('nombre', '')} {shipping.get('apellidos', '')}</p>
            <p style="color: #d1d5db; margin: 0.5rem 0 0 0;">{shipping.get('direccion', '')}</p>
            <p style="color: #d1d5db; margin: 0.25rem 0 0 0;">
                {shipping.get('codigo_postal', '')} - {shipping.get('ciudad', '')}, {shipping.get('provincia', '')}
            </p>
            <p style="color: #d1d5db; margin: 0.25rem 0 0 0;">
                📞 {shipping.get('telefono', '')}
            </p>
        </div>
        """, unsafe_allow_html=True)

    # Productos
    st.markdown("#### 🛍️ Productos")
    items = order.get('items', [])

    for item in items:
        render_order_item(item)


def render_order_item(item: dict):
    """
    Renderiza un item del pedido.

    Args:
        item: Diccionario con información del item
    """
    st.markdown(f"""
    <div style="
        background: #181633;
        border: 1px solid #2d2d3a;
        border-radius: 8px;
        padding: 1rem;
        margin-bottom: 1rem;
        display: flex;
        gap: 1rem;
    ">
        <div style="flex-shrink: 0;">
            <img src="{item.get('imagen_url', 'https://via.placeholder.com/80')}"
                 style="width: 80px; height: 80px; border-radius: 4px; object-fit: cover;"
                 alt="{item.get('name', 'Producto')}">
        </div>
        <div style="flex-grow: 1;">
            <p style="color: #a78bfa; font-size: 0.75rem; margin: 0;">{item.get('equipo', '')}</p>
            <p style="color: #ffffff; font-weight: 600; margin: 0.25rem 0;">{item.get('name', 'Producto')}</p>
            <p style="color: #9ca3af; font-size: 0.875rem; margin: 0.25rem 0;">
                Talla: <strong>{item.get('talla', '-')}</strong> |
                Cantidad: <strong>{item.get('cantidad', 1)}</strong>
            </p>
            {f'''
            <div style="
                background: #1e1b4b;
                border-left: 2px solid #a78bfa;
                padding: 0.5rem;
                margin-top: 0.5rem;
                border-radius: 4px;
            ">
                <p style="color: #a78bfa; font-size: 0.75rem; margin: 0;">✨ Personalizado</p>
                <p style="color: #d1d5db; font-size: 0.875rem; margin: 0.25rem 0 0 0;">
                    {item.get('personalizacion', {}).get('nombre', '')} #{item.get('personalizacion', {}).get('numero', '')}
                </p>
            </div>
            ''' if item.get('personalizacion') else ''}
        </div>
        <div style="text-align: right; flex-shrink: 0;">
            <p style="color: #a78bfa; font-size: 1.25rem; font-weight: 700; margin: 0;">
                {item.get('precio_total', 0):.2f}€
            </p>
        </div>
    </div>
    """, unsafe_allow_html=True)


def render_order_summary(order: dict):
    """
    Renderiza el resumen del pedido.

    Args:
        order: Diccionario con información del pedido
    """
    st.markdown("### 💰 Resumen")

    subtotal = order.get('subtotal', 0)
    shipping = order.get('shipping', 5.00)
    discount = order.get('discount', 0)
    points_used = order.get('points_used', 0)
    total = order.get('total', 0)
    points_earned = order.get('points_earned', 0)

    st.markdown(f"""
    <div style="
        background: linear-gradient(135deg, #1e1b4b 0%, #2d2d3a 100%);
        border: 2px solid #a78bfa;
        border-radius: 12px;
        padding: 1.5rem;
        margin-bottom: 1.5rem;
    ">
        <!-- Subtotal -->
        <div style="display: flex; justify-content: space-between; margin-bottom: 0.75rem;">
            <span style="color: #d1d5db;">Subtotal:</span>
            <span style="color: #ffffff; font-weight: 600;">{subtotal:.2f}€</span>
        </div>

        <!-- Envío -->
        <div style="display: flex; justify-content: space-between; margin-bottom: 0.75rem;">
            <span style="color: #d1d5db;">Envío:</span>
            <span style="color: #ffffff; font-weight: 600;">{shipping:.2f}€</span>
        </div>

        {f'''
        <!-- Descuento -->
        <div style="display: flex; justify-content: space-between; margin-bottom: 0.75rem;">
            <span style="color: #10b981;">Descuento ({points_used} puntos):</span>
            <span style="color: #10b981; font-weight: 600;">-{discount:.2f}€</span>
        </div>
        ''' if discount > 0 else ''}

        <!-- Separador -->
        <div style="border-top: 2px solid #2d2d3a; margin: 1rem 0;"></div>

        <!-- Total -->
        <div style="display: flex; justify-content: space-between; margin-bottom: 1.5rem;">
            <span style="color: #ffffff; font-size: 1.25rem; font-weight: 700;">TOTAL:</span>
            <span style="color: #a78bfa; font-size: 1.5rem; font-weight: 700;">{total:.2f}€</span>
        </div>

        <!-- Puntos ganados -->
        <div style="
            background: #181633;
            border: 1px solid #a78bfa;
            border-radius: 8px;
            padding: 1rem;
            text-align: center;
        ">
            <p style="color: #a78bfa; font-size: 0.875rem; margin: 0 0 0.5rem 0;">🎉 ¡Puntos Ganados!</p>
            <p style="color: #ffffff; font-size: 1.5rem; font-weight: 700; margin: 0;">
                +{points_earned} puntos
            </p>
            <p style="color: #9ca3af; font-size: 0.75rem; margin: 0.5rem 0 0 0;">
                (1€ = 10 puntos)
            </p>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Información adicional
    st.markdown("### 📧 ¿Qué sigue?")
    st.markdown("""
    <div style="
        background: #181633;
        border-left: 3px solid #a78bfa;
        border-radius: 8px;
        padding: 1rem;
    ">
        <p style="color: #d1d5db; font-size: 0.875rem; margin: 0 0 0.5rem 0;">
            ✉️ Te hemos enviado un correo de confirmación con los detalles de tu pedido.
        </p>
        <p style="color: #d1d5db; font-size: 0.875rem; margin: 0 0 0.5rem 0;">
            📦 Tu pedido será procesado en 24-48 horas.
        </p>
        <p style="color: #d1d5db; font-size: 0.875rem; margin: 0;">
            🚚 Recibirás un email cuando tu pedido sea enviado con el número de seguimiento.
        </p>
    </div>
    """, unsafe_allow_html=True)


def render_action_buttons():
    """
    Renderiza los botones de acción.
    """
    st.markdown("<br>", unsafe_allow_html=True)

    # Botón principal grande para volver al inicio
    if st.button("🏠 Volver al Inicio", type="primary", use_container_width=True, key="btn_home_main"):
        # Limpiar el carrito completamente
        try:
            CartService.clear_cart()
        except Exception as e:
            print(f"Error al limpiar carrito: {e}")

        # Forzar limpieza del carrito en session_state
        st.session_state[CartService.CART_KEY] = []
        st.session_state[CartService.CART_COUNT_KEY] = 0
        st.session_state[CartService.CART_TOTAL_KEY] = 0.0

        # Marcar que el carrito fue limpiado manualmente (para evitar recargar de Firebase)
        st.session_state['cart_just_cleared'] = True

        # Limpiar datos de checkout
        if 'checkout_data' in st.session_state:
            del st.session_state['checkout_data']
        if 'checkout_step' in st.session_state:
            del st.session_state['checkout_step']
        if 'last_order_number' in st.session_state:
            del st.session_state['last_order_number']

        st.session_state[SESSION_KEYS["current_page"]] = "home"
        st.rerun()

    st.markdown("<br>", unsafe_allow_html=True)

    # Botón secundario para ver pedidos
    if st.button("📋 Ver Mis Pedidos", type="secondary", use_container_width=True, key="btn_orders"):
        st.session_state[SESSION_KEYS["current_page"]] = "account"
        st.rerun()
