"""
Página del carrito de compras.
Muestra productos agregados, permite editar cantidades y proceder al checkout.
"""

import streamlit as st
from frontend.components.cart_item import render_cart_item
from frontend.config import SESSION_KEYS


# Constantes (deberían venir de config)
SHIPPING_COST = 5.0
POINTS_PER_EURO = 10
POINTS_TO_EURO_RATIO = 100


def render_cart_page():
    """
    Renderiza la página del carrito de compras.
    """
    st.markdown("# 🛒 Carrito de Compras")

    # Obtener carrito
    cart = st.session_state.get('cart', [])

    if not cart:
        render_empty_cart()
        return

    # Layout de 2 columnas: Items | Resumen
    col_items, col_summary = st.columns([2, 1], gap="large")

    with col_items:
        render_cart_items(cart)

    with col_summary:
        render_cart_summary(cart)


def render_empty_cart():
    """
    Renderiza la vista de carrito vacío.
    """
    st.markdown("""
    <div style="
        text-align: center;
        padding: 4rem 2rem;
        background: #181633;
        border: 2px dashed #2d2d3a;
        border-radius: 16px;
        margin: 2rem 0;
    ">
        <p style="font-size: 4rem; margin: 0 0 1rem 0;">🛒</p>
        <h2 style="color: #a78bfa; margin: 0 0 1rem 0;">
            Tu carrito está vacío
        </h2>
        <p style="color: #9ca3af; margin: 0 0 2rem 0;">
            ¡Explora nuestro catálogo y encuentra tus productos favoritos!
        </p>
    </div>
    """, unsafe_allow_html=True)

    # Botón para ir al catálogo
    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        if st.button("🛍️ Ir al Catálogo", type="primary", use_container_width=True):
            st.session_state[SESSION_KEYS["current_page"]] = "home"
            st.rerun()


def render_cart_items(cart: list):
    """
    Renderiza la lista de items en el carrito.

    Args:
        cart: Lista de items del carrito
    """
    # Header de la sección
    col1, col2 = st.columns([3, 1])

    with col1:
        st.markdown(f"### 📦 Productos ({len(cart)})")

    with col2:
        if st.button("🗑️ Vaciar Carrito", type="secondary", use_container_width=True):
            clear_cart()

    st.markdown("<br>", unsafe_allow_html=True)

    # Renderizar cada item
    for index, item in enumerate(cart):
        render_cart_item(item, index)


def render_cart_summary(cart: list):
    """
    Renderiza el resumen del carrito con totales y opciones de checkout.

    Args:
        cart: Lista de items del carrito
    """
    st.markdown("### 💰 Resumen del Pedido")

    # Calcular totales
    subtotal = calculate_subtotal(cart)
    shipping = SHIPPING_COST
    discount_points = st.session_state.get('applied_points_discount', 0)
    total = subtotal + shipping - discount_points

    # Contenedor del resumen
    st.markdown("""
    <div style="
        background: #181633;
        border: 2px solid #2d2d3a;
        border-radius: 12px;
        padding: 1.5rem;
        margin-bottom: 1.5rem;
    ">
    </div>
    """, unsafe_allow_html=True)

    # Subtotal
    st.markdown(f"""
    <div style="display: flex; justify-content: space-between; margin-bottom: 0.75rem;">
        <span style="color: #d1d5db;">Subtotal:</span>
        <span style="color: #ffffff; font-weight: 600;">{subtotal:.2f}€</span>
    </div>
    """, unsafe_allow_html=True)

    # Gastos de envío
    st.markdown(f"""
    <div style="display: flex; justify-content: space-between; margin-bottom: 0.75rem;">
        <span style="color: #d1d5db;">Gastos de envío:</span>
        <span style="color: #ffffff; font-weight: 600;">{shipping:.2f}€</span>
    </div>
    """, unsafe_allow_html=True)

    # Descuento por puntos
    if discount_points > 0:
        st.markdown(f"""
        <div style="display: flex; justify-content: space-between; margin-bottom: 0.75rem;">
            <span style="color: #10b981;">Descuento puntos:</span>
            <span style="color: #10b981; font-weight: 600;">-{discount_points:.2f}€</span>
        </div>
        """, unsafe_allow_html=True)

    # Separador
    st.markdown("<hr style='margin: 1rem 0; border-color: #2d2d3a;'>", unsafe_allow_html=True)

    # Total
    st.markdown(f"""
    <div style="display: flex; justify-content: space-between; margin-bottom: 1.5rem;">
        <span style="color: #ffffff; font-size: 1.25rem; font-weight: 700;">TOTAL:</span>
        <span style="color: #a78bfa; font-size: 1.75rem; font-weight: 700;">{total:.2f}€</span>
    </div>
    """, unsafe_allow_html=True)

    # Puntos que ganará
    points_to_earn = int(total * POINTS_PER_EURO)
    st.markdown(f"""
    <div style="
        background: linear-gradient(135deg, #1e1b4b 0%, #2d2d3a 100%);
        border: 1px solid #a78bfa;
        border-radius: 8px;
        padding: 1rem;
        margin-bottom: 1.5rem;
        text-align: center;
    ">
        <p style="color: #a78bfa; font-size: 0.875rem; margin: 0 0 0.25rem 0;">
            ⭐ Ganarás con esta compra
        </p>
        <p style="color: #ffffff; font-size: 1.5rem; font-weight: 700; margin: 0;">
            {points_to_earn} puntos
        </p>
    </div>
    """, unsafe_allow_html=True)

    # Sección de canjear puntos
    render_points_section(subtotal)

    # Botón de checkout
    st.markdown("<br>", unsafe_allow_html=True)

    if st.button("💳 Proceder al Pago", type="primary", use_container_width=True, key="checkout_btn"):
        proceed_to_checkout()

    # Botón continuar comprando
    if st.button("🛍️ Continuar Comprando", use_container_width=True, key="continue_shopping"):
        st.session_state[SESSION_KEYS["current_page"]] = "home"
        st.rerun()


def render_points_section(subtotal: float):
    """
    Renderiza la sección de canjear puntos de fidelización.

    Args:
        subtotal: Subtotal del pedido
    """
    st.markdown("---")
    st.markdown("#### 🎁 Canjear Puntos")

    # Obtener puntos del usuario (por ahora mock)
    user_points = st.session_state.get('user_points', 0)

    st.markdown(f"""
    <p style="color: #d1d5db; font-size: 0.875rem;">
        Tienes <strong style="color: #a78bfa;">{user_points} puntos</strong> disponibles
        <br>
        <span style="color: #9ca3af; font-size: 0.75rem;">
            ({POINTS_TO_EURO_RATIO} puntos = 1€ de descuento)
        </span>
    </p>
    """, unsafe_allow_html=True)

    if user_points >= POINTS_TO_EURO_RATIO:
        # Calcular máximo canjeable (50% del subtotal)
        max_discount = subtotal * 0.5
        max_points_can_use = int((max_discount * POINTS_TO_EURO_RATIO))
        max_points_available = min(user_points, max_points_can_use)

        # Slider para seleccionar puntos
        points_to_use = st.slider(
            "Puntos a canjear",
            min_value=0,
            max_value=max_points_available,
            step=POINTS_TO_EURO_RATIO,
            value=st.session_state.get('points_to_use', 0),
            key="points_slider"
        )

        # Calcular descuento
        discount = points_to_use / POINTS_TO_EURO_RATIO

        if points_to_use > 0:
            st.markdown(f"""
            <p style="color: #10b981; font-size: 0.875rem; margin-top: 0.5rem;">
                ✅ Aplicando descuento de <strong>{discount:.2f}€</strong>
            </p>
            """, unsafe_allow_html=True)

            # Guardar descuento aplicado
            st.session_state['applied_points_discount'] = discount
            st.session_state['points_to_use'] = points_to_use
        else:
            st.session_state['applied_points_discount'] = 0
            st.session_state['points_to_use'] = 0
    else:
        st.info(f"ℹ️ Necesitas al menos {POINTS_TO_EURO_RATIO} puntos para canjear")


def calculate_subtotal(cart: list) -> float:
    """
    Calcula el subtotal del carrito.

    Args:
        cart: Lista de items del carrito

    Returns:
        float: Subtotal del carrito
    """
    subtotal = 0
    for item in cart:
        precio_unitario = item.get('precio_unitario', 0)
        precio_personalizacion = item.get('precio_personalizacion', 0)
        cantidad = item.get('cantidad', 1)
        subtotal += (precio_unitario + precio_personalizacion) * cantidad

    return subtotal


def clear_cart():
    """
    Vacía completamente el carrito.
    """
    if 'cart' in st.session_state:
        st.session_state['cart'] = []

    # Limpiar también puntos aplicados
    if 'applied_points_discount' in st.session_state:
        del st.session_state['applied_points_discount']
    if 'points_to_use' in st.session_state:
        del st.session_state['points_to_use']

    st.success("✅ Carrito vaciado")
    st.rerun()


def proceed_to_checkout():
    """
    Procede al proceso de checkout.
    """
    # Validar que el carrito no esté vacío
    cart = st.session_state.get('cart', [])
    if not cart:
        st.error("❌ El carrito está vacío")
        return

    # Guardar información del pedido para checkout
    subtotal = calculate_subtotal(cart)
    shipping = SHIPPING_COST
    discount = st.session_state.get('applied_points_discount', 0)
    total = subtotal + shipping - discount

    st.session_state['checkout_data'] = {
        'cart': cart.copy(),
        'subtotal': subtotal,
        'shipping': shipping,
        'discount': discount,
        'total': total,
        'points_to_earn': int(total * POINTS_PER_EURO),
        'points_used': st.session_state.get('points_to_use', 0)
    }

    # Navegar a checkout
    st.session_state[SESSION_KEYS["current_page"]] = "checkout"
    st.success("✅ Procediendo al pago...")
    st.rerun()
