"""
Componente de tarjeta de producto.
Muestra información del producto con imagen, precio y acciones.
"""

import streamlit as st
from components.navbar import show_welcome_toast, show_error_toast, show_info_toast, show_success_toast
from services.cart_service import CartService


def add_quick_to_cart(product: dict):
    """
    Agrega rápidamente un producto al carrito con valores por defecto.

    Args:
        product: Diccionario del producto
    """
    # Obtener primera talla disponible o 'M' por defecto
    tallas = product.get('tallas', ['M'])
    talla = tallas[0] if tallas else 'M'

    # Agregar al carrito usando el servicio
    try:
        CartService.add_to_cart(
            product_id=product.get('id'),
            quantity=1,
            size=talla,
            personalization=None
        )
    except Exception as e:
        show_error_toast(f"Error al agregar al carrito: {str(e)}")


def render_product_card(product: dict, key_prefix: str = ""):
    """
    Renderiza una tarjeta de producto con diseño atractivo.

    Args:
        product: Diccionario con información del producto
        key_prefix: Prefijo para keys únicos de Streamlit
    """
    # Determinar si hay stock
    has_stock = product.get("stock", 0) > 0
    stock_class = "in-stock" if has_stock else "out-of-stock"

    # Construir HTML usando lista para evitar f-strings anidados y strings vacíos
    html_parts = []

    # Abrir div principal y div de imagen
    imagen_url = product.get('imagen_url', 'https://via.placeholder.com/400')
    product_name = product.get('name', 'Producto')
    html_parts.append(f'''
    <div class="product-card {stock_class}" style="
        background: #181633;
        border: 1px solid #2d2d3a;
        border-radius: 12px;
        padding: 1rem;
        transition: all 0.3s;
        cursor: pointer;
        height: 100%;
    ">
        <div style="
            position: relative;
            width: 100%;
            padding-bottom: 100%;
            border-radius: 8px;
            overflow: hidden;
            background: #1e1b4b;
            margin-bottom: 1rem;
        ">
            <img src="{imagen_url}"
                 style="
                    position: absolute;
                    top: 0;
                    left: 0;
                    width: 100%;
                    height: 100%;
                    object-fit: cover;
                 "
                 alt="{product_name}">
    ''')

    # Badge de agotado (solo si no hay stock)
    if not has_stock:
        html_parts.append('<div style="position: absolute; top: 10px; right: 10px; background: #ef4444; color: white; padding: 0.25rem 0.5rem; border-radius: 4px; font-size: 0.75rem; font-weight: 600;">AGOTADO</div>')

    # Badge de personalizable (solo si permite personalización)
    if product.get('permite_personalizacion'):
        precio_pers = product.get("precio_personalizacion", 0)
        html_parts.append(f'<div style="position: absolute; top: 10px; left: 10px; background: #a78bfa; color: white; padding: 0.25rem 0.5rem; border-radius: 4px; font-size: 0.75rem; font-weight: 600;">✨ Personalizable +{precio_pers:.2f}€</div>')

    # Cerrar div de imagen y abrir div de información
    html_parts.append('</div><div style="padding: 0 0.5rem;">')

    # Equipo
    equipo = product.get('equipo', 'Equipo')
    html_parts.append(f'<p style="color: #9ca3af; font-size: 0.875rem; margin: 0 0 0.5rem 0;">{equipo}</p>')

    # Nombre del producto
    nombre = product.get('name', 'Producto sin nombre')
    html_parts.append(f'''<h3 style="
                color: #ffffff;
                font-size: 1rem;
                margin: 0 0 1rem 0;
                font-weight: 600;
                min-height: 2.5rem;
                display: -webkit-box;
                -webkit-line-clamp: 2;
                -webkit-box-orient: vertical;
                overflow: hidden;
            ">{nombre}</h3>''')

    # Precio y stock
    precio = product.get('precio', 0)
    stock = product.get('stock', 0)
    html_parts.append(f'''<div style="
                display: flex;
                justify-content: space-between;
                align-items: center;
                margin-bottom: 1rem;
            ">
                <div>
                    <span style="
                        color: #a78bfa;
                        font-size: 1.5rem;
                        font-weight: 700;
                    ">{precio:.2f}€</span>
                </div>
                <div style="color: #9ca3af; font-size: 0.875rem;">
                    Stock: {stock}
                </div>
            </div>''')

    # Tallas
    tallas_html = "".join([f'<span style="background: #1e1b4b; color: #d1d5db; padding: 0.25rem 0.5rem; border-radius: 4px; font-size: 0.75rem;">{talla}</span>' for talla in product.get('tallas', [])])
    html_parts.append(f'''<div style="margin-bottom: 1rem;">
                <p style="color: #9ca3af; font-size: 0.75rem; margin: 0 0 0.25rem 0;">Tallas:</p>
                <div style="display: flex; gap: 0.25rem; flex-wrap: wrap;">
                    {tallas_html}
                </div>
            </div>''')

    # Cerrar divs
    html_parts.append('</div></div>')

    # Unir todas las partes
    card_html = ''.join(html_parts)

    # CSS adicional para hover
    st.markdown("""
    <style>
        .product-card:hover {
            transform: translateY(-4px);
            box-shadow: 0 8px 24px rgba(167, 139, 250, 0.3);
            border-color: #a78bfa;
        }
        .product-card.out-of-stock {
            opacity: 0.6;
        }
    </style>
    """, unsafe_allow_html=True)

    # Renderizar la tarjeta
    st.markdown(card_html, unsafe_allow_html=True)

    # Botón para ver detalles del producto
    if st.button(
        "👁️ VER DETALLES",
        key=f"{key_prefix}_view_{product.get('id')}",
        use_container_width=True,
        type="secondary"
    ):
        st.session_state["selected_product"] = product.get("id")
        st.session_state["current_page"] = "product_detail"
        st.rerun()

    # Botón de agregar al carrito
    if has_stock:
        if st.button("🛒 Agregar al Carrito", key=f"{key_prefix}_add_{product.get('id')}", use_container_width=True, type="primary"):
            # Agregar al carrito con valores por defecto
            add_quick_to_cart(product)
            show_success_toast(f"✅ {product.get('name')} agregado al carrito")


def render_product_grid(products: list, key_prefix: str = "grid"):
    """
    Renderiza una cuadrícula de productos.

    Args:
        products: Lista de productos a mostrar
        key_prefix: Prefijo para keys únicos
    """
    if not products:
        st.info("🔍 No se encontraron productos con los filtros seleccionados")
        return

    # Mostrar en grid de 4 columnas
    cols_per_row = 4
    num_products = len(products)

    for i in range(0, num_products, cols_per_row):
        cols = st.columns(cols_per_row)

        for j, col in enumerate(cols):
            product_index = i + j
            if product_index < num_products:
                with col:
                    render_product_card(
                        products[product_index],
                        key_prefix=f"{key_prefix}_{product_index}"
                    )
            else:
                with col:
                    st.empty()  # Espacio vacío para mantener la cuadrícula
