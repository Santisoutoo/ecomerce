"""
Página de checkout/pago.
Proceso de finalización de compra con dirección de envío y pago simulado.
"""

import streamlit as st
from datetime import datetime
from config import SESSION_KEYS


def render_checkout_page():
    """
    Renderiza la página de checkout con formularios de envío y pago.
    """
    st.markdown("# 💳 Checkout - Finalizar Compra")

    # Verificar si hay que mostrar el modal de confirmación
    if st.session_state.get('show_order_modal', False):
        order = st.session_state.get('modal_order')
        if order:
            render_order_confirmation_modal(order)

            # Botón para continuar (fuera del modal HTML pero estilizado)
            st.markdown("<br><br><br><br><br><br><br><br><br><br><br><br><br>", unsafe_allow_html=True)
            col1, col2, col3 = st.columns([1, 2, 1])
            with col2:
                if st.button("✓ CONTINUAR", type="primary", use_container_width=True, key="continue_after_modal"):
                    # Ahora sí, limpiar carrito y datos de checkout
                    st.session_state['cart'] = []
                    st.session_state['checkout_data'] = None
                    st.session_state['checkout_step'] = 1
                    st.session_state['applied_points_discount'] = 0
                    st.session_state['points_to_use'] = 0

                    # Limpiar flags del modal
                    st.session_state['show_order_modal'] = False
                    st.session_state['modal_order'] = None

                    # Ir a página de confirmación
                    st.session_state[SESSION_KEYS["current_page"]] = "order_confirmation"
                    st.rerun()
            return

    # Verificar que haya datos de checkout
    checkout_data = st.session_state.get('checkout_data')

    if not checkout_data:
        st.error("❌ No hay datos de checkout. Por favor, vuelve al carrito.")
        if st.button("🛒 Volver al Carrito"):
            st.session_state[SESSION_KEYS["current_page"]] = "cart"
            st.rerun()
        return

    # Inicializar paso del checkout
    if 'checkout_step' not in st.session_state:
        st.session_state['checkout_step'] = 1

    # Progress bar
    render_progress_bar(st.session_state['checkout_step'])

    # Renderizar el paso correspondiente
    step = st.session_state['checkout_step']

    if step == 1:
        render_review_order_step(checkout_data)
    elif step == 2:
        render_shipping_address_step()
    elif step == 3:
        render_payment_method_step()


def render_progress_bar(current_step: int):
    """
    Renderiza la barra de progreso del checkout.

    Args:
        current_step: Paso actual (1-3)
    """
    steps = [
        {"num": 1, "title": "Revisión"},
        {"num": 2, "title": "Envío"},
        {"num": 3, "title": "Pago"}
    ]

    cols = st.columns(len(steps))

    for i, step in enumerate(steps):
        with cols[i]:
            is_active = step["num"] <= current_step
            is_current = step["num"] == current_step

            color = "#a78bfa" if is_active else "#2d2d3a"
            border_color = "#a78bfa" if is_current else color

            st.markdown(f"""
            <div style="text-align: center; margin-bottom: 2rem;">
                <div style="
                    width: 50px;
                    height: 50px;
                    background: {color};
                    border: 3px solid {border_color};
                    border-radius: 50%;
                    margin: 0 auto 0.5rem auto;
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    color: white;
                    font-size: 1.5rem;
                    font-weight: 700;
                ">
                    {step["num"]}
                </div>
                <p style="color: {color}; margin: 0; font-size: 0.9rem; font-weight: 600;">
                    {step["title"]}
                </p>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("<hr style='margin: 1rem 0; border-color: #2d2d3a;'>", unsafe_allow_html=True)


def render_review_order_step(checkout_data: dict):
    """
    Paso 1: Revisión del pedido.

    Args:
        checkout_data: Datos del pedido
    """
    st.markdown("## 📦 Paso 1: Revisa tu Pedido")

    # Layout de 2 columnas
    col_left, col_right = st.columns([2, 1], gap="large")

    with col_left:
        st.markdown("### 🛍️ Productos")

        # Mostrar cada producto
        for item in checkout_data['cart']:
            render_checkout_item(item)

    with col_right:
        st.markdown("### 💰 Resumen")

        # Resumen de precios
        subtotal = checkout_data['subtotal']
        shipping = checkout_data['shipping']
        discount = checkout_data['discount']
        total = checkout_data['total']

        # Contenedor con borde
        st.markdown("""
        <div style="
            background: #181633;
            border: 2px solid #2d2d3a;
            border-radius: 12px;
            padding: 1.5rem;
        ">
        """, unsafe_allow_html=True)

        # Subtotal
        st.markdown(f"""
        <div style="margin-bottom: 0.75rem;">
            <span style="color: #d1d5db;">Subtotal:</span>
            <span style="color: #ffffff; float: right; font-weight: 600;">{subtotal:.2f}€</span>
        </div>
        """, unsafe_allow_html=True)

        # Envío
        st.markdown(f"""
        <div style="margin-bottom: 0.75rem;">
            <span style="color: #d1d5db;">Envío:</span>
            <span style="color: #ffffff; float: right; font-weight: 600;">{shipping:.2f}€</span>
        </div>
        """, unsafe_allow_html=True)

        # Descuento (solo si existe)
        if discount > 0:
            st.markdown(f"""
            <div style="margin-bottom: 0.75rem;">
                <span style="color: #10b981;">Descuento:</span>
                <span style="color: #10b981; float: right; font-weight: 600;">-{discount:.2f}€</span>
            </div>
            """, unsafe_allow_html=True)

        # Separador
        st.markdown('<hr style="margin: 1rem 0; border-color: #2d2d3a;">', unsafe_allow_html=True)

        # Total
        st.markdown(f"""
        <div>
            <span style="color: #ffffff; font-size: 1.25rem; font-weight: 700;">TOTAL:</span>
            <span style="color: #a78bfa; float: right; font-size: 1.5rem; font-weight: 700;">{total:.2f}€</span>
        </div>
        """, unsafe_allow_html=True)

        # Cerrar contenedor
        st.markdown("</div>", unsafe_allow_html=True)

        # Puntos a ganar
        st.markdown(f"""
        <div style="
            background: linear-gradient(135deg, #1e1b4b 0%, #2d2d3a 100%);
            border: 1px solid #a78bfa;
            border-radius: 8px;
            padding: 1rem;
            margin-top: 1rem;
            text-align: center;
        ">
            <p style="color: #a78bfa; font-size: 0.875rem; margin: 0 0 0.25rem 0;">
                ⭐ Ganarás con esta compra
            </p>
            <p style="color: #ffffff; font-size: 1.5rem; font-weight: 700; margin: 0;">
                {checkout_data['points_to_earn']} puntos
            </p>
        </div>
        """, unsafe_allow_html=True)

    # Botones de navegación
    st.markdown("<br><br>", unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1, 2, 1])

    with col1:
        if st.button("⬅️ Volver al Carrito", use_container_width=True):
            st.session_state[SESSION_KEYS["current_page"]] = "cart"
            st.rerun()

    with col3:
        if st.button("Siguiente ➡️", type="primary", use_container_width=True):
            st.session_state['checkout_step'] = 2
            st.rerun()


def render_checkout_item(item: dict):
    """
    Renderiza un item del checkout (resumen).

    Args:
        item: Diccionario del item
    """
    personalizacion = item.get('personalization')
    cantidad = item.get('quantity', 1)
    precio_total = (item.get('unit_price', 0) + item.get('personalization_price', 0)) * cantidad

    # Usar columnas para layout
    col1, col2, col3 = st.columns([1, 4, 1.5])

    with col1:
        st.image(item.get('product_image', 'https://via.placeholder.com/80'), width=80)

    with col2:
        st.markdown(f"""
        <div>
            <p style="color: #a78bfa; font-size: 0.75rem; margin: 0 0 0.25rem 0;">{item.get('team', '')}</p>
            <p style="color: #ffffff; font-weight: 600; font-size: 0.95rem; margin: 0 0 0.25rem 0;">{item.get('product_name', '')}</p>
            <p style="color: #9ca3af; font-size: 0.875rem; margin: 0;">
                Talla: {item.get('size', '-')} | Cantidad: {cantidad}
            </p>
            {f"<p style='color: #a78bfa; font-size: 0.75rem; margin: 0.25rem 0 0 0;'>✨ {personalizacion.get('nombre', '')} #{personalizacion.get('numero', '')}</p>" if personalizacion else ""}
        </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown(f"""
        <div style="text-align: right; padding-top: 0.5rem;">
            <p style="color: #a78bfa; font-size: 1.25rem; font-weight: 700; margin: 0;">
                {precio_total:.2f}€
            </p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<hr style='margin: 0.5rem 0; border-color: #2d2d3a;'>", unsafe_allow_html=True)


def render_shipping_address_step():
    """
    Paso 2: Dirección de envío.
    """
    st.markdown("## 📦 Paso 2: Dirección de Envío")

    # Inicializar datos de dirección si no existen
    if 'shipping_address' not in st.session_state:
        st.session_state['shipping_address'] = {}

    with st.form("shipping_form"):
        col1, col2 = st.columns(2)

        with col1:
            nombre = st.text_input(
                "Nombre completo *",
                value=st.session_state.get('shipping_address', {}).get('nombre', ''),
                placeholder="Juan Pérez"
            )

        with col2:
            telefono = st.text_input(
                "Teléfono *",
                value=st.session_state.get('shipping_address', {}).get('telefono', ''),
                placeholder="612345678",
                max_chars=9
            )

        direccion = st.text_input(
            "Dirección (Calle y número) *",
            value=st.session_state.get('shipping_address', {}).get('direccion', ''),
            placeholder="Calle Mayor 123, 2ºB"
        )

        col1, col2 = st.columns(2)

        with col1:
            ciudad = st.text_input(
                "Ciudad *",
                value=st.session_state.get('shipping_address', {}).get('ciudad', ''),
                placeholder="Madrid"
            )

        with col2:
            # Provincias de España
            provincias = [
                "Álava", "Albacete", "Alicante", "Almería", "Asturias", "Ávila",
                "Badajoz", "Barcelona", "Burgos", "Cáceres", "Cádiz", "Cantabria",
                "Castellón", "Ciudad Real", "Córdoba", "Cuenca", "Gerona", "Granada",
                "Guadalajara", "Guipúzcoa", "Huelva", "Huesca", "Islas Baleares",
                "Jaén", "La Coruña", "La Rioja", "Las Palmas", "León", "Lérida",
                "Lugo", "Madrid", "Málaga", "Murcia", "Navarra", "Orense", "Palencia",
                "Pontevedra", "Salamanca", "Santa Cruz de Tenerife", "Segovia",
                "Sevilla", "Soria", "Tarragona", "Teruel", "Toledo", "Valencia",
                "Valladolid", "Vizcaya", "Zamora", "Zaragoza"
            ]

            current_provincia = st.session_state.get('shipping_address', {}).get('provincia', '')
            provincia_index = provincias.index(current_provincia) if current_provincia in provincias else 0

            provincia = st.selectbox(
                "Provincia *",
                options=provincias,
                index=provincia_index
            )

        codigo_postal = st.text_input(
            "Código Postal *",
            value=st.session_state.get('shipping_address', {}).get('codigo_postal', ''),
            placeholder="28001",
            max_chars=5
        )

        # Botones del formulario
        col1, col2, col3 = st.columns([1, 2, 1])

        with col1:
            back_button = st.form_submit_button("⬅️ Volver")

        with col3:
            submit_button = st.form_submit_button("Siguiente ➡️", type="primary")

        # Procesar formulario
        if back_button:
            st.session_state['checkout_step'] = 1
            st.rerun()

        if submit_button:
            # Validar campos obligatorios
            if not all([nombre, telefono, direccion, ciudad, provincia, codigo_postal]):
                st.error("⚠️ Por favor completa todos los campos obligatorios")
            elif len(telefono) != 9 or not telefono.isdigit():
                st.error("⚠️ El teléfono debe tener 9 dígitos")
            elif len(codigo_postal) != 5 or not codigo_postal.isdigit():
                st.error("⚠️ El código postal debe tener 5 dígitos")
            else:
                # Guardar dirección
                st.session_state['shipping_address'] = {
                    'nombre': nombre,
                    'telefono': telefono,
                    'direccion': direccion,
                    'ciudad': ciudad,
                    'provincia': provincia,
                    'codigo_postal': codigo_postal
                }

                # Avanzar al siguiente paso
                st.session_state['checkout_step'] = 3
                st.rerun()


def render_payment_method_step():
    """
    Paso 3: Método de pago (SIMULADO).
    """
    st.markdown("## 💳 Paso 3: Método de Pago")

    st.info("⚠️ **SIMULACIÓN ACADÉMICA** - No se procesará ningún pago real")

    # Método de pago
    payment_method = st.radio(
        "Selecciona tu método de pago",
        options=["💳 Tarjeta de Crédito/Débito", "🏦 Transferencia Bancaria"],
        index=0
    )

    st.markdown("<br>", unsafe_allow_html=True)

    if "Tarjeta" in payment_method:
        render_card_payment_form()
    else:
        render_bank_transfer_info()

    # Botones de navegación
    st.markdown("<br><br>", unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1, 2, 1])

    with col1:
        if st.button("⬅️ Volver", use_container_width=True):
            st.session_state['checkout_step'] = 2
            st.rerun()

    with col3:
        if st.button("✅ Confirmar Pedido", type="primary", use_container_width=True):
            confirm_order(payment_method)


def render_card_payment_form():
    """
    Renderiza el formulario de pago con tarjeta (simulado).
    """
    st.markdown("### 💳 Datos de la Tarjeta")

    with st.form("payment_form"):
        card_number = st.text_input(
            "Número de tarjeta",
            placeholder="1234 5678 9012 3456",
            max_chars=19,
            help="Simulado - cualquier número válido"
        )

        col1, col2 = st.columns(2)

        with col1:
            expiry = st.text_input(
                "Fecha de expiración",
                placeholder="MM/AA",
                max_chars=5
            )

        with col2:
            cvv = st.text_input(
                "CVV",
                placeholder="123",
                max_chars=3,
                type="password"
            )

        cardholder = st.text_input(
            "Titular de la tarjeta",
            placeholder="JUAN PEREZ"
        )

        # Note: Este formulario no hace nada real, los botones están fuera
        st.form_submit_button("Guardar", disabled=True, help="Los botones principales están fuera del formulario")


def render_bank_transfer_info():
    """
    Muestra información para transferencia bancaria (simulado).
    """
    st.markdown("### 🏦 Datos para Transferencia")

    st.markdown("""
    <div style="
        background: #181633;
        border: 1px solid #2d2d3a;
        border-radius: 8px;
        padding: 1.5rem;
    ">
        <p style="color: #d1d5db; margin: 0 0 1rem 0;">
            Realiza la transferencia a la siguiente cuenta:
        </p>
        <p style="color: #ffffff; margin: 0.5rem 0;">
            <strong>Banco:</strong> Banco SportStyle
        </p>
        <p style="color: #ffffff; margin: 0.5rem 0;">
            <strong>IBAN:</strong> ES12 3456 7890 1234 5678 9012
        </p>
        <p style="color: #ffffff; margin: 0.5rem 0;">
            <strong>Concepto:</strong> Pedido SportStyle
        </p>
        <p style="color: #9ca3af; font-size: 0.875rem; margin: 1rem 0 0 0;">
            💡 Una vez confirmado el pedido, recibirás un email con los detalles.
        </p>
    </div>
    """, unsafe_allow_html=True)


def confirm_order(payment_method: str):
    """
    Confirma el pedido y guarda en session_state.

    Args:
        payment_method: Método de pago seleccionado
    """
    checkout_data = st.session_state.get('checkout_data')
    shipping_address = st.session_state.get('shipping_address')

    if not checkout_data or not shipping_address:
        st.error("❌ Faltan datos para completar el pedido")
        return

    # Generar número de pedido
    order_number = generate_order_number()

    # Crear pedido
    order = {
        'order_number': order_number,
        'date': datetime.now().isoformat(),
        'items': checkout_data['cart'],
        'subtotal': checkout_data['subtotal'],
        'shipping': checkout_data['shipping'],
        'discount': checkout_data['discount'],
        'total': checkout_data['total'],
        'points_earned': checkout_data['points_to_earn'],
        'points_used': checkout_data.get('points_used', 0),
        'shipping_address': shipping_address,
        'payment_method': payment_method,
        'status': 'confirmado'
    }

    # Guardar pedido en session_state
    if 'orders' not in st.session_state:
        st.session_state['orders'] = []

    st.session_state['orders'].append(order)

    # Actualizar puntos del usuario (simulado)
    current_points = st.session_state.get('user_points', 0)
    new_points = current_points + order['points_earned'] - order['points_used']
    st.session_state['user_points'] = new_points

    # Guardar número de pedido para la página de confirmación
    st.session_state['last_order_number'] = order_number

    # Guardar el pedido para mostrar en el modal
    # NO limpiamos el carrito ni checkout_data todavía - se hará después del modal
    st.session_state['show_order_modal'] = True
    st.session_state['modal_order'] = order

    # Mostrar balloons
    st.balloons()
    st.rerun()


def generate_order_number() -> str:
    """
    Genera un número de pedido único.

    Returns:
        str: Número de pedido formato ORD-YYYYMMDD-NNNN
    """
    date_str = datetime.now().strftime("%Y%m%d")
    orders_today = len([o for o in st.session_state.get('orders', []) if date_str in o.get('order_number', '')])
    order_num = f"ORD-{date_str}-{orders_today + 1:04d}"
    return order_num


def render_order_confirmation_modal(order: dict):
    """
    Renderiza modal de confirmación de pedido con animación y resumen.

    Args:
        order: Diccionario con datos del pedido
    """
    order_number = order.get('order_number', 'N/A')
    items = order.get('items', [])
    total = order.get('total', 0)
    points_earned = order.get('points_earned', 0)

    # Modal simplificado usando contenedores de Streamlit
    st.markdown("<br><br>", unsafe_allow_html=True)

    # Contenedor centrado
    col1, col2, col3 = st.columns([1, 3, 1])

    with col2:
        st.markdown("""
        <div style="
            background: linear-gradient(135deg, #1e1b4b 0%, #181633 100%);
            border: 3px solid #a78bfa;
            border-radius: 16px;
            padding: 2.5rem;
            text-align: center;
            box-shadow: 0 20px 60px rgba(167, 139, 250, 0.5);
        ">
            <div style="font-size: 5rem; margin-bottom: 1rem;">✅</div>
            <h1 style="color: #ffffff; font-size: 2rem; margin: 0 0 0.5rem 0;">¡Pedido Procesado!</h1>
            <p style="color: #a78bfa; font-size: 1.2rem; font-weight: 600; margin: 0 0 2rem 0;">#""" + order_number + """</p>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

        # Sección de productos
        st.markdown("""
        <div style="
            background: rgba(45, 45, 58, 0.5);
            border: 1px solid rgba(167, 139, 250, 0.2);
            border-radius: 12px;
            padding: 1.5rem;
        ">
            <h3 style="color: #a78bfa; margin: 0 0 1rem 0; font-size: 1.1rem;">📦 Resumen del Pedido</h3>
        """, unsafe_allow_html=True)

        # Listar productos
        for i, item in enumerate(items[:3]):
            name = item.get('product_name', 'Producto')
            cantidad = item.get('quantity', 1)
            st.markdown(f"""
            <p style="color: #d1d5db; margin: 0.5rem 0; font-size: 1rem;">
                • {cantidad}x {name}
            </p>
            """, unsafe_allow_html=True)

        if len(items) > 3:
            st.markdown(f"""
            <p style="color: #9ca3af; margin: 0.5rem 0; font-size: 0.9rem; font-style: italic;">
                ... y {len(items) - 3} producto(s) más
            </p>
            """, unsafe_allow_html=True)

        # Total
        st.markdown(f"""
            <hr style="border: 0; border-top: 2px solid rgba(167, 139, 250, 0.3); margin: 1.5rem 0;">
            <div style="display: flex; justify-content: space-between; align-items: center;">
                <span style="color: #ffffff; font-size: 1.2rem; font-weight: 700;">TOTAL:</span>
                <span style="color: #a78bfa; font-size: 2rem; font-weight: 700;">{total:.2f}€</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

        # Puntos ganados
        st.markdown(f"""
        <div style="
            background: rgba(16, 185, 129, 0.15);
            border: 2px solid #10b981;
            border-radius: 12px;
            padding: 1.5rem;
            text-align: center;
            margin-top: 1rem;
        ">
            <p style="color: #10b981; font-size: 1.3rem; font-weight: 600; margin: 0;">
                ✨ Has ganado {points_earned} puntos
            </p>
        </div>
        """, unsafe_allow_html=True)
