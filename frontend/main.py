"""
Aplicación principal de Streamlit para SportStyle Store.
Punto de entrada del frontend con gestión de autenticación y navegación.
"""

import streamlit as st
from frontend.config import APP_NAME, APP_ICON, SESSION_KEYS
from frontend.components.auth_form import render_auth_form
from frontend.components.navbar import render_navbar, show_welcome_toast
from frontend.pages.home import render_home_page
from frontend.pages.catalog import render_catalog_page
from frontend.pages.product_detail import render_product_detail_page
from frontend.pages.cart import render_cart_page
from frontend.pages.checkout import render_checkout_page
from frontend.pages.order_confirmation import render_order_confirmation_page
from frontend.pages.account import render_account_page
from frontend.pages.admin import render_admin_page


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


# Todas las páginas ahora se importan desde frontend.pages.*


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

        elif current_page == "product_detail":
            render_product_detail_page()

        elif current_page == "cart":
            render_cart_page()

        elif current_page == "checkout":
            render_checkout_page()

        elif current_page == "order_confirmation":
            render_order_confirmation_page()

        elif current_page == "account":
            render_account_page()

        elif current_page == "admin":
            render_admin_page()

        else:
            # Página por defecto
            render_home_page()


if __name__ == "__main__":
    main()
