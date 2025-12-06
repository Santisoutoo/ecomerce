"""
Componente de item del carrito.
Muestra cada producto en el carrito con opciones de editar/eliminar.
"""

import streamlit as st
from services.cart_service import CartService


def render_cart_item(item: dict, index: int):
    """
    Renderiza un item del carrito con controles de cantidad y eliminar.

    Args:
        item: Diccionario con información del item
        index: Índice del item en el carrito
    """
    # Contenedor del item con borde
    with st.container():
        st.markdown("""
        <style>
            .cart-item-container {
                background: #181633;
                border: 1px solid #2d2d3a;
                border-radius: 12px;
                padding: 1.5rem;
                margin-bottom: 1rem;
                transition: all 0.3s;
            }
            .cart-item-container:hover {
                border-color: #a78bfa;
                box-shadow: 0 4px 12px rgba(167, 139, 250, 0.2);
            }
        </style>
        """, unsafe_allow_html=True)

        # Layout principal: Imagen | Info | Cantidad (botones) | Precio
        col1, col2, col3, col4, col5, col6 = st.columns([1.5, 4, 1, 1.5, 1, 2.5])

        with col1:
            # Imagen del producto
            st.markdown(f"""
            <div style="
                background: #1e1b4b;
                border-radius: 8px;
                padding: 0.5rem;
                text-align: center;
            ">
                <img src="{item.get('product_image', 'https://via.placeholder.com/150')}"
                     style="width: 100%; border-radius: 4px;"
                     alt="{item.get('product_name', 'Producto')}">
            </div>
            """, unsafe_allow_html=True)

        with col2:
            # Información del producto
            st.markdown(f"""
            <div style="padding: 0.5rem 0;">
                <p style="color: #a78bfa; font-size: 0.875rem; margin: 0 0 0.25rem 0;">
                    {item.get('team', 'Equipo')}
                </p>
                <h4 style="color: #ffffff; margin: 0 0 0.5rem 0; font-size: 1rem;">
                    {item.get('product_name', 'Producto')}
                </h4>
                <p style="color: #9ca3af; font-size: 0.875rem; margin: 0;">
                    Talla: <strong>{item.get('size', '-')}</strong>
                </p>
            </div>
            """, unsafe_allow_html=True)

            # Personalización (si aplica)
            personalizacion = item.get('personalization')
            if personalizacion:
                nombre = personalizacion.get('nombre', '')
                numero = personalizacion.get('numero', '')
                st.markdown(f"""
                <div style="
                    background: #1e1b4b;
                    border-left: 3px solid #a78bfa;
                    padding: 0.5rem;
                    margin-top: 0.5rem;
                    border-radius: 4px;
                ">
                    <p style="color: #a78bfa; font-size: 0.75rem; margin: 0; font-weight: 600;">
                        ✨ Personalizado
                    </p>
                    <p style="color: #d1d5db; font-size: 0.875rem; margin: 0.25rem 0 0 0;">
                        {nombre} #{numero}
                    </p>
                </div>
                """, unsafe_allow_html=True)

        # Botón Menos
        with col3:
            st.markdown("<p style='color: #9ca3af; font-size: 0.875rem; margin: 0 0 0.5rem 0;'>Cantidad</p>", unsafe_allow_html=True)
            if st.button("➖", key=f"minus_{index}", use_container_width=True):
                update_quantity(index, item.get('quantity', 1) - 1)

        # Cantidad actual
        with col4:
            st.markdown("<p style='color: transparent; font-size: 0.875rem; margin: 0 0 0.5rem 0;'>.</p>", unsafe_allow_html=True)
            st.markdown(f"""
            <div style="
                background: #1e1b4b;
                border: 1px solid #2d2d3a;
                border-radius: 8px;
                padding: 0.5rem;
                text-align: center;
                color: #ffffff;
                font-weight: 600;
                font-size: 1.1rem;
            ">
                {item.get('quantity', 1)}
            </div>
            """, unsafe_allow_html=True)

        # Botón Más
        with col5:
            st.markdown("<p style='color: transparent; font-size: 0.875rem; margin: 0 0 0.5rem 0;'>.</p>", unsafe_allow_html=True)
            if st.button("➕", key=f"plus_{index}", use_container_width=True):
                update_quantity(index, item.get('quantity', 1) + 1)

        with col6:
            # Precios
            precio_unitario = item.get('unit_price', 0)
            precio_personalizacion = item.get('personalization_price', 0)
            cantidad = item.get('quantity', 1)
            subtotal = (precio_unitario + precio_personalizacion) * cantidad

            st.markdown("<p style='color: #9ca3af; font-size: 0.875rem; margin: 0 0 0.5rem 0;'>Precio</p>", unsafe_allow_html=True)

            # Precio unitario
            st.markdown(f"""
            <div style="margin-bottom: 0.5rem;">
                <p style="color: #d1d5db; font-size: 0.875rem; margin: 0;">
                    Base: <strong>{precio_unitario:.2f}€</strong>
                </p>
            </div>
            """, unsafe_allow_html=True)

            # Personalización (si aplica)
            if precio_personalizacion > 0:
                st.markdown(f"""
                <div style="margin-bottom: 0.5rem;">
                    <p style="color: #a78bfa; font-size: 0.875rem; margin: 0;">
                        + Extra: <strong>{precio_personalizacion:.2f}€</strong>
                    </p>
                </div>
                """, unsafe_allow_html=True)

            # Subtotal
            st.markdown(f"""
            <div style="
                background: linear-gradient(135deg, #1e1b4b 0%, #2d2d3a 100%);
                border: 1px solid #a78bfa;
                border-radius: 8px;
                padding: 0.75rem;
                text-align: center;
            ">
                <p style="color: #9ca3af; font-size: 0.75rem; margin: 0 0 0.25rem 0;">Subtotal</p>
                <p style="color: #a78bfa; font-size: 1.25rem; font-weight: 700; margin: 0;">
                    {subtotal:.2f}€
                </p>
            </div>
            """, unsafe_allow_html=True)

        # Botón eliminar (fuera de las columnas)
        st.markdown("<br>", unsafe_allow_html=True)
        col_empty, col_btn = st.columns([8, 2])
        with col_btn:
            if st.button("🗑️ Eliminar", key=f"remove_{index}", use_container_width=True, type="secondary"):
                remove_item(index)

        # Separador
        st.markdown("<hr style='margin: 1rem 0; border-color: #2d2d3a;'>", unsafe_allow_html=True)


def update_quantity(index: int, new_quantity: int):
    """
    Actualiza la cantidad de un item del carrito.

    Args:
        index: Índice del item en el carrito
        new_quantity: Nueva cantidad
    """
    # Validar cantidad mínima y máxima
    if new_quantity < 1:
        # Si es 0, eliminar el item
        remove_item(index)
        return

    if new_quantity > 10:
        st.warning("⚠️ Cantidad máxima: 10 unidades por producto")
        new_quantity = 10

    # Actualizar usando CartService
    try:
        CartService.update_item(index, quantity=new_quantity)
        st.rerun()
    except Exception as e:
        st.error(f"Error al actualizar cantidad: {str(e)}")


def remove_item(index: int):
    """
    Elimina un item del carrito.

    Args:
        index: Índice del item a eliminar
    """
    # Obtener nombre del producto antes de eliminar
    cart = CartService.get_cart()
    if index >= len(cart):
        return

    item_name = cart[index].get('product_name', 'Producto')

    # Eliminar usando CartService
    try:
        CartService.remove_item(index)
        st.success(f"✅ {item_name} eliminado del carrito")
        st.rerun()
    except Exception as e:
        st.error(f"Error al eliminar producto: {str(e)}")
