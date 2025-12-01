"""
Página de catálogo completo con filtros avanzados.
Permite buscar, filtrar y ordenar productos.
"""

import streamlit as st
from typing import List, Dict
from services.product_service import ProductService
from components.product_card import render_product_card


def render_catalog_page():
    """
    Renderiza la página de catálogo con filtros y grid de productos.
    """
    st.title("🛍️ Catálogo de Productos")

    # Layout de 2 columnas: Filtros (sidebar) | Productos
    col_filters, col_products = st.columns([1, 3], gap="large")

    with col_filters:
        filters = render_filters_sidebar()

    with col_products:
        render_products_grid(filters)


def render_filters_sidebar() -> dict:
    """
    Renderiza la barra lateral de filtros.

    Returns:
        dict: Diccionario con los filtros seleccionados
    """
    st.markdown("### 🔍 Filtros")

    filters = {}

    # Búsqueda por texto
    search_query = st.text_input(
        "Buscar productos",
        placeholder="Nombre, equipo, categoría...",
        key="catalog_search",
        help="Busca por nombre, equipo o categoría"
    )
    filters['search'] = search_query

    st.markdown("---")

    # Filtro por deporte
    st.markdown("#### ⚽ Deporte")
    sports = ProductService.get_sports()
    sport_options = ["Todos"] + [sport["name"] for sport in sports]

    selected_sport_name = st.selectbox(
        "Selecciona deporte",
        options=sport_options,
        key="catalog_sport",
        label_visibility="collapsed"
    )

    # Obtener ID del deporte seleccionado
    if selected_sport_name != "Todos":
        selected_sport = next((s for s in sports if s["name"] == selected_sport_name), None)
        filters['sport'] = selected_sport["id"] if selected_sport else None
    else:
        filters['sport'] = None

    st.markdown("---")

    # Filtro por equipo (dinámico según deporte)
    st.markdown("#### 🏟️ Equipo")
    if filters['sport']:
        teams = ProductService.get_teams_by_sport(filters['sport'])
        team_options = ["Todos"] + teams
        selected_team = st.selectbox(
            "Selecciona equipo",
            options=team_options,
            key="catalog_team",
            label_visibility="collapsed"
        )
        filters['team'] = selected_team if selected_team != "Todos" else None
    else:
        st.info("Selecciona un deporte para filtrar por equipo")
        filters['team'] = None

    st.markdown("---")

    # Filtro por categoría
    st.markdown("#### 👕 Categoría")
    categories = ProductService.get_categories()
    category_options = ["Todas"] + categories
    selected_category = st.selectbox(
        "Selecciona categoría",
        options=category_options,
        key="catalog_category",
        label_visibility="collapsed"
    )
    filters['category'] = selected_category if selected_category != "Todas" else None

    st.markdown("---")

    # Filtro por rango de precio
    st.markdown("#### 💰 Precio")
    price_range = st.slider(
        "Rango de precio (€)",
        min_value=0,
        max_value=200,
        value=(0, 200),
        step=5,
        key="catalog_price_range"
    )
    filters['price_min'] = price_range[0]
    filters['price_max'] = price_range[1]

    st.markdown("---")

    # Filtro por disponibilidad
    st.markdown("#### 📦 Disponibilidad")
    only_in_stock = st.checkbox(
        "Solo productos en stock",
        value=True,
        key="catalog_stock"
    )
    filters['only_in_stock'] = only_in_stock

    st.markdown("---")

    # Botón para limpiar filtros
    if st.button("🔄 Limpiar Filtros", use_container_width=True, type="secondary"):
        clear_filters()

    return filters


def render_products_grid(filters: dict):
    """
    Renderiza el grid de productos con ordenamiento.

    Args:
        filters: Diccionario con los filtros seleccionados
    """
    # Obtener productos filtrados
    products = get_filtered_products(filters)

    # Controles de ordenamiento
    col_sort, col_count = st.columns([2, 1])

    with col_sort:
        sort_options = {
            "Más relevantes": "relevance",
            "Precio: menor a mayor": "price_asc",
            "Precio: mayor a menor": "price_desc",
            "Nombre: A-Z": "name_asc",
            "Nombre: Z-A": "name_desc"
        }

        selected_sort = st.selectbox(
            "Ordenar por",
            options=list(sort_options.keys()),
            key="catalog_sort"
        )

        # Aplicar ordenamiento
        products = sort_products(products, sort_options[selected_sort])

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
                {len(products)} producto{'s' if len(products) != 1 else ''}
            </p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # Mostrar productos
    if not products:
        render_no_results()
    else:
        render_product_grid(products)


def get_filtered_products(filters: dict) -> List[Dict]:
    """
    Obtiene productos aplicando todos los filtros.

    Args:
        filters: Diccionario con los filtros seleccionados

    Returns:
        List[Dict]: Lista de productos filtrados
    """
    # Si hay búsqueda, usarla primero
    if filters.get('search'):
        products = ProductService.search_products(filters['search'])
    # Si hay deporte seleccionado, filtrar por deporte
    elif filters.get('sport'):
        products = ProductService.get_products_by_sport(
            sport_id=filters['sport'],
            team=filters.get('team'),
            categoria=filters.get('category'),
            limit=100
        )
    else:
        # Obtener todos los productos
        products = ProductService.get_featured_products(limit=100)

    # Aplicar filtros adicionales
    filtered = products

    # Filtro por equipo (si no se aplicó en get_products_by_sport)
    if filters.get('team') and not filters.get('sport'):
        filtered = [p for p in filtered if p.get('equipo') == filters['team']]

    # Filtro por categoría (si no se aplicó en get_products_by_sport)
    if filters.get('category') and not filters.get('sport'):
        filtered = [p for p in filtered if p.get('categoria') == filters['category']]

    # Filtro por precio
    price_min = filters.get('price_min', 0)
    price_max = filters.get('price_max', 999999)
    filtered = [p for p in filtered if price_min <= p.get('precio', 0) <= price_max]

    # Filtro por stock
    if filters.get('only_in_stock', True):
        filtered = [p for p in filtered if p.get('stock', 0) > 0]

    return filtered


def sort_products(products: List[Dict], sort_by: str) -> List[Dict]:
    """
    Ordena los productos según el criterio seleccionado.

    Args:
        products: Lista de productos
        sort_by: Criterio de ordenamiento

    Returns:
        List[Dict]: Lista de productos ordenados
    """
    if sort_by == "price_asc":
        return sorted(products, key=lambda p: p.get('precio', 0))
    elif sort_by == "price_desc":
        return sorted(products, key=lambda p: p.get('precio', 0), reverse=True)
    elif sort_by == "name_asc":
        return sorted(products, key=lambda p: p.get('name', ''))
    elif sort_by == "name_desc":
        return sorted(products, key=lambda p: p.get('name', ''), reverse=True)
    else:  # relevance
        return products


def render_product_grid(products: List[Dict]):
    """
    Renderiza el grid de productos.

    Args:
        products: Lista de productos a mostrar
    """
    # Grid de 3 columnas
    cols_per_row = 3

    for i in range(0, len(products), cols_per_row):
        cols = st.columns(cols_per_row)

        for j, col in enumerate(cols):
            idx = i + j
            if idx < len(products):
                with col:
                    render_product_card(products[idx])
                    st.markdown("<br>", unsafe_allow_html=True)


def render_no_results():
    """
    Renderiza mensaje cuando no hay resultados.
    """
    st.markdown("""
    <div style="
        background: #181633;
        border: 2px dashed #2d2d3a;
        border-radius: 16px;
        padding: 3rem;
        text-align: center;
        margin: 2rem 0;
    ">
        <p style="font-size: 4rem; margin: 0;">🔍</p>
        <h3 style="color: #a78bfa; margin: 1rem 0;">No se encontraron productos</h3>
        <p style="color: #9ca3af; margin: 0;">
            Intenta ajustar los filtros o realizar una búsqueda diferente
        </p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    if st.button("🔄 Limpiar Filtros y Volver a Buscar", use_container_width=True, type="primary"):
        clear_filters()


def clear_filters():
    """
    Limpia todos los filtros y reinicia el catálogo.
    """
    # Limpiar todas las variables de sesión relacionadas con filtros
    filter_keys = [
        'catalog_search',
        'catalog_sport',
        'catalog_team',
        'catalog_category',
        'catalog_price_range',
        'catalog_stock',
        'catalog_sort'
    ]

    for key in filter_keys:
        if key in st.session_state:
            del st.session_state[key]

    st.rerun()
