"""
Página de detalle de producto.
Muestra información completa, galería, personalización y opciones de compra.
"""

import streamlit as st
from services.product_service import ProductService
from services.cart_service import CartService
from components.navbar import show_success_toast, show_error_toast, show_info_toast
from config import SESSION_KEYS


def render_product_detail_page():
    """
    Renderiza la página de detalle de un producto.
    """
    # Obtener ID del producto desde session_state
    product_id = st.session_state.get("selected_product")

    if not product_id:
        show_error_toast("❌ No se ha seleccionado ningún producto")
        if st.button("🏠 Volver al inicio"):
            st.session_state[SESSION_KEYS["current_page"]] = "home"
            st.rerun()
        return

    # Obtener producto
    product = ProductService.get_product_by_id(product_id)

    if not product:
        show_error_toast("❌ Producto no encontrado")
        if st.button("🏠 Volver al inicio"):
            st.session_state[SESSION_KEYS["current_page"]] = "home"
            st.rerun()
        return

    # Renderizar detalle
    render_product_header(product)

    # Layout de 2 columnas
    col_left, col_right = st.columns([1, 1], gap="large")

    with col_left:
        render_product_gallery(product)

    with col_right:
        render_product_info(product)


def render_product_header(product: dict):
    """
    Renderiza el header con navegación breadcrumb.

    Args:
        product: Diccionario del producto
    """
    # Breadcrumb navigation
    col1, col2 = st.columns([3, 1])

    with col1:
        st.markdown(f"""
        <div style="
            color: #9ca3af;
            font-size: 0.9rem;
            margin-bottom: 1rem;
        ">
            <a href="#" style="color: #a78bfa; text-decoration: none;">Home</a>
            <span style="margin: 0 0.5rem;">/</span>
            <a href="#" style="color: #a78bfa; text-decoration: none;">{product.get('deporte', '').capitalize()}</a>
            <span style="margin: 0 0.5rem;">/</span>
            <span>{product.get('equipo', '')}</span>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        if st.button("⬅️ Volver", type="secondary", use_container_width=True):
            st.session_state[SESSION_KEYS["current_page"]] = "home"
            st.rerun()


def render_product_gallery(product: dict):
    """
    Renderiza la galería de imágenes del producto.

    Args:
        product: Diccionario del producto
    """
    # Imagen principal
    st.markdown(f"""
    <div style="
        background: #1e1b4b;
        border: 2px solid #2d2d3a;
        border-radius: 16px;
        padding: 2rem;
        text-align: center;
    ">
        <img src="{product.get('imagen_url', 'https://via.placeholder.com/600')}"
             style="
                width: 100%;
                max-width: 500px;
                border-radius: 12px;
             "
             alt="{product.get('name', 'Producto')}">
    </div>
    """, unsafe_allow_html=True)

    # Miniaturas (placeholder - en el futuro con múltiples imágenes)
    st.markdown("<br>", unsafe_allow_html=True)

    cols = st.columns(4)
    for i, col in enumerate(cols):
        with col:
            st.markdown(f"""
            <div style="
                background: #181633;
                border: 1px solid #2d2d3a;
                border-radius: 8px;
                padding: 0.5rem;
                cursor: pointer;
                text-align: center;
            ">
                <img src="{product.get('imagen_url', 'https://via.placeholder.com/150')}"
                     style="width: 100%; border-radius: 4px; opacity: 0.6;"
                     alt="Vista {i+1}">
            </div>
            """, unsafe_allow_html=True)


def render_product_info(product: dict):
    """
    Renderiza la información y opciones de compra del producto.

    Args:
        product: Diccionario del producto
    """
    # Título y equipo
    st.markdown(f"""
    <div style="margin-bottom: 1rem;">
        <p style="color: #a78bfa; font-size: 0.9rem; margin: 0 0 0.5rem 0; font-weight: 600;">
            {product.get('equipo', 'Equipo')}
        </p>
        <h1 style="color: #ffffff; margin: 0 0 1rem 0; font-size: 2rem;">
            {product.get('name', 'Producto sin nombre')}
        </h1>
    </div>
    """, unsafe_allow_html=True)

    # Badge de categoría
    st.markdown(f"""
    <span style="
        background: #2d2d3a;
        color: #d1d5db;
        padding: 0.5rem 1rem;
        border-radius: 8px;
        font-size: 0.875rem;
        display: inline-block;
        margin-bottom: 1.5rem;
    ">
        {product.get('categoria', 'Categoría')}
    </span>
    """, unsafe_allow_html=True)

    # Descripción
    st.markdown(f"""
    <p style="color: #d1d5db; line-height: 1.6; margin-bottom: 1.5rem;">
        {product.get('descripcion', 'Producto oficial de alta calidad. Materiales premium y diseño exclusivo.')}
    </p>
    """, unsafe_allow_html=True)

    # Precio base
    precio_base = product.get('precio', 0)
    st.markdown(f"""
    <div style="
        background: linear-gradient(135deg, #1e1b4b 0%, #2d2d3a 100%);
        border: 2px solid #a78bfa;
        border-radius: 12px;
        padding: 1.5rem;
        margin-bottom: 1.5rem;
    ">
        <p style="color: #9ca3af; font-size: 0.9rem; margin: 0 0 0.5rem 0;">Precio base</p>
        <p style="color: #a78bfa; font-size: 2.5rem; font-weight: 700; margin: 0;">
            {precio_base:.2f}€
        </p>
    </div>
    """, unsafe_allow_html=True)

    # Stock
    stock = product.get('stock', 0)
    stock_color = "#10b981" if stock > 10 else "#f59e0b" if stock > 0 else "#ef4444"
    stock_text = f"✅ {stock} unidades disponibles" if stock > 10 else f"⚠️ Últimas {stock} unidades" if stock > 0 else "❌ Agotado"

    st.markdown(f"""
    <p style="color: {stock_color}; font-weight: 600; margin-bottom: 1.5rem;">
        {stock_text}
    </p>
    """, unsafe_allow_html=True)

    # Separador
    st.markdown("---")

    # Selector de talla
    render_size_selector(product)

    # Personalización (si aplica)
    precio_personalizacion = 0
    if product.get('permite_personalizacion'):
        precio_personalizacion = render_customization_form(product)

    # Separador
    st.markdown("---")

    # Resumen de precio total
    render_price_summary(precio_base, precio_personalizacion)

    # Botones de acción
    render_action_buttons(product, stock)


def render_size_selector(product: dict):
    """
    Renderiza el selector de tallas.

    Args:
        product: Diccionario del producto
    """
    st.markdown("### 📏 Selecciona tu Talla")

    tallas = product.get('tallas', [])

    if not tallas:
        st.warning("⚠️ No hay tallas disponibles")
        return

    # Inicializar talla seleccionada
    if 'selected_size' not in st.session_state:
        st.session_state['selected_size'] = tallas[0]

    # Selector de talla con botones
    cols = st.columns(len(tallas))

    for i, talla in enumerate(tallas):
        with cols[i]:
            is_selected = st.session_state.get('selected_size') == talla

            if st.button(
                talla,
                key=f"size_{talla}",
                use_container_width=True,
                type="primary" if is_selected else "secondary"
            ):
                st.session_state['selected_size'] = talla


def render_customization_form(product: dict) -> float:
    """
    Renderiza el formulario de personalización.

    Args:
        product: Diccionario del producto

    Returns:
        float: Precio adicional de personalización
    """
    st.markdown("### ✨ Personalización")

    precio_extra = product.get('precio_personalizacion', 0)

    st.markdown(f"""
    <div style="
        background: #181633;
        border: 1px solid #a78bfa;
        border-radius: 8px;
        padding: 1rem;
        margin-bottom: 1rem;
    ">
        <p style="color: #a78bfa; margin: 0; font-size: 0.9rem;">
            💡 Agrega nombre y número por solo <strong>{precio_extra:.2f}€</strong>
        </p>
    </div>
    """, unsafe_allow_html=True)

    # Checkbox para activar personalización
    add_customization = st.checkbox(
        "Quiero personalizar mi producto",
        key="enable_customization"
    )

    if add_customization:
        col1, col2 = st.columns(2)

        with col1:
            nombre_custom = st.text_input(
                "Nombre",
                placeholder="Ej: RONALDO",
                max_chars=15,
                key="custom_name",
                help="Máximo 15 caracteres"
            )

        with col2:
            numero_custom = st.number_input(
                "Número",
                min_value=0,
                max_value=99,
                value=10,
                step=1,
                key="custom_number"
            )

        return precio_extra if nombre_custom or numero_custom else 0

    return 0


def render_price_summary(precio_base: float, precio_personalizacion: float):
    """
    Renderiza el resumen de precios.

    Args:
        precio_base: Precio base del producto
        precio_personalizacion: Precio adicional de personalización
    """
    st.markdown("### 💰 Resumen de Precio")

    # Precio base
    st.markdown(f"""
    <div style="display: flex; justify-content: space-between; margin-bottom: 0.5rem;">
        <span style="color: #d1d5db;">Precio base:</span>
        <span style="color: #ffffff; font-weight: 600;">{precio_base:.2f}€</span>
    </div>
    """, unsafe_allow_html=True)

    # Personalización (si aplica)
    if precio_personalizacion > 0:
        st.markdown(f"""
        <div style="display: flex; justify-content: space-between; margin-bottom: 0.5rem;">
            <span style="color: #d1d5db;">Personalización:</span>
            <span style="color: #a78bfa; font-weight: 600;">+{precio_personalizacion:.2f}€</span>
        </div>
        """, unsafe_allow_html=True)

    # Total
    total = precio_base + precio_personalizacion

    st.markdown(f"""
    <div style="
        display: flex;
        justify-content: space-between;
        padding-top: 1rem;
        border-top: 2px solid #2d2d3a;
        margin-top: 1rem;
    ">
        <span style="color: #ffffff; font-size: 1.25rem; font-weight: 700;">TOTAL:</span>
        <span style="color: #a78bfa; font-size: 1.5rem; font-weight: 700;">{total:.2f}€</span>
    </div>
    """, unsafe_allow_html=True)


def render_action_buttons(product: dict, stock: int):
    """
    Renderiza los botones de acción (agregar al carrito, favoritos).

    Args:
        product: Diccionario del producto
        stock: Stock disponible
    """
    st.markdown("<br>", unsafe_allow_html=True)

    col1, col2 = st.columns([3, 1])

    with col1:
        # Botón agregar al carrito
        if stock > 0:
            if st.button(
                "🛒 Agregar al Carrito",
                type="primary",
                use_container_width=True,
                key="add_to_cart_detail"
            ):
                add_to_cart(product)
        else:
            st.button(
                "❌ Producto Agotado",
                disabled=True,
                use_container_width=True
            )

    with col2:
        # Botón agregar a favoritos
        if st.button("❤️", use_container_width=True, key="add_to_favorites"):
            add_to_favorites(product)


def add_to_cart(product: dict):
    """
    Agrega el producto al carrito con las opciones seleccionadas.

    Args:
        product: Diccionario del producto
    """
    # Obtener opciones seleccionadas
    talla = st.session_state.get('selected_size')
    cantidad = 1  # Por ahora cantidad fija de 1

    # Personalización
    personalizacion = None
    if st.session_state.get('enable_customization'):
        nombre = st.session_state.get('custom_name', '')
        numero = st.session_state.get('custom_number', 0)
        if nombre or numero:
            personalizacion = {
                'nombre': nombre,
                'numero': numero
            }

    # Agregar al carrito usando el servicio
    try:
        CartService.add_to_cart(
            product_id=product.get('id'),
            quantity=cantidad,
            size=talla,
            personalization=personalizacion
        )

        # Mostrar mensaje de éxito con animación elegante
        show_success_toast(f"✅ {product.get('name')} agregado al carrito")
        show_elegant_add_animation()

    except Exception as e:
        show_error_toast(f"Error al agregar al carrito: {str(e)}")


def show_elegant_add_animation():
    """
    Muestra una animación elegante al agregar un producto al carrito.
    Usa los colores de la aplicación y un efecto de confeti sutil.
    """
    st.markdown("""
    <style>
    @keyframes fadeInOut {
        0% { opacity: 0; transform: translateY(-20px); }
        15% { opacity: 1; transform: translateY(0); }
        85% { opacity: 1; transform: translateY(0); }
        100% { opacity: 0; transform: translateY(-20px); }
    }

    @keyframes confetti {
        0% { transform: translateY(0) rotate(0deg); opacity: 1; }
        100% { transform: translateY(100vh) rotate(360deg); opacity: 0; }
    }

    .success-notification {
        position: fixed;
        top: 80px;
        right: 20px;
        background: linear-gradient(135deg, #a78bfa 0%, #8b5cf6 100%);
        color: white;
        padding: 1rem 1.5rem;
        border-radius: 12px;
        box-shadow: 0 10px 40px rgba(167, 139, 250, 0.4);
        animation: fadeInOut 3s ease-in-out;
        z-index: 9999;
        font-weight: 600;
        border: 2px solid rgba(255, 255, 255, 0.3);
    }

    .confetti-piece {
        position: fixed;
        width: 10px;
        height: 10px;
        background: #a78bfa;
        top: -10px;
        opacity: 0;
        animation: confetti 3s ease-out;
        z-index: 9998;
    }
    </style>

    <div class="success-notification">
        🎉 ¡Agregado con éxito!
    </div>

    """, unsafe_allow_html=True)

    # Agregar piezas de confeti en posiciones aleatorias
    import random
    confetti_html = ""
    for i in range(20):
        left_pos = random.randint(10, 90)
        delay = random.uniform(0, 0.5)
        duration = random.uniform(2, 3)
        color = random.choice(['#a78bfa', '#8b5cf6', '#7c3aed', '#c4b5fd'])
        confetti_html += f"""
        <div class="confetti-piece" style="
            left: {left_pos}%;
            animation-delay: {delay}s;
            animation-duration: {duration}s;
            background: {color};
            border-radius: {'50%' if i % 2 == 0 else '0'};
        "></div>
        """

    st.markdown(confetti_html, unsafe_allow_html=True)


def add_to_favorites(product: dict):
    """
    Agrega el producto a favoritos.

    Args:
        product: Diccionario del producto
    """
    # Inicializar favoritos si no existe
    if 'favorites' not in st.session_state:
        st.session_state['favorites'] = []

    # Verificar si ya está en favoritos
    product_id = product.get('id')
    if product_id in st.session_state['favorites']:
        show_info_toast("ℹ️ Este producto ya está en tus favoritos")
    else:
        st.session_state['favorites'].append(product_id)
        show_success_toast("❤️ Producto agregado a favoritos")
