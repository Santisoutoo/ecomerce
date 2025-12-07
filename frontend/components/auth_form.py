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


def render_profile_picture_upload():
    """
    Renderiza el componente de upload de foto de perfil con preview.
    Muestra un círculo con imagen default y un lápiz para cambiarla.
    """
    # Inicializar estado de la imagen
    if "profile_picture_file" not in st.session_state:
        st.session_state.profile_picture_file = None

    # URL de imagen default (icono de usuario)
    default_image = "https://cdn-icons-png.flaticon.com/512/149/149071.png"

    # Obtener URL de preview
    if st.session_state.profile_picture_file:
        # Si hay una imagen seleccionada, usarla como preview
        image_to_show = st.session_state.profile_picture_file
    else:
        image_to_show = default_image

    # CSS personalizado para el círculo y el lápiz
    st.markdown(f"""
    <style>
    .profile-picture-container {{
        display: flex;
        justify-content: center;
        align-items: center;
        margin: 1rem 0 2rem 0;
    }}

    .profile-picture-wrapper {{
        position: relative;
        width: 150px;
        height: 150px;
    }}

    .profile-picture-circle {{
        width: 150px;
        height: 150px;
        border-radius: 50%;
        border: 3px solid #a78bfa;
        overflow: hidden;
        display: flex;
        justify-content: center;
        align-items: center;
        background: #1e1b4b;
        box-shadow: 0 4px 20px rgba(167, 139, 250, 0.3);
    }}

    .profile-picture-circle img {{
        width: 100%;
        height: 100%;
        object-fit: cover;
    }}

    .edit-icon {{
        position: absolute;
        bottom: 5px;
        right: 5px;
        width: 40px;
        height: 40px;
        background: linear-gradient(135deg, #a78bfa 0%, #8b5cf6 100%);
        border-radius: 50%;
        display: flex;
        justify-content: center;
        align-items: center;
        cursor: pointer;
        border: 3px solid #0f0f1e;
        box-shadow: 0 2px 10px rgba(167, 139, 250, 0.5);
        transition: transform 0.2s;
    }}

    .edit-icon:hover {{
        transform: scale(1.1);
    }}

    .edit-icon::after {{
        content: "✏️";
        font-size: 1.2rem;
    }}
    </style>

    <div class="profile-picture-container">
        <div class="profile-picture-wrapper">
            <div class="profile-picture-circle">
                <img src="{image_to_show if isinstance(image_to_show, str) else default_image}" alt="Profile Picture">
            </div>
            <div class="edit-icon"></div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # File uploader
    st.markdown("<p style='text-align: center; color: #9ca3af; font-size: 0.9rem; margin-bottom: 1rem;'>Click en el lápiz para subir tu foto de perfil</p>", unsafe_allow_html=True)

    uploaded_file = st.file_uploader(
        "Selecciona una imagen",
        type=["jpg", "jpeg", "png", "webp"],
        key="profile_picture_uploader",
        help="Formatos: JPG, PNG, WEBP. Máximo 5MB",
        label_visibility="collapsed"
    )

    if uploaded_file:
        # Validar tamaño
        file_size_mb = len(uploaded_file.getvalue()) / (1024 * 1024)
        if file_size_mb > 5:
            st.error("⚠️ La imagen no puede superar los 5MB")
            st.session_state.profile_picture_file = None
        else:
            st.session_state.profile_picture_file = uploaded_file
            st.success(f"✅ Foto seleccionada: {uploaded_file.name} ({file_size_mb:.2f} MB)")


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
                # Obtener datos completos del usuario incluyendo es_admin
                user_success, user_data, user_error = AuthService.get_current_user(data["access_token"])

                # Guardar datos en session_state
                st.session_state[SESSION_KEYS["authenticated"]] = True
                st.session_state[SESSION_KEYS["access_token"]] = data["access_token"]
                st.session_state[SESSION_KEYS["user_id"]] = data["user_id"]
                st.session_state[SESSION_KEYS["user_email"]] = data["email"]
                st.session_state[SESSION_KEYS["es_admin"]] = user_data.get("es_admin", False) if user_success else False
                st.session_state['user_foto_perfil'] = user_data.get("foto_perfil", "") if user_success else ""
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

    # Componente de foto de perfil
    render_profile_picture_upload()

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
                # Si hay una foto de perfil seleccionada, subirla
                foto_perfil_url = None
                if st.session_state.get("profile_picture_file"):
                    with st.spinner("Subiendo foto de perfil..."):
                        upload_success, foto_url, upload_error = AuthService.upload_profile_picture(
                            st.session_state.profile_picture_file,
                            data["access_token"]
                        )
                        if upload_success:
                            foto_perfil_url = foto_url
                            st.success("✅ Foto de perfil subida correctamente")
                        else:
                            st.warning(f"⚠️ No se pudo subir la foto: {upload_error}")

                # Obtener datos completos del usuario incluyendo es_admin
                user_success, user_data, user_error = AuthService.get_current_user(data["access_token"])

                # Guardar datos en session_state
                st.session_state[SESSION_KEYS["authenticated"]] = True
                st.session_state[SESSION_KEYS["access_token"]] = data["access_token"]
                st.session_state[SESSION_KEYS["user_id"]] = data["user_id"]
                st.session_state[SESSION_KEYS["user_email"]] = data["email"]
                st.session_state[SESSION_KEYS["es_admin"]] = user_data.get("es_admin", False) if user_success else False
                st.session_state['user_foto_perfil'] = user_data.get("foto_perfil", "") if user_success else ""
                st.session_state[SESSION_KEYS["show_welcome"]] = True

                # Limpiar el archivo de perfil del session state
                st.session_state.profile_picture_file = None

                st.success("✅ Cuenta creada exitosamente")
                st.balloons()
                st.rerun()
            else:
                st.error(f"❌ {error}")
