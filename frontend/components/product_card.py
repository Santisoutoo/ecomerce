"""
Componente de tarjeta de producto.
Muestra información del producto con imagen, precio y acciones.
"""

import streamlit as st


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

    # HTML de la tarjeta
    card_html = f"""
    <div class="product-card {stock_class}" style="
        background: #181633;
        border: 1px solid #2d2d3a;
        border-radius: 12px;
        padding: 1rem;
        transition: all 0.3s;
        cursor: pointer;
        height: 100%;
    ">
        <!-- Imagen del producto -->
        <div style="
            position: relative;
            width: 100%;
            padding-bottom: 100%;
            border-radius: 8px;
            overflow: hidden;
            background: #1e1b4b;
            margin-bottom: 1rem;
        ">
            <img src="{product.get('imagen_url', 'https://via.placeholder.com/400')}"
                 style="
                    position: absolute;
                    top: 0;
                    left: 0;
                    width: 100%;
                    height: 100%;
                    object-fit: cover;
                 "
                 alt="{product.get('name', 'Producto')}">

            <!-- Badge de stock -->
            {'<div style="position: absolute; top: 10px; right: 10px; background: #ef4444; color: white; padding: 0.25rem 0.5rem; border-radius: 4px; font-size: 0.75rem; font-weight: 600;">AGOTADO</div>' if not has_stock else ''}

            <!-- Badge de personalización -->
            {f'<div style="position: absolute; top: 10px; left: 10px; background: #a78bfa; color: white; padding: 0.25rem 0.5rem; border-radius: 4px; font-size: 0.75rem; font-weight: 600;">✨ Personalizable +{product.get("precio_personalizacion", 0):.2f}€</div>' if product.get('permite_personalizacion') else ''}
        </div>

        <!-- Información del producto -->
        <div style="padding: 0 0.5rem;">
            <!-- Equipo -->
            <p style="color: #9ca3af; font-size: 0.875rem; margin: 0 0 0.5rem 0;">
                {product.get('equipo', 'Equipo')}
            </p>

            <!-- Nombre del producto -->
            <h3 style="
                color: #ffffff;
                font-size: 1rem;
                margin: 0 0 1rem 0;
                font-weight: 600;
                min-height: 2.5rem;
                display: -webkit-box;
                -webkit-line-clamp: 2;
                -webkit-box-orient: vertical;
                overflow: hidden;
            ">
                {product.get('name', 'Producto sin nombre')}
            </h3>

            <!-- Precio -->
            <div style="
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
                    ">{product.get('precio', 0):.2f}€</span>
                </div>
                <div style="color: #9ca3af; font-size: 0.875rem;">
                    Stock: {product.get('stock', 0)}
                </div>
            </div>

            <!-- Tallas disponibles -->
            <div style="margin-bottom: 1rem;">
                <p style="color: #9ca3af; font-size: 0.75rem; margin: 0 0 0.25rem 0;">Tallas:</p>
                <div style="display: flex; gap: 0.25rem; flex-wrap: wrap;">
                    {"".join([f'<span style="background: #1e1b4b; color: #d1d5db; padding: 0.25rem 0.5rem; border-radius: 4px; font-size: 0.75rem;">{talla}</span>' for talla in product.get('tallas', [])])}
                </div>
            </div>
        </div>
    </div>
    """

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

    # Botones de acción
    col1, col2 = st.columns(2)

    with col1:
        if has_stock:
            if st.button("🛒 Agregar", key=f"{key_prefix}_add_{product.get('id')}", use_container_width=True):
                st.session_state[f"add_to_cart_{product.get('id')}"] = True
                st.toast(f"✅ {product.get('name')} agregado al carrito", icon="🛒")
        else:
            st.button("❌ Agotado", key=f"{key_prefix}_sold_out_{product.get('id')}", use_container_width=True, disabled=True)

    with col2:
        if st.button("👁️ Ver", key=f"{key_prefix}_view_{product.get('id')}", use_container_width=True, type="secondary"):
            st.session_state["selected_product"] = product.get("id")
            st.session_state["current_page"] = "product_detail"
            st.rerun()


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
