"""
Formulario de autenticación (Login y Registro) para Streamlit.
Componente UI completo con validación y estilos.
"""

import streamlit as st
from services.auth_service import AuthService
from config import SESSION_KEYS


def render_auth_form():
    """
    Renderiza el formulario principal de autenticación con pestañas de Login y Registro.
    """
    # Inicializar estado de la pestaña activa
    if "auth_tab" not in st.session_state:
        st.session_state.auth_tab = "login"

    # Título principal
    st.markdown("""
    <div style='text-align: center; padding: 2rem 0;'>
        <h1 style='color: #a78bfa; font-family: "Exo 2", sans-serif;'>
            🏪 SportStyle Store
        </h1>
        <p style='color: #d1d5db; font-size: 1.1rem;'>
            Tu tienda de merchandising deportivo
        </p>
    </div>
    """, unsafe_allow_html=True)

    # Contenedor del formulario
    st.markdown("""
    <div class='auth-container' style='
        max-width: 500px;
        margin: 0 auto;
        padding: 2rem;
        background: #181633;
        border-radius: 12px;
        border: 1px solid #2d2d3a;
    '>
    </div>
    """, unsafe_allow_html=True)

    # Tabs para Login y Registro
    tab1, tab2 = st.tabs(["🔑 Iniciar Sesión", "📝 Registrarse"])

    with tab1:
        render_login_tab()

    with tab2:
        render_register_tab()


def render_login_tab():
    """
    Renderiza el formulario de inicio de sesión.
    """
    st.markdown("<br>", unsafe_allow_html=True)

    with st.form("login_form", clear_on_submit=False):
        # Campos del formulario
        email = st.text_input(
            "📧 Email",
            placeholder="tu@email.com",
            key="login_email"
        )

        password = st.text_input(
            "🔒 Contraseña",
            type="password",
            placeholder="Tu contraseña",
            key="login_password"
        )

        # Botón de submit
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            submit = st.form_submit_button(
                "Iniciar Sesión",
                use_container_width=True,
                type="primary"
            )

        # Procesar el formulario
        if submit:
            if not email or not password:
                st.error("⚠️ Por favor completa todos los campos")
                return

            # Llamar al servicio de autenticación
            with st.spinner("Verificando credenciales..."):
                success, data, error = AuthService.login(email, password)

            if success:
                # Guardar datos en session_state
                st.session_state[SESSION_KEYS["authenticated"]] = True
                st.session_state[SESSION_KEYS["access_token"]] = data["access_token"]
                st.session_state[SESSION_KEYS["user_id"]] = data["user_id"]
                st.session_state[SESSION_KEYS["user_email"]] = data["email"]
                st.session_state[SESSION_KEYS["show_welcome"]] = True

                st.success("✅ Sesión iniciada correctamente")
                st.rerun()
            else:
                st.error(f"❌ {error}")


def render_register_tab():
    """
    Renderiza el formulario de registro de nuevo usuario.
    """
    st.markdown("<br>", unsafe_allow_html=True)

    with st.form("register_form", clear_on_submit=False):
        # Campos del formulario
        col1, col2 = st.columns(2)

        with col1:
            nombre = st.text_input(
                "👤 Nombre",
                placeholder="Juan",
                key="register_nombre"
            )

        with col2:
            apellidos = st.text_input(
                "👥 Apellidos",
                placeholder="Pérez García",
                key="register_apellidos"
            )

        email = st.text_input(
            "📧 Email",
            placeholder="tu@email.com",
            key="register_email"
        )

        telefono = st.text_input(
            "📱 Teléfono (opcional)",
            placeholder="612345678",
            max_chars=9,
            key="register_telefono"
        )

        col1, col2 = st.columns(2)

        with col1:
            password = st.text_input(
                "🔒 Contraseña",
                type="password",
                placeholder="Mínimo 6 caracteres",
                key="register_password"
            )

        with col2:
            password_confirm = st.text_input(
                "🔒 Confirmar Contraseña",
                type="password",
                placeholder="Repite tu contraseña",
                key="register_password_confirm"
            )

        # Términos y condiciones
        terms = st.checkbox(
            "Acepto los términos y condiciones",
            key="register_terms"
        )

        # Botón de submit
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            submit = st.form_submit_button(
                "Crear Cuenta",
                use_container_width=True,
                type="primary"
            )

        # Procesar el formulario
        if submit:
            # Validaciones
            if not all([nombre, apellidos, email, password, password_confirm]):
                st.error("⚠️ Por favor completa todos los campos obligatorios")
                return

            if password != password_confirm:
                st.error("⚠️ Las contraseñas no coinciden")
                return

            if len(password) < 6:
                st.error("⚠️ La contraseña debe tener al menos 6 caracteres")
                return

            if not terms:
                st.error("⚠️ Debes aceptar los términos y condiciones")
                return

            if telefono and len(telefono) != 9:
                st.error("⚠️ El teléfono debe tener 9 dígitos")
                return

            # Llamar al servicio de autenticación
            with st.spinner("Creando cuenta..."):
                success, data, error = AuthService.register(
                    email=email,
                    password=password,
                    nombre=nombre,
                    apellidos=apellidos,
                    telefono=telefono if telefono else None
                )

            if success:
                # Guardar datos en session_state
                st.session_state[SESSION_KEYS["authenticated"]] = True
                st.session_state[SESSION_KEYS["access_token"]] = data["access_token"]
                st.session_state[SESSION_KEYS["user_id"]] = data["user_id"]
                st.session_state[SESSION_KEYS["user_email"]] = data["email"]
                st.session_state[SESSION_KEYS["show_welcome"]] = True

                st.success("✅ Cuenta creada exitosamente")
                st.balloons()
                st.rerun()
            else:
                st.error(f"❌ {error}")
