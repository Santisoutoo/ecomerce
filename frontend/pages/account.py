"""
Página de cuenta de usuario.
Muestra información personal, historial de pedidos, puntos y favoritos.
"""

import streamlit as st
from datetime import datetime
from typing import List, Dict
from config import SESSION_KEYS
from services.product_service import ProductService
from services.auth_service import AuthService


def render_account_page():
    """
    Renderiza la página de cuenta del usuario con tabs.
    """
    st.title("👤 Mi Cuenta")

    # Obtener información del usuario
    user_email = st.session_state.get(SESSION_KEYS["user_email"], "No disponible")
    user_id = st.session_state.get(SESSION_KEYS["user_id"], "No disponible")

    # Header con info básica
    render_account_header(user_email, user_id)

    # Tabs para organizar secciones
    tab1, tab2, tab3, tab4 = st.tabs([
        "📦 Mis Pedidos",
        "🎁 Puntos de Fidelización",
        "❤️ Favoritos",
        "⚙️ Configuración"
    ])

    with tab1:
        render_orders_section()

    with tab2:
        render_points_section()

    with tab3:
        render_favorites_section()

    with tab4:
        render_settings_section(user_email, user_id)


def render_account_header(user_email: str, user_id: str):
    """
    Renderiza el header de la cuenta con resumen.

    Args:
        user_email: Email del usuario
        user_id: ID del usuario
    """
    st.markdown("""
    <style>
        .account-header {
            background: linear-gradient(135deg, #1e1b4b 0%, #2d2d3a 100%);
            border: 2px solid #a78bfa;
            border-radius: 16px;
            padding: 2rem;
            margin-bottom: 2rem;
        }
    </style>
    """, unsafe_allow_html=True)

    # Perfil y estadísticas
    col_avatar, col_stats = st.columns([1, 4])

    with col_avatar:
        # Mostrar avatar del usuario
        user_foto = st.session_state.get('user_foto_perfil', '')
        if user_foto:
            st.image(user_foto, width=120)
        else:
            st.markdown("""
            <div style="
                width: 120px;
                height: 120px;
                border-radius: 50%;
                background: linear-gradient(135deg, #a78bfa 0%, #7c3aed 100%);
                display: flex;
                align-items: center;
                justify-content: center;
                font-size: 3rem;
            ">
                👤
            </div>
            """, unsafe_allow_html=True)

    with col_stats:
        # Estadísticas rápidas
        col1, col2, col3, col4 = st.columns(4)

        orders = st.session_state.get('orders', [])
        user_points = st.session_state.get('user_points', 0)
        favorites = st.session_state.get('favorites', [])

        with col1:
            st.metric("📧 Email", user_email)

        with col2:
            st.metric("📦 Pedidos Totales", len(orders))

        with col3:
            st.metric("🎁 Puntos Disponibles", user_points)

        with col4:
            st.metric("❤️ Favoritos", len(favorites))

    st.markdown("---")


def render_orders_section():
    """
    Renderiza la sección de historial de pedidos.
    """
    st.markdown("### 📦 Historial de Pedidos")

    orders = st.session_state.get('orders', [])

    if not orders:
        render_empty_orders()
        return

    # Ordenar pedidos por fecha (más reciente primero)
    sorted_orders = sorted(
        orders,
        key=lambda x: x.get('date', ''),
        reverse=True
    )

    st.markdown(f"**{len(orders)} pedido{'s' if len(orders) != 1 else ''} realizado{'s' if len(orders) != 1 else ''}**")
    st.markdown("<br>", unsafe_allow_html=True)

    # Mostrar cada pedido
    for order in sorted_orders:
        render_order_card(order)


def render_empty_orders():
    """
    Renderiza mensaje cuando no hay pedidos.
    """
    st.markdown("""
    <div style="
        background: #181633;
        border: 2px dashed #2d2d3a;
        border-radius: 16px;
        padding: 3rem;
        text-align: center;
        margin: 2rem 0;
    ">
        <p style="font-size: 4rem; margin: 0;">📦</p>
        <h3 style="color: #a78bfa; margin: 1rem 0;">No tienes pedidos todavía</h3>
        <p style="color: #9ca3af; margin: 0;">
            ¡Explora nuestro catálogo y realiza tu primera compra!
        </p>
    </div>
    """, unsafe_allow_html=True)

    if st.button("🛍️ Ir al Catálogo", type="primary", use_container_width=True):
        st.session_state[SESSION_KEYS["current_page"]] = "catalog"
        st.rerun()


def render_order_card(order: dict):
    """
    Renderiza una tarjeta de pedido.

    Args:
        order: Diccionario con información del pedido
    """
    order_number = order.get('order_number', 'N/A')
    date_str = order.get('date', datetime.now().isoformat())
    status = order.get('status', 'pendiente')
    total = order.get('total', 0)
    items = order.get('items', [])

    # Formatear fecha
    try:
        date_obj = datetime.fromisoformat(date_str)
        formatted_date = date_obj.strftime('%d/%m/%Y %H:%M')
    except:
        formatted_date = date_str

    # Color del estado
    status_colors = {
        'confirmado': '#10b981',
        'en_proceso': '#f59e0b',
        'enviado': '#3b82f6',
        'entregado': '#10b981',
        'cancelado': '#ef4444'
    }
    status_color = status_colors.get(status, '#9ca3af')

    with st.container():
        # Abrir contenedor principal
        st.markdown("""
        <div style="
            background: #181633;
            border: 1px solid #2d2d3a;
            border-radius: 12px;
            padding: 1.5rem;
            margin-bottom: 1rem;
            transition: all 0.3s;
        ">
        """, unsafe_allow_html=True)

        # Abrir header flex
        st.markdown("""
            <div style="display: flex; justify-content: space-between; align-items: start; margin-bottom: 1rem;">
                <div>
        """, unsafe_allow_html=True)

        # Número de pedido
        st.markdown(f"""
                    <p style="color: #a78bfa; font-weight: 600; font-size: 1rem; margin: 0;">
                        Pedido #{order_number}
                    </p>
        """, unsafe_allow_html=True)

        # Fecha
        st.markdown(f"""
                    <p style="color: #9ca3af; font-size: 0.875rem; margin: 0.25rem 0 0 0;">
                        {formatted_date}
                    </p>
                </div>
                <div>
        """, unsafe_allow_html=True)

        # Estado badge
        status_text = status.replace('_', ' ').capitalize()
        st.markdown(f"""
                    <span style="
                        background: {status_color}20;
                        color: {status_color};
                        padding: 0.5rem 1rem;
                        border-radius: 8px;
                        font-size: 0.875rem;
                        font-weight: 600;
                    ">
                        {status_text}
                    </span>
                </div>
            </div>
        """, unsafe_allow_html=True)

        # Separador y resumen
        st.markdown("""
            <div style="border-top: 1px solid #2d2d3a; padding-top: 1rem; margin-bottom: 1rem;">
        """, unsafe_allow_html=True)

        # Productos y total
        productos_text = f"{len(items)} producto" + ("s" if len(items) != 1 else "")
        st.markdown(f"""
                <p style="color: #d1d5db; font-size: 0.875rem; margin: 0 0 0.5rem 0;">
                    <strong>{productos_text}</strong> ·
                    Total: <strong style="color: #a78bfa; font-size: 1.1rem;">{total:.2f}€</strong>
                </p>
            </div>
        """, unsafe_allow_html=True)

        # Cerrar contenedor principal
        st.markdown("</div>", unsafe_allow_html=True)

        # Mostrar productos del pedido (colapsable)
        with st.expander(f"Ver productos ({len(items)})"):
            for item in items:
                col1, col2, col3, col4 = st.columns([1, 3, 1, 1])

                with col1:
                    st.image(item.get('imagen_url', 'https://via.placeholder.com/100'), width=80)

                with col2:
                    st.markdown(f"**{item.get('name', 'Producto')}**")
                    st.caption(f"Talla: {item.get('talla', 'N/A')}")
                    if item.get('personalizacion'):
                        pers = item['personalizacion']
                        st.caption(f"✨ {pers.get('nombre', '')} #{pers.get('numero', '')}")

                with col3:
                    st.markdown(f"x{item.get('cantidad', 1)}")

                with col4:
                    st.markdown(f"**{item.get('precio_total', 0):.2f}€**")

        st.markdown("<br>", unsafe_allow_html=True)


def render_points_section():
    """
    Renderiza la sección de puntos de fidelización.
    """
    st.markdown("### 🎁 Puntos de Fidelización")

    user_points = st.session_state.get('user_points', 0)

    # Card de saldo de puntos
    col1, col2 = st.columns([2, 1])

    with col1:
        st.markdown(f"""
        <div style="
            background: linear-gradient(135deg, #1e1b4b 0%, #2d2d3a 100%);
            border: 2px solid #a78bfa;
            border-radius: 16px;
            padding: 2rem;
            text-align: center;
        ">
            <p style="color: #9ca3af; font-size: 0.9rem; margin: 0 0 0.5rem 0;">Puntos Disponibles</p>
            <p style="color: #a78bfa; font-size: 3rem; font-weight: 700; margin: 0;">
                {user_points}
            </p>
            <p style="color: #d1d5db; font-size: 0.9rem; margin: 1rem 0 0 0;">
                = {user_points / 100:.2f}€ en descuentos
            </p>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div style="
            background: #181633;
            border: 1px solid #2d2d3a;
            border-radius: 12px;
            padding: 1.5rem;
        ">
            <p style="color: #a78bfa; font-weight: 600; margin: 0 0 1rem 0;">💡 ¿Cómo funciona?</p>
            <p style="color: #d1d5db; font-size: 0.875rem; margin: 0 0 0.5rem 0;">
                • 1€ gastado = 10 puntos
            </p>
            <p style="color: #d1d5db; font-size: 0.875rem; margin: 0 0 0.5rem 0;">
                • 100 puntos = 1€ descuento
            </p>
            <p style="color: #d1d5db; font-size: 0.875rem; margin: 0;">
                • Máximo 50% por pedido
            </p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")

    # Historial de puntos
    st.markdown("### 📊 Historial de Puntos")

    orders = st.session_state.get('orders', [])

    if not orders:
        st.info("No hay movimientos de puntos todavía")
    else:
        render_points_history(orders)


def render_points_history(orders: List[Dict]):
    """
    Renderiza el historial de movimientos de puntos.

    Args:
        orders: Lista de pedidos
    """
    # Crear tabla de movimientos
    movements = []

    for order in orders:
        date_str = order.get('date', datetime.now().isoformat())
        try:
            date_obj = datetime.fromisoformat(date_str)
            formatted_date = date_obj.strftime('%d/%m/%Y')
        except:
            formatted_date = date_str

        # Puntos ganados
        points_earned = order.get('points_earned', 0)
        if points_earned > 0:
            movements.append({
                'date': formatted_date,
                'description': f"Pedido #{order.get('order_number', 'N/A')}",
                'points': f"+{points_earned}",
                'color': '#10b981'
            })

        # Puntos usados
        points_used = order.get('points_used', 0)
        if points_used > 0:
            movements.append({
                'date': formatted_date,
                'description': f"Descuento en pedido #{order.get('order_number', 'N/A')}",
                'points': f"-{points_used}",
                'color': '#ef4444'
            })

    # Ordenar por fecha
    movements.reverse()

    # Mostrar movimientos
    for movement in movements:
        st.markdown(f"""
        <div style="
            background: #181633;
            border-left: 3px solid {movement['color']};
            border-radius: 8px;
            padding: 1rem;
            margin-bottom: 0.5rem;
            display: flex;
            justify-content: space-between;
            align-items: center;
        ">
            <div>
                <p style="color: #d1d5db; margin: 0; font-weight: 600;">{movement['description']}</p>
                <p style="color: #9ca3af; font-size: 0.875rem; margin: 0.25rem 0 0 0;">{movement['date']}</p>
            </div>
            <div>
                <p style="color: {movement['color']}; font-size: 1.25rem; font-weight: 700; margin: 0;">
                    {movement['points']}
                </p>
            </div>
        </div>
        """, unsafe_allow_html=True)


def render_favorites_section():
    """
    Renderiza la sección de productos favoritos.
    """
    st.markdown("### ❤️ Mis Favoritos")

    favorites = st.session_state.get('favorites', [])

    if not favorites:
        render_empty_favorites()
        return

    st.markdown(f"**{len(favorites)} producto{'s' if len(favorites) != 1 else ''} guardado{'s' if len(favorites) != 1 else ''}**")
    st.markdown("<br>", unsafe_allow_html=True)

    # Obtener información de productos favoritos
    favorite_products = []
    for product_id in favorites:
        product = ProductService.get_product_by_id(product_id)
        if product:
            favorite_products.append(product)

    # Grid de favoritos
    cols_per_row = 3
    for i in range(0, len(favorite_products), cols_per_row):
        cols = st.columns(cols_per_row)

        for j, col in enumerate(cols):
            idx = i + j
            if idx < len(favorite_products):
                with col:
                    render_favorite_card(favorite_products[idx], idx)


def render_empty_favorites():
    """
    Renderiza mensaje cuando no hay favoritos.
    """
    st.markdown("""
    <div style="
        background: #181633;
        border: 2px dashed #2d2d3a;
        border-radius: 16px;
        padding: 3rem;
        text-align: center;
        margin: 2rem 0;
    ">
        <p style="font-size: 4rem; margin: 0;">❤️</p>
        <h3 style="color: #a78bfa; margin: 1rem 0;">No tienes favoritos todavía</h3>
        <p style="color: #9ca3af; margin: 0;">
            Guarda tus productos favoritos para encontrarlos fácilmente
        </p>
    </div>
    """, unsafe_allow_html=True)

    if st.button("🛍️ Explorar Productos", type="primary", use_container_width=True):
        st.session_state[SESSION_KEYS["current_page"]] = "catalog"
        st.rerun()


def render_favorite_card(product: dict, index: int):
    """
    Renderiza una tarjeta de producto favorito.

    Args:
        product: Diccionario del producto
        index: Índice del producto
    """
    # Contenedor de la tarjeta
    with st.container():
        # Imagen
        st.image(
            product.get('imagen_url', 'https://via.placeholder.com/200')
        )

        # Info del producto
        st.markdown(f"""
        <div style="text-align: center; padding: 0.5rem 0;">
            <p style="color: #a78bfa; font-size: 0.75rem; margin: 0 0 0.25rem 0;">
                {product.get('equipo', '')}
            </p>
            <p style="color: #ffffff; font-weight: 600; font-size: 0.9rem; margin: 0 0 0.5rem 0;">
                {product.get('name', 'Producto')}
            </p>
            <p style="color: #a78bfa; font-size: 1.25rem; font-weight: 700; margin: 0;">
                {product.get('precio', 0):.2f}€
            </p>
        </div>
        """, unsafe_allow_html=True)

        # Botones
        col1, col2 = st.columns(2)

        with col1:
            if st.button("👁️ Ver", key=f"view_fav_{index}", use_container_width=True):
                st.session_state['selected_product'] = product.get('id')
                st.session_state[SESSION_KEYS["current_page"]] = "product_detail"
                st.rerun()

        with col2:
            if st.button("🗑️", key=f"remove_fav_{index}", use_container_width=True, type="secondary"):
                remove_from_favorites(product.get('id'))

        st.markdown("<hr style='margin: 1rem 0; border-color: #2d2d3a;'>", unsafe_allow_html=True)


def remove_from_favorites(product_id: str):
    """
    Elimina un producto de favoritos.

    Args:
        product_id: ID del producto a eliminar
    """
    if 'favorites' not in st.session_state:
        return

    if product_id in st.session_state['favorites']:
        st.session_state['favorites'].remove(product_id)
        st.success("❤️ Producto eliminado de favoritos")
        st.rerun()


def render_settings_section(user_email: str, user_id: str):
    """
    Renderiza la sección de configuración.

    Args:
        user_email: Email del usuario
        user_id: ID del usuario
    """
    st.markdown("### ⚙️ Configuración de Cuenta")

    # Información personal
    st.markdown("#### 👤 Información Personal")

    col1, col2 = st.columns(2)

    with col1:
        st.text_input("Email", value=user_email, disabled=True)

    with col2:
        st.text_input("ID de Usuario", value=user_id, disabled=True)

    st.markdown("---")

    # Foto de perfil
    st.markdown("#### 📸 Foto de Perfil")

    col_img, col_upload = st.columns([1, 2])

    with col_img:
        # Mostrar foto actual
        user_foto = st.session_state.get('user_foto_perfil', '')
        if user_foto:
            st.image(user_foto, width=150, caption="Foto actual")
        else:
            st.markdown("""
            <div style="
                width: 150px;
                height: 150px;
                border-radius: 50%;
                background: linear-gradient(135deg, #a78bfa 0%, #7c3aed 100%);
                display: flex;
                align-items: center;
                justify-content: center;
                font-size: 4rem;
            ">
                👤
            </div>
            """, unsafe_allow_html=True)

    with col_upload:
        st.markdown("**Subir nueva foto**")
        st.caption("Formatos: JPG, PNG. Tamaño máximo: 5MB")

        uploaded_file = st.file_uploader(
            "Selecciona una imagen",
            type=["jpg", "jpeg", "png"],
            key="profile_picture_upload",
            label_visibility="collapsed"
        )

        if uploaded_file is not None:
            # Validar tamaño (máximo 5MB)
            file_size_mb = uploaded_file.size / (1024 * 1024)

            if file_size_mb > 5:
                st.error("❌ La imagen es demasiado grande. Máximo 5MB.")
            else:
                # Mostrar botón para confirmar subida
                if st.button("📤 Subir Foto", type="primary", use_container_width=True):
                    with st.spinner("Subiendo imagen..."):
                        # Obtener token de acceso
                        access_token = st.session_state.get(SESSION_KEYS["access_token"])

                        if not access_token:
                            st.error("❌ No se encontró el token de acceso. Por favor, inicia sesión nuevamente.")
                        else:
                            # Subir imagen
                            success, url, error = AuthService.upload_profile_picture(uploaded_file, access_token)

                            if success and url:
                                # Actualizar session state
                                st.session_state['user_foto_perfil'] = url
                                st.success("✅ Foto de perfil actualizada correctamente")
                                st.rerun()
                            else:
                                st.error(f"❌ {error or 'Error al subir la imagen'}")

    st.markdown("---")

    # Direcciones guardadas
    st.markdown("#### 📍 Direcciones Guardadas")

    saved_addresses = st.session_state.get('saved_addresses', [])

    if saved_addresses:
        for i, address in enumerate(saved_addresses):
            st.markdown(f"""
            <div style="
                background: #181633;
                border: 1px solid #2d2d3a;
                border-radius: 8px;
                padding: 1rem;
                margin-bottom: 0.5rem;
            ">
                <p style="color: #ffffff; font-weight: 600; margin: 0;">{address.get('nombre', '')} {address.get('apellidos', '')}</p>
                <p style="color: #d1d5db; margin: 0.25rem 0 0 0;">{address.get('direccion', '')}</p>
                <p style="color: #d1d5db; margin: 0.25rem 0 0 0;">
                    {address.get('codigo_postal', '')} - {address.get('ciudad', '')}, {address.get('provincia', '')}
                </p>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.info("No tienes direcciones guardadas. Se guardarán automáticamente al hacer un pedido.")

    st.markdown("---")

    # Preferencias
    st.markdown("#### 🔔 Preferencias")

    st.checkbox("Recibir emails de promociones", value=True)
    st.checkbox("Notificaciones de nuevos productos", value=True)
    st.checkbox("Alertas de descuentos personalizados", value=True)

    st.markdown("<br>", unsafe_allow_html=True)

    if st.button("💾 Guardar Preferencias", type="primary", use_container_width=True):
        st.success("✅ Preferencias guardadas correctamente")
