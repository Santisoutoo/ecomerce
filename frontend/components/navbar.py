"""
Barra de navegación principal de la aplicación.
Muestra el menú, usuario actual y opciones de navegación.
"""

import streamlit as st
from frontend.services.auth_service import AuthService
from frontend.config import SESSION_KEYS


def render_navbar():
    """
    Renderiza la barra de navegación superior con información del usuario.
    """
    # CSS personalizado para el navbar
    st.markdown("""
    <style>
        .navbar {
            background: linear-gradient(90deg, #1e1b4b 0%, #181633 100%);
            padding: 1rem 2rem;
            border-bottom: 2px solid #a78bfa;
            margin-bottom: 2rem;
            border-radius: 8px;
        }
        .navbar-title {
            color: #a78bfa;
            font-size: 1.5rem;
            font-weight: 700;
            font-family: 'Exo 2', sans-serif;
        }
        .user-info {
            color: #d1d5db;
            font-size: 0.9rem;
        }
    </style>
    """, unsafe_allow_html=True)

    # Contenedor del navbar
    col1, col2, col3 = st.columns([2, 3, 2])

    with col1:
        st.markdown("""
        <div class='navbar-title'>
            🏪 SportStyle Store
        </div>
        """, unsafe_allow_html=True)

    with col2:
        # Obtener cantidad de items en el carrito
        cart = st.session_state.get('cart', [])
        cart_count = len(cart)

        # Menú de navegación con contador de carrito
        cart_label = f"🛒 Carrito ({cart_count})" if cart_count > 0 else "🛒 Carrito"

        selected = st.segmented_control(
            "Navegación",
            options=["🏠 Home", "🛍️ Catálogo", cart_label, "👤 Mi Cuenta"],
            default="🏠 Home",
            label_visibility="collapsed"
        )

        # Guardar la página seleccionada
        if selected:
            page_map = {
                "🏠 Home": "home",
                "🛍️ Catálogo": "catalog",
                cart_label: "cart",
                "👤 Mi Cuenta": "account"
            }
            st.session_state[SESSION_KEYS["current_page"]] = page_map[selected]

    with col3:
        # Información del usuario y logout
        user_email = st.session_state.get(SESSION_KEYS["user_email"], "Usuario")

        # Mostrar email del usuario
        st.markdown(f"""
        <div class='user-info' style='text-align: right; padding-top: 0.5rem;'>
            📧 {user_email}
        </div>
        """, unsafe_allow_html=True)

        # Botón de admin (solo para administradores)
        if is_admin_user(user_email):
            if st.button("📊 Panel Admin", use_container_width=True, type="primary"):
                st.session_state[SESSION_KEYS["current_page"]] = "admin"
                st.rerun()

        # Botón de cerrar sesión
        if st.button("🚪 Cerrar Sesión", use_container_width=True, type="secondary"):
            logout_user()

    st.markdown("<hr style='margin: 1rem 0; border-color: #2d2d3a;'>", unsafe_allow_html=True)


def is_admin_user(user_email: str) -> bool:
    """
    Verifica si el usuario es administrador.

    Args:
        user_email: Email del usuario

    Returns:
        bool: True si es admin, False en caso contrario
    """
    # Mock: Por ahora, cualquier email que contenga "admin" es admin
    # En producción, esto vendría de la base de datos
    return "admin" in user_email.lower()


def logout_user():
    """
    Cierra la sesión del usuario y limpia el session_state.
    """
    # Obtener token antes de limpiar
    access_token = st.session_state.get(SESSION_KEYS["access_token"])

    if access_token:
        # Llamar al backend para cerrar sesión
        AuthService.logout(access_token)

    # Limpiar todas las variables de sesión
    for key in list(st.session_state.keys()):
        del st.session_state[key]

    st.success("✅ Sesión cerrada correctamente")
    st.rerun()


def show_welcome_toast():
    """
    Muestra un mensaje de bienvenida al usuario la primera vez que inicia sesión.
    """
    if st.session_state.get(SESSION_KEYS["show_welcome"], False):
        user_email = st.session_state.get(SESSION_KEYS["user_email"], "Usuario")

        st.toast(f"¡Bienvenido, {user_email}!", icon="👋")

        # Marcar como mostrado
        st.session_state[SESSION_KEYS["show_welcome"]] = False
