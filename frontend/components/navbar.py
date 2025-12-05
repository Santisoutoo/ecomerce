"""
Barra de navegación principal de la aplicación usando hydralit_components.
Muestra el menú con iconos Font Awesome, usuario actual y opciones de navegación.
"""

import streamlit as st
import hydralit_components as hc
from services.auth_service import AuthService
from config import SESSION_KEYS


def render_navbar():
    """
    Renderiza la barra de navegación superior fija usando hydralit_components.
    Incluye navegación con iconos Font Awesome y logout button.
    """
    # Obtener información del usuario y carrito
    user_email = st.session_state.get(SESSION_KEYS["user_email"], "")
    cart = st.session_state.get('cart', [])
    cart_count = len(cart)

    # Theme personalizado para SportStyle Store
    override_theme = {
        'txc_inactive': '#d1d5db',       # TextColor.SECONDARY (Light gray para inactivo)
        'menu_background': '#121127',     # Color.PRIMARY_BG (Dark blue-black)
        'txc_active': '#ffffff',          # TextColor.PRIMARY (White para activo)
        'option_active': '#1e1b4b',       # Color.SECONDARY_BG (Dark indigo para hover)
        'txc_hover': '#a78bfa'            # Color.ACCENT (Purple para hover text)
    }

    # CSS adicional para navbar fijo y ajustes de estilo
    st.markdown("""
        <style>
        /* Forzar navbar fijo en la parte superior */
        iframe[title="hydralit_components.NAV_BAR.nav_bar"] {
            position: fixed !important;
            top: 0 !important;
            left: 0 !important;
            right: 0 !important;
            z-index: 999999 !important;
            width: 100% !important;
        }

        /* Padding al contenido principal para evitar solapamiento con navbar */
        .main .block-container {
            padding-top: 80px !important;
        }

        /* Asegurar que el contenedor del navbar iframe tenga altura y posición correcta */
        div[data-testid="stVerticalBlock"] > div:has(iframe[title="hydralit_components.NAV_BAR.nav_bar"]) {
            position: fixed !important;
            top: 0 !important;
            left: 0 !important;
            right: 0 !important;
            z-index: 999999 !important;
            width: 100% !important;
        }

        /* Estilo para mostrar info del usuario debajo del navbar */
        .user-info-banner {
            position: fixed;
            top: 60px;
            right: 20px;
            background: rgba(30, 27, 75, 0.95);
            color: #d1d5db;
            padding: 0.5rem 1rem;
            border-radius: 8px;
            font-size: 0.85rem;
            z-index: 999998;
            border: 1px solid #a78bfa;
            box-shadow: 0 2px 8px rgba(0, 0, 0, 0.3);
        }
        </style>
    """, unsafe_allow_html=True)

    # Construir menú dinámicamente según permisos
    menu_items = [
        {'id': 'Catalog', 'icon': "fa fa-shopping-bag", 'label': "Catálogo"},
    ]

    # Agregar item de carrito con badge de cantidad si hay items
    if cart_count > 0:
        menu_items.append({
            'id': 'Cart',
            'icon': "fa fa-shopping-cart",
            'label': f"Carrito ({cart_count})"
        })
    else:
        menu_items.append({
            'id': 'Cart',
            'icon': "fa fa-shopping-cart",
            'label': "Carrito"
        })

    menu_items.append({'id': 'Account', 'icon': "fa fa-user", 'label': "Mi Cuenta"})

    # Agregar opción de admin si el usuario es administrador
    if is_admin_user(user_email):
        menu_items.append({'id': 'Admin', 'icon': "fa fa-cog", 'label': "Admin"})

    # Renderizar navbar con hydralit_components
    menu_id = hc.nav_bar(
        menu_definition=menu_items,
        override_theme=override_theme,
        home_name='Home',          # Botón Home a la izquierda
        login_name='Logout',       # Botón Logout a la derecha
        sticky_nav=True,           # Navbar sticky
        sticky_mode='pinned',      # Modo pinned (sin saltos)
        hide_streamlit_markers=False
    )

    # Mostrar información del usuario en esquina superior derecha
    st.markdown(f"""
        <div class='user-info-banner'>
            <i class='fa fa-user'></i> {user_email}
        </div>
    """, unsafe_allow_html=True)

    # Obtener última selección del navbar para evitar re-navegación en re-renders
    last_menu_id = st.session_state.get('last_navbar_menu_id', None)

    # Solo navegar si el menu_id cambió (nuevo click)
    if menu_id != last_menu_id:
        st.session_state['last_navbar_menu_id'] = menu_id

        # Manejar logout
        if menu_id == 'Logout':
            logout_user()

        # Manejar navegación
        elif menu_id == 'Home':
            navigate_to_page('home')

        elif menu_id == 'Catalog':
            navigate_to_page('catalog')

        elif menu_id == 'Cart':
            navigate_to_page('cart')

        elif menu_id == 'Account':
            navigate_to_page('account')

        elif menu_id == 'Admin':
            if is_admin_user(user_email):
                navigate_to_page('admin')

    return menu_id


def navigate_to_page(page: str):
    """
    Navega a una página específica si no es la actual.

    Args:
        page: Nombre de la página a navegar
    """
    current_page = st.session_state.get(SESSION_KEYS["current_page"])
    if current_page != page:
        st.session_state[SESSION_KEYS["current_page"]] = page
        st.rerun()


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
    Muestra un toast de bienvenida animado al usuario la primera vez que inicia sesión.
    Aparece en la esquina superior derecha y desaparece después de 3 segundos.
    """
    if st.session_state.get(SESSION_KEYS["show_welcome"], False):
        user_email = st.session_state.get(SESSION_KEYS["user_email"], "Usuario")

        # Toast personalizado con animación
        toast_html = f"""
            <style>
            /* Animaciones para el toast */
            @keyframes slideInRight {{
                from {{
                    transform: translateX(100%);
                    opacity: 0;
                }}
                to {{
                    transform: translateX(0);
                    opacity: 1;
                }}
            }}

            @keyframes slideOutRight {{
                from {{
                    transform: translateX(0);
                    opacity: 1;
                }}
                to {{
                    transform: translateX(100%);
                    opacity: 0;
                }}
            }}

            .custom-toast {{
                position: fixed;
                top: 100px;
                right: 20px;
                background: linear-gradient(135deg, #10b981 0%, #059669 100%);
                color: white;
                padding: 1rem 1.5rem;
                border-radius: 12px;
                box-shadow: 0 4px 20px rgba(16, 185, 129, 0.4);
                z-index: 10000;
                font-weight: 600;
                font-size: 1rem;
                animation: slideInRight 0.5s ease-out, slideOutRight 0.5s ease-in 2.5s;
                animation-fill-mode: forwards;
            }}

            .custom-toast-icon {{
                font-size: 1.5rem;
                margin-right: 0.5rem;
            }}
            </style>

            <div class="custom-toast">
                <span class="custom-toast-icon">🏪</span>
                ✅ ¡Bienvenido, {user_email}!
            </div>

            <script>
            setTimeout(function() {{
                const toast = document.querySelector('.custom-toast');
                if (toast) {{
                    toast.style.animation = 'slideOutRight 0.5s ease-in';
                    setTimeout(() => toast.remove(), 500);
                }}
            }}, 3000);
            </script>
        """

        st.markdown(toast_html, unsafe_allow_html=True)

        # Marcar como mostrado
        st.session_state[SESSION_KEYS["show_welcome"]] = False


def show_error_toast(message):
    """
    Muestra un toast de error animado.
    Aparece en la esquina superior derecha y desaparece después de 4 segundos.

    Args:
        message (str): Mensaje de error a mostrar
    """
    toast_html = f"""
        <style>
        /* Animaciones para el toast de error */
        @keyframes slideInRight {{
            from {{
                transform: translateX(100%);
                opacity: 0;
            }}
            to {{
                transform: translateX(0);
                opacity: 1;
            }}
        }}

        @keyframes slideOutRight {{
            from {{
                transform: translateX(0);
                opacity: 1;
            }}
            to {{
                transform: translateX(100%);
                opacity: 0;
            }}
        }}

        .custom-error-toast {{
            position: fixed;
            top: 100px;
            right: 20px;
            background: linear-gradient(135deg, #ef4444 0%, #dc2626 100%);
            color: white;
            padding: 1rem 1.5rem;
            border-radius: 12px;
            box-shadow: 0 4px 20px rgba(239, 68, 68, 0.4);
            z-index: 10000;
            font-weight: 600;
            font-size: 1rem;
            animation: slideInRight 0.5s ease-out, slideOutRight 0.5s ease-in 3.5s;
            animation-fill-mode: forwards;
            max-width: 400px;
        }}

        .custom-error-toast-icon {{
            font-size: 1.5rem;
            margin-right: 0.5rem;
        }}
        </style>

        <div class="custom-error-toast">
            <span class="custom-error-toast-icon">❌</span>
            {message}
        </div>

        <script>
        setTimeout(function() {{
            const toast = document.querySelector('.custom-error-toast');
            if (toast) {{
                toast.style.animation = 'slideOutRight 0.5s ease-in';
                setTimeout(() => toast.remove(), 500);
            }}
        }}, 4000);
        </script>
    """

    st.markdown(toast_html, unsafe_allow_html=True)


def show_info_toast(message="⏳ Cargando..."):
    """
    Muestra un toast informativo animado con el tema purple del proyecto.
    Aparece en la esquina superior derecha y desaparece después de 5 segundos.

    Args:
        message (str): Mensaje informativo a mostrar
    """
    toast_html = f"""
        <style>
        /* Animaciones para el toast informativo */
        @keyframes slideInRight {{
            from {{
                transform: translateX(100%);
                opacity: 0;
            }}
            to {{
                transform: translateX(0);
                opacity: 1;
            }}
        }}

        @keyframes slideOutRight {{
            from {{
                transform: translateX(0);
                opacity: 1;
            }}
            to {{
                transform: translateX(100%);
                opacity: 0;
            }}
        }}

        .custom-info-toast {{
            position: fixed;
            top: 100px;
            right: 20px;
            background: linear-gradient(135deg, #a78bfa 0%, #8b5cf6 100%);
            color: white;
            padding: 1rem 1.5rem;
            border-radius: 12px;
            box-shadow: 0 4px 20px rgba(167, 139, 250, 0.4);
            z-index: 10000;
            font-weight: 600;
            font-size: 1rem;
            animation: slideInRight 0.5s ease-out, slideOutRight 0.5s ease-in 4.5s;
            animation-fill-mode: forwards;
            max-width: 400px;
        }}
        </style>

        <div class="custom-info-toast">
            {message}
        </div>

        <script>
        setTimeout(function() {{
            const toast = document.querySelector('.custom-info-toast');
            if (toast) {{
                toast.style.animation = 'slideOutRight 0.5s ease-in';
                setTimeout(() => toast.remove(), 500);
            }}
        }}, 5000);
        </script>
    """

    st.markdown(toast_html, unsafe_allow_html=True)


def show_success_toast(message):
    """
    Muestra un toast de éxito animado con gradiente verde.
    Aparece en la esquina superior derecha y desaparece después de 3 segundos.

    Args:
        message (str): Mensaje de éxito a mostrar
    """
    toast_html = f"""
        <style>
        /* Animaciones para el toast de éxito */
        @keyframes slideInRight {{
            from {{
                transform: translateX(100%);
                opacity: 0;
            }}
            to {{
                transform: translateX(0);
                opacity: 1;
            }}
        }}

        @keyframes slideOutRight {{
            from {{
                transform: translateX(0);
                opacity: 1;
            }}
            to {{
                transform: translateX(100%);
                opacity: 0;
            }}
        }}

        .custom-success-toast {{
            position: fixed;
            top: 100px;
            right: 20px;
            background: linear-gradient(135deg, #10b981 0%, #059669 100%);
            color: white;
            padding: 1rem 1.5rem;
            border-radius: 12px;
            box-shadow: 0 4px 20px rgba(16, 185, 129, 0.4);
            z-index: 10000;
            font-weight: 600;
            font-size: 1rem;
            animation: slideInRight 0.5s ease-out, slideOutRight 0.5s ease-in 2.5s;
            animation-fill-mode: forwards;
            max-width: 400px;
        }}

        .custom-success-toast-icon {{
            font-size: 1.5rem;
            margin-right: 0.5rem;
        }}
        </style>

        <div class="custom-success-toast">
            {message}
        </div>

        <script>
        setTimeout(function() {{
            const toast = document.querySelector('.custom-success-toast');
            if (toast) {{
                toast.style.animation = 'slideOutRight 0.5s ease-in';
                setTimeout(() => toast.remove(), 500);
            }}
        }}, 3000);
        </script>
    """

    st.markdown(toast_html, unsafe_allow_html=True)
