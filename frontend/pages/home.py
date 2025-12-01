"""
Página principal (Home) de SportStyle Store.
Muestra selección de deportes, productos destacados y catálogo filtrado.
"""

import streamlit as st
from frontend.components.sport_selector import render_sport_selector, render_filters_sidebar
from frontend.components.product_card import render_product_grid
from frontend.services.product_service import ProductService


def render_home_page():
    """
    Renderiza la página de inicio con selección de deportes y productos.
    """
    # Banner principal
    render_hero_banner()

    # Obtener deporte seleccionado
    selected_sport = st.session_state.get("selected_sport", None)

    if not selected_sport:
        # Mostrar selector de deportes si no hay ninguno seleccionado
        st.markdown("<br>", unsafe_allow_html=True)
        render_sport_selector()

        st.markdown("<br><br>", unsafe_allow_html=True)

        # Mostrar productos destacados
        render_featured_products()

    else:
        # Mostrar filtros en sidebar
        render_filters_sidebar()

        # Mostrar catálogo filtrado
        render_filtered_catalog()


def render_hero_banner():
    """
    Renderiza el banner principal de la página.
    """
    st.markdown("""
    <div style="
        background: linear-gradient(135deg, #1e1b4b 0%, #2d2d3a 100%);
        border: 2px solid #a78bfa;
        border-radius: 16px;
        padding: 3rem 2rem;
        text-align: center;
        margin-bottom: 2rem;
    ">
        <h1 style="
            color: #a78bfa;
            font-size: 2.5rem;
            font-weight: 700;
            margin: 0 0 1rem 0;
            font-family: 'Exo 2', sans-serif;
        ">
            ¡Bienvenido a SportStyle Store! 🏪
        </h1>
        <p style="
            color: #d1d5db;
            font-size: 1.25rem;
            margin: 0;
        ">
            Tu tienda de merchandising oficial de Fútbol ⚽ Baloncesto 🏀 y Fórmula 1 🏎️
        </p>
    </div>
    """, unsafe_allow_html=True)


def render_featured_products():
    """
    Renderiza la sección de productos destacados.
    """
    st.markdown("## ⭐ Productos Destacados")
    st.markdown("Los más vendidos de todas las categorías")

    # Obtener productos destacados
    featured_products = ProductService.get_featured_products(limit=8)

    # Mostrar en grid
    render_product_grid(featured_products, key_prefix="featured")


def render_filtered_catalog():
    """
    Renderiza el catálogo de productos filtrado por deporte, equipo y categoría.
    """
    selected_sport = st.session_state.get("selected_sport")
    selected_team = st.session_state.get("selected_team", None)
    selected_category = st.session_state.get("selected_category", None)

    # Construir título dinámico
    sport_names = {
        "futbol": "Fútbol ⚽",
        "baloncesto": "Baloncesto 🏀",
        "formula1": "Fórmula 1 🏎️"
    }

    title = sport_names.get(selected_sport, "Productos")

    if selected_team:
        title += f" - {selected_team}"

    if selected_category:
        title += f" - {selected_category}"

    st.markdown(f"## 🛍️ {title}")

    # Información de filtros activos
    filter_info = []
    if selected_team:
        filter_info.append(f"Equipo: **{selected_team}**")
    if selected_category:
        filter_info.append(f"Categoría: **{selected_category}**")

    if filter_info:
        st.markdown(f"*Filtros activos:* {' | '.join(filter_info)}")

    st.markdown("<br>", unsafe_allow_html=True)

    # Obtener productos filtrados
    products = ProductService.get_products_by_sport(
        sport_id=selected_sport,
        team=selected_team,
        categoria=selected_category,
        limit=20
    )

    # Mostrar número de resultados
    if products:
        st.markdown(f"*Mostrando {len(products)} productos*")
    else:
        st.info("🔍 No se encontraron productos con los filtros seleccionados. Intenta cambiar los filtros.")
        return

    st.markdown("<br>", unsafe_allow_html=True)

    # Mostrar productos en grid
    render_product_grid(products, key_prefix="catalog")


def render_search_bar():
    """
    Renderiza una barra de búsqueda de productos.
    """
    st.markdown("### 🔎 Buscar Productos")

    col1, col2 = st.columns([4, 1])

    with col1:
        search_query = st.text_input(
            "Búsqueda",
            placeholder="Busca por nombre, equipo o categoría...",
            label_visibility="collapsed",
            key="search_query"
        )

    with col2:
        search_button = st.button("Buscar", use_container_width=True, type="primary")

    if search_button and search_query:
        # Buscar productos
        results = ProductService.search_products(search_query)

        st.markdown(f"### Resultados para '{search_query}'")
        st.markdown(f"*{len(results)} productos encontrados*")

        if results:
            render_product_grid(results, key_prefix="search")
        else:
            st.warning(f"No se encontraron productos para '{search_query}'")
