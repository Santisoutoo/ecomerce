"""
Página principal (Home) de SportStyle Store.
Muestra selección de deportes, productos destacados y catálogo filtrado.
"""

import streamlit as st
from components.sport_selector import render_sport_selector, render_filters_sidebar
from components.product_card import render_product_grid
from services.product_service import ProductService


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

    # Botón de volver prominente
    col_back, col_title = st.columns([1, 5])

    with col_back:
        if st.button("← Volver al Inicio", type="primary", use_container_width=True):
            st.session_state["selected_sport"] = None
            st.session_state["selected_team"] = None
            st.session_state["selected_category"] = None
            st.session_state["selected_size"] = None
            st.session_state["price_range"] = None
            st.rerun()

    # Construir título dinámico
    sport_names = {
        "futbol": "Fútbol ⚽",
        "baloncesto": "Baloncesto 🏀",
        "formula1": "Fórmula 1 🏎️"
    }

    with col_title:
        st.markdown(f"## 🛍️ {sport_names.get(selected_sport, 'Productos')}")

    st.markdown("---")

    # Layout: Filtros (sidebar) | Productos
    col_filters, col_products = st.columns([1, 3], gap="large")

    with col_filters:
        filters = render_inline_filters(selected_sport)

    with col_products:
        render_products_with_filters(selected_sport, filters)


def render_inline_filters(sport_id: str) -> dict:
    """
    Renderiza filtros inline para la vista de deporte.

    Args:
        sport_id: ID del deporte seleccionado

    Returns:
        dict: Diccionario con los filtros seleccionados
    """
    st.markdown("### 🔍 Filtros")

    filters = {}

    # Filtro por equipo
    st.markdown("#### 🏟️ Equipo")
    teams = ProductService.get_teams_by_sport(sport_id)
    team_options = ["Todos"] + teams
    selected_team = st.selectbox(
        "Selecciona equipo",
        options=team_options,
        key="filter_team",
        label_visibility="collapsed"
    )
    filters['team'] = selected_team if selected_team != "Todos" else None

    st.markdown("---")

    # Filtro por categoría
    st.markdown("#### 👕 Categoría")
    categories = ProductService.get_categories()
    category_options = ["Todas"] + categories
    selected_category = st.selectbox(
        "Selecciona categoría",
        options=category_options,
        key="filter_category",
        label_visibility="collapsed"
    )
    filters['category'] = selected_category if selected_category != "Todas" else None

    st.markdown("---")

    # Filtro por talla
    st.markdown("#### 📏 Talla")
    size_options = ["Todas", "XS", "S", "M", "L", "XL", "XXL"]
    selected_size = st.selectbox(
        "Selecciona talla",
        options=size_options,
        key="filter_size",
        label_visibility="collapsed"
    )
    filters['size'] = selected_size if selected_size != "Todas" else None

    st.markdown("---")

    # Filtro por rango de precio
    st.markdown("#### 💰 Precio")
    price_range = st.slider(
        "Rango de precio (€)",
        min_value=0,
        max_value=200,
        value=(0, 200),
        step=5,
        key="filter_price_range"
    )
    filters['price_min'] = price_range[0]
    filters['price_max'] = price_range[1]

    st.markdown("---")

    # Filtro por disponibilidad
    st.markdown("#### 📦 Disponibilidad")
    only_in_stock = st.checkbox(
        "Solo productos en stock",
        value=True,
        key="filter_stock"
    )
    filters['only_in_stock'] = only_in_stock

    st.markdown("---")

    # Botón para limpiar filtros
    if st.button("🔄 Limpiar Filtros", use_container_width=True, type="secondary"):
        for key in ['filter_team', 'filter_category', 'filter_size', 'filter_price_range', 'filter_stock']:
            if key in st.session_state:
                del st.session_state[key]
        st.rerun()

    return filters


def render_products_with_filters(sport_id: str, filters: dict):
    """
    Renderiza los productos aplicando los filtros seleccionados.

    Args:
        sport_id: ID del deporte seleccionado
        filters: Diccionario con los filtros activos
    """
    # Obtener productos base por deporte
    products = ProductService.get_products_by_sport(
        sport_id=sport_id,
        team=filters.get('team'),
        categoria=filters.get('category'),
        limit=100
    )

    # Aplicar filtros adicionales
    filtered_products = products

    # Filtro por talla
    if filters.get('size'):
        filtered_products = [p for p in filtered_products if filters['size'] in p.get('tallas', [])]

    # Filtro por precio
    price_min = filters.get('price_min', 0)
    price_max = filters.get('price_max', 999999)
    filtered_products = [p for p in filtered_products if price_min <= p.get('precio', 0) <= price_max]

    # Filtro por stock
    if filters.get('only_in_stock', True):
        filtered_products = [p for p in filtered_products if p.get('stock', 0) > 0]

    # Controles de ordenamiento y contador
    col_sort, col_count = st.columns([2, 1])

    with col_sort:
        sort_options = {
            "Más relevantes": "relevance",
            "Precio: menor a mayor": "price_asc",
            "Precio: mayor a menor": "price_desc",
            "Nombre: A-Z": "name_asc"
        }

        selected_sort = st.selectbox(
            "Ordenar por",
            options=list(sort_options.keys()),
            key="sport_sort"
        )

        # Aplicar ordenamiento
        if sort_options[selected_sort] == "price_asc":
            filtered_products = sorted(filtered_products, key=lambda p: p.get('precio', 0))
        elif sort_options[selected_sort] == "price_desc":
            filtered_products = sorted(filtered_products, key=lambda p: p.get('precio', 0), reverse=True)
        elif sort_options[selected_sort] == "name_asc":
            filtered_products = sorted(filtered_products, key=lambda p: p.get('name', ''))

    with col_count:
        st.markdown(f"""
        <div style="
            background: #1e1b4b;
            border: 1px solid #a78bfa;
            border-radius: 8px;
            padding: 0.75rem;
            text-align: center;
            margin-top: 1.6rem;
        ">
            <p style="color: #a78bfa; font-weight: 600; margin: 0;">
                {len(filtered_products)} producto{'s' if len(filtered_products) != 1 else ''}
            </p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # Mostrar productos
    if not filtered_products:
        st.info("🔍 No se encontraron productos con los filtros seleccionados. Intenta ajustar los filtros.")
        return

    # Mostrar productos en grid
    render_product_grid(filtered_products, key_prefix="sport")


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
