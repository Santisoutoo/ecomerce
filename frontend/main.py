"""
Aplicación principal de Streamlit para SportStyle Store.
Punto de entrada del frontend con gestión de autenticación y navegación.
"""

import streamlit as st
from frontend.config import APP_NAME, APP_ICON, SESSION_KEYS
from frontend.components.auth_form import render_auth_form
from frontend.components.navbar import render_navbar, show_welcome_toast


# Configuración de la página
st.set_page_config(
    page_title=APP_NAME,
    page_icon=APP_ICON,
    layout="wide",
    initial_sidebar_state="collapsed"
)


def initialize_session_state():
    """
    Inicializa las variables de sesión necesarias.
    """
    if SESSION_KEYS["authenticated"] not in st.session_state:
        st.session_state[SESSION_KEYS["authenticated"]] = False

    if SESSION_KEYS["current_page"] not in st.session_state:
        st.session_state[SESSION_KEYS["current_page"]] = "home"

    if SESSION_KEYS["show_welcome"] not in st.session_state:
        st.session_state[SESSION_KEYS["show_welcome"]] = False


def load_custom_css():
    """
    Carga los estilos CSS personalizados.
    """
    try:
        from frontend.styles import GLOBAL_CSS
        st.markdown(GLOBAL_CSS, unsafe_allow_html=True)
    except ImportError:
        # Si no existe styles.py, usar estilos básicos
        st.markdown("""
        <style>
            .stApp {
                background: linear-gradient(135deg, #121127 0%, #1e1b4b 100%);
            }
            h1, h2, h3 {
                color: #a78bfa !important;
                font-family: 'Exo 2', sans-serif;
            }
        </style>
        """, unsafe_allow_html=True)


def render_home_page():
    """
    Renderiza la página de inicio (placeholder).
    """
    st.title("🏠 Inicio")
    st.write("Bienvenido a SportStyle Store")
    st.info("🚧 Página en construcción - Próximamente catálogo de productos")


def render_catalog_page():
    """
    Renderiza la página de catálogo (placeholder).
    """
    st.title("🛍️ Catálogo")
    st.write("Explora nuestros productos deportivos")
    st.info("🚧 Página en construcción - Próximamente productos de fútbol, baloncesto y F1")


def render_cart_page():
    """
    Renderiza la página del carrito (placeholder).
    """
    st.title("🛒 Carrito de Compras")
    st.write("Tu carrito de compras")
    st.info("🚧 Página en construcción - Gestión de carrito próximamente")


def render_account_page():
    """
    Renderiza la página de cuenta de usuario (placeholder).
    """
    st.title("👤 Mi Cuenta")

    # Mostrar información básica del usuario
    user_email = st.session_state.get(SESSION_KEYS["user_email"], "No disponible")
    user_id = st.session_state.get(SESSION_KEYS["user_id"], "No disponible")

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Información Personal")
        st.write(f"**Email:** {user_email}")
        st.write(f"**ID:** {user_id}")

    with col2:
        st.subheader("Puntos de Fidelización")
        st.metric("Puntos Disponibles", 0)

    st.info("🚧 Página en construcción - Gestión completa de perfil próximamente")


def main():
    """
    Función principal de la aplicación.
    Gestiona el flujo de autenticación y navegación.
    """
    # Inicializar estado
    initialize_session_state()

    # Cargar estilos
    load_custom_css()

    # Verificar si el usuario está autenticado
    is_authenticated = st.session_state.get(SESSION_KEYS["authenticated"], False)

    if not is_authenticated:
        # Mostrar formulario de autenticación
        render_auth_form()

    else:
        # Usuario autenticado - Mostrar aplicación principal

        # Mostrar mensaje de bienvenida (solo una vez)
        show_welcome_toast()

        # Renderizar navbar
        render_navbar()

        # Obtener página actual
        current_page = st.session_state.get(SESSION_KEYS["current_page"], "home")

        # Renderizar la página correspondiente
        if current_page == "home":
            render_home_page()

        elif current_page == "catalog":
            render_catalog_page()

        elif current_page == "cart":
            render_cart_page()

        elif current_page == "account":
            render_account_page()

        else:
            # Página por defecto
            render_home_page()


if __name__ == "__main__":
    main()
