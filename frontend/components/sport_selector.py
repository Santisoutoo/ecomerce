"""
Componente selector de deportes.
Permite al usuario elegir entre Fútbol, Baloncesto y Fórmula 1.
"""

import streamlit as st
from services.product_service import ProductService


def render_sport_selector():
    """
    Renderiza un selector de deportes con diseño atractivo.
    Guarda la selección en session_state.
    """
    st.markdown("### 🏆 Selecciona tu Deporte")

    sports = ProductService.get_sports()

    # CSS personalizado para las tarjetas de deporte
    st.markdown("""
    <style>
        .sport-card {
            background: linear-gradient(135deg, #1e1b4b 0%, #181633 100%);
            border: 2px solid #2d2d3a;
            border-radius: 16px;
            padding: 2rem 1rem;
            text-align: center;
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
            cursor: pointer;
            height: 100%;
        }
        .sport-card:hover {
            transform: translateY(-8px);
            border-color: #a78bfa;
            box-shadow: 0 12px 32px rgba(167, 139, 250, 0.3);
        }
        .sport-card.selected {
            border-color: #a78bfa;
            background: linear-gradient(135deg, #2d2d3a 0%, #1e1b4b 100%);
            box-shadow: 0 8px 24px rgba(167, 139, 250, 0.4);
        }
        .sport-icon {
            font-size: 4rem;
            margin-bottom: 1rem;
            display: block;
        }
        .sport-name {
            color: #ffffff;
            font-size: 1.25rem;
            font-weight: 700;
            margin: 0;
        }
    </style>
    """, unsafe_allow_html=True)

    # Obtener deporte seleccionado actual
    selected_sport = st.session_state.get("selected_sport", None)

    # Crear columnas para los deportes
    cols = st.columns(len(sports))

    for i, sport in enumerate(sports):
        with cols[i]:
            # Determinar si está seleccionado
            is_selected = selected_sport == sport["id"]
            selected_class = "selected" if is_selected else ""

            # Renderizar tarjeta del deporte
            st.markdown(f"""
            <div class="sport-card {selected_class}">
                <span class="sport-icon">{sport["icon"]}</span>
                <h3 class="sport-name">{sport["name"]}</h3>
            </div>
            """, unsafe_allow_html=True)

            # Botón para seleccionar el deporte
            if st.button(
                "SELECCIONAR",
                key=f"sport_btn_{sport['id']}",
                use_container_width=True,
                type="secondary"
            ):
                st.session_state["selected_sport"] = sport["id"]
                st.session_state["selected_team"] = None  # Reset team selection
                st.rerun()


def render_team_selector(sport_id: str):
    """
    Renderiza un selector de equipos basado en el deporte seleccionado.

    Args:
        sport_id: ID del deporte seleccionado
    """
    teams = ProductService.get_teams_by_sport(sport_id)

    if not teams:
        return

    st.markdown("### ⭐ Selecciona tu Equipo Favorito")

    # Obtener equipo seleccionado actual
    selected_team = st.session_state.get("selected_team", None)

    # Selector de equipo
    team_options = ["Todos los equipos"] + teams

    current_index = 0
    if selected_team and selected_team in teams:
        current_index = teams.index(selected_team) + 1

    selected = st.selectbox(
        "Equipo",
        options=team_options,
        index=current_index,
        label_visibility="collapsed",
        key="team_selector"
    )

    # Guardar selección
    if selected != "Todos los equipos":
        st.session_state["selected_team"] = selected
    else:
        st.session_state["selected_team"] = None


def render_category_filter():
    """
    Renderiza un filtro de categorías de productos.
    """
    categories = ProductService.get_categories()

    st.markdown("### 🏷️ Categoría")

    # Obtener categoría seleccionada
    selected_category = st.session_state.get("selected_category", None)

    # Selector de categoría
    category_options = ["Todas las categorías"] + categories

    current_index = 0
    if selected_category and selected_category in categories:
        current_index = categories.index(selected_category) + 1

    selected = st.selectbox(
        "Categoría",
        options=category_options,
        index=current_index,
        label_visibility="collapsed",
        key="category_selector"
    )

    # Guardar selección
    if selected != "Todas las categorías":
        st.session_state["selected_category"] = selected
    else:
        st.session_state["selected_category"] = None


def render_filters_sidebar():
    """
    Renderiza la barra lateral con todos los filtros.
    """
    with st.sidebar:
        st.markdown("## 🔍 Filtros")

        # Deporte (si ya hay uno seleccionado)
        selected_sport = st.session_state.get("selected_sport")

        if selected_sport:
            st.markdown(f"**Deporte:** {selected_sport.capitalize()}")

            # Botón para cambiar deporte
            if st.button("🔄 Cambiar Deporte", use_container_width=True):
                st.session_state["selected_sport"] = None
                st.session_state["selected_team"] = None
                st.session_state["selected_category"] = None
                st.rerun()

            st.markdown("---")

            # Filtro de equipo
            render_team_selector(selected_sport)

            st.markdown("---")

            # Filtro de categoría
            render_category_filter()

            st.markdown("---")

            # Botón para limpiar filtros
            if st.button("🗑️ Limpiar Filtros", use_container_width=True):
                st.session_state["selected_team"] = None
                st.session_state["selected_category"] = None
                st.rerun()
