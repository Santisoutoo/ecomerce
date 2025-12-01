"""
Página de administración - Dashboard BI.
Solo accesible para usuarios administradores.
"""

import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import random
from config import SESSION_KEYS


def render_admin_page():
    """
    Renderiza la página de administración con dashboard BI.
    """
    # Verificar si el usuario es admin
    if not is_admin():
        render_access_denied()
        return

    st.title("📊 Panel de Administración")
    st.markdown("Dashboard de Business Intelligence - Vista general del negocio")

    # Mostrar loader mientras carga
    with st.spinner("Cargando métricas del dashboard..."):
        # Métricas principales en cards
        render_main_metrics()

        st.markdown("---")

        # Layout de 2 columnas
        col_left, col_right = st.columns([2, 1], gap="large")

        with col_left:
            # Gráfico de ingresos en el tiempo
            render_revenue_chart()

            st.markdown("<br>", unsafe_allow_html=True)

            # Usuarios por región
            render_users_by_region()

        with col_right:
            # Stock por categorías
            render_stock_by_category()

            st.markdown("<br>", unsafe_allow_html=True)

            # Métricas adicionales
            render_additional_metrics()


def is_admin() -> bool:
    """
    Verifica si el usuario actual es administrador.

    Returns:
        bool: True si es admin, False en caso contrario
    """
    # Mock: Por ahora, cualquier usuario con email que contenga "admin" es admin
    # En producción, esto vendría de la base de datos
    user_email = st.session_state.get(SESSION_KEYS["user_email"], "")
    return "admin" in user_email.lower()


def render_access_denied():
    """
    Renderiza mensaje de acceso denegado.
    """
    st.markdown("""
    <div style="
        background: #181633;
        border: 2px solid #ef4444;
        border-radius: 16px;
        padding: 3rem;
        text-align: center;
        margin: 2rem 0;
    ">
        <p style="font-size: 4rem; margin: 0;">🚫</p>
        <h2 style="color: #ef4444; margin: 1rem 0;">Acceso Denegado</h2>
        <p style="color: #9ca3af; margin: 0;">
            No tienes permisos para acceder a esta página.
        </p>
        <p style="color: #9ca3af; font-size: 0.875rem; margin: 1rem 0 0 0;">
            Esta sección es solo para administradores.
        </p>
    </div>
    """, unsafe_allow_html=True)

    if st.button("🏠 Volver al Inicio", type="primary"):
        st.session_state[SESSION_KEYS["current_page"]] = "home"
        st.rerun()


def render_main_metrics():
    """
    Renderiza las métricas principales en cards.
    """
    # Datos mock
    total_users = 1247
    new_users_today = 23
    new_users_yesterday = 18
    users_change = ((new_users_today - new_users_yesterday) / new_users_yesterday * 100)

    total_revenue = 45678.90
    revenue_yesterday = 1234.50
    revenue_last_month = 38950.20
    revenue_change_day = ((total_revenue - revenue_yesterday) / revenue_yesterday * 100) if revenue_yesterday > 0 else 0
    revenue_change_month = ((total_revenue - revenue_last_month) / revenue_last_month * 100) if revenue_last_month > 0 else 0

    total_orders = 543
    total_stock = 12450

    # Cards de métricas
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        render_metric_card(
            "👥 Usuarios Totales",
            total_users,
            new_users_today,
            users_change,
            "nuevos hoy"
        )

    with col2:
        render_metric_card(
            "💰 Ingresos Totales",
            f"{total_revenue:,.2f}€",
            None,
            revenue_change_day,
            "vs ayer"
        )

    with col3:
        render_metric_card(
            "📈 Ingresos Mes",
            f"{total_revenue:,.2f}€",
            None,
            revenue_change_month,
            "vs mes anterior"
        )

    with col4:
        render_metric_card(
            "📦 Pedidos Totales",
            total_orders,
            None,
            None,
            None
        )


def render_metric_card(title: str, value, secondary_value=None, change_percent=None, change_label=None):
    """
    Renderiza una tarjeta de métrica.

    Args:
        title: Título de la métrica
        value: Valor principal
        secondary_value: Valor secundario (opcional)
        change_percent: Porcentaje de cambio (opcional)
        change_label: Etiqueta del cambio (opcional)
    """
    # Construir HTML completo usando lista para evitar f-strings anidados
    html_parts = []

    # Abrir div y agregar título y valor principal
    html_parts.append('''
    <div style="
        background: linear-gradient(135deg, #1e1b4b 0%, #2d2d3a 100%);
        border: 1px solid #a78bfa;
        border-radius: 12px;
        padding: 1.5rem;
        text-align: center;
    ">
    ''')

    html_parts.append(f'<p style="color: #9ca3af; font-size: 0.875rem; margin: 0 0 0.5rem 0;">{title}</p>')
    html_parts.append(f'<p style="color: #ffffff; font-size: 2rem; font-weight: 700; margin: 0;">{value}</p>')

    # Agregar secondary_value si existe
    if secondary_value:
        label_text = change_label if change_label else ''
        html_parts.append(f'<p style="color: #d1d5db; font-size: 0.875rem; margin: 0.5rem 0 0 0;">{secondary_value} {label_text}</p>')

    # Agregar change_percent si existe
    if change_percent is not None:
        change_color = "#10b981" if change_percent >= 0 else "#ef4444"
        change_icon = "▲" if change_percent >= 0 else "▼"
        label_text = change_label if change_label and not secondary_value else ''
        html_parts.append(f'<p style="color: {change_color}; font-size: 0.875rem; font-weight: 600; margin: 0.5rem 0 0 0;">{change_icon} {abs(change_percent):.1f}% {label_text}</p>')

    # Cerrar div
    html_parts.append('</div>')

    # Unir todas las partes y renderizar
    full_html = ''.join(html_parts)
    st.markdown(full_html, unsafe_allow_html=True)


def render_revenue_chart():
    """
    Renderiza el gráfico de ingresos en el tiempo.
    """
    st.markdown("### 📈 Ingresos - Últimos 30 Días")

    # Generar datos mock
    dates = [(datetime.now() - timedelta(days=i)) for i in range(30, 0, -1)]
    revenues = [random.uniform(800, 2000) for _ in range(30)]

    df = pd.DataFrame({
        'Fecha': dates,
        'Ingresos (€)': revenues
    })

    # Gráfico de línea
    st.line_chart(df.set_index('Fecha'))

    # Resumen
    col1, col2, col3 = st.columns(3)

    with col1:
        avg_revenue = sum(revenues) / len(revenues)
        st.metric("📊 Promedio Diario", f"{avg_revenue:.2f}€")

    with col2:
        max_revenue = max(revenues)
        st.metric("🔝 Máximo", f"{max_revenue:.2f}€")

    with col3:
        min_revenue = min(revenues)
        st.metric("📉 Mínimo", f"{min_revenue:.2f}€")


def render_users_by_region():
    """
    Renderiza el mapa/tabla de usuarios por comunidad autónoma.
    """
    st.markdown("### 🗺️ Usuarios por Comunidad Autónoma")

    # Datos mock de usuarios por comunidad
    regions_data = [
        {"region": "Madrid", "users": 287, "percentage": 23.0},
        {"region": "Cataluña", "users": 245, "percentage": 19.6},
        {"region": "Andalucía", "users": 198, "percentage": 15.9},
        {"region": "Valencia", "users": 156, "percentage": 12.5},
        {"region": "País Vasco", "users": 98, "percentage": 7.9},
        {"region": "Galicia", "users": 76, "percentage": 6.1},
        {"region": "Castilla y León", "users": 54, "percentage": 4.3},
        {"region": "Aragón", "users": 43, "percentage": 3.4},
        {"region": "Murcia", "users": 38, "percentage": 3.0},
        {"region": "Otras", "users": 52, "percentage": 4.3}
    ]

    df_regions = pd.DataFrame(regions_data)

    # Heatmap visual con barras de colores
    st.markdown("""
    <style>
        .region-bar {
            background: linear-gradient(90deg, #a78bfa 0%, #1e1b4b 100%);
            border-radius: 4px;
            padding: 0.5rem;
            margin-bottom: 0.5rem;
        }
    </style>
    """, unsafe_allow_html=True)

    for _, row in df_regions.iterrows():
        # Calcular intensidad del color según porcentaje
        intensity = row['percentage'] / 25 * 100  # Normalizar al máximo

        st.markdown(f"""
        <div style="
            background: linear-gradient(90deg,
                rgba(167, 139, 250, {intensity/100}) 0%,
                rgba(30, 27, 75, 0.3) {row['percentage']*3}%,
                #181633 100%);
            border: 1px solid #2d2d3a;
            border-radius: 8px;
            padding: 0.75rem 1rem;
            margin-bottom: 0.5rem;
            display: flex;
            justify-content: space-between;
            align-items: center;
        ">
            <div style="flex: 1;">
                <span style="color: #ffffff; font-weight: 600;">{row['region']}</span>
            </div>
            <div style="text-align: right;">
                <span style="color: #a78bfa; font-weight: 700; margin-right: 1rem;">{row['users']} usuarios</span>
                <span style="color: #d1d5db; font-size: 0.875rem;">({row['percentage']:.1f}%)</span>
            </div>
        </div>
        """, unsafe_allow_html=True)


def render_stock_by_category():
    """
    Renderiza el stock por categorías.
    """
    st.markdown("### 📦 Stock por Categoría")

    # Datos mock
    stock_data = [
        {"categoria": "Camisetas", "stock": 4567, "color": "#10b981"},
        {"categoria": "Sudaderas", "stock": 2341, "color": "#3b82f6"},
        {"categoria": "Gorras", "stock": 1876, "color": "#f59e0b"},
        {"categoria": "Bufandas", "stock": 1543, "color": "#a78bfa"},
        {"categoria": "Chaquetas", "stock": 1234, "color": "#ef4444"},
        {"categoria": "Pantalones", "stock": 889, "color": "#8b5cf6"}
    ]

    total_stock = sum(item['stock'] for item in stock_data)

    # Total
    st.markdown(f"""
    <div style="
        background: linear-gradient(135deg, #1e1b4b 0%, #2d2d3a 100%);
        border: 2px solid #a78bfa;
        border-radius: 12px;
        padding: 1.5rem;
        text-align: center;
        margin-bottom: 1.5rem;
    ">
        <p style="color: #9ca3af; font-size: 0.875rem; margin: 0;">Stock Total</p>
        <p style="color: #a78bfa; font-size: 2.5rem; font-weight: 700; margin: 0.5rem 0 0 0;">
            {total_stock:,}
        </p>
        <p style="color: #d1d5db; font-size: 0.875rem; margin: 0.5rem 0 0 0;">unidades</p>
    </div>
    """, unsafe_allow_html=True)

    # Desglose por categoría
    for item in stock_data:
        percentage = (item['stock'] / total_stock) * 100

        st.markdown(f"""
        <div style="
            background: #181633;
            border-left: 4px solid {item['color']};
            border-radius: 8px;
            padding: 1rem;
            margin-bottom: 0.75rem;
        ">
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.5rem;">
                <span style="color: #ffffff; font-weight: 600;">{item['categoria']}</span>
                <span style="color: {item['color']}; font-weight: 700; font-size: 1.1rem;">{item['stock']:,}</span>
            </div>
            <div style="background: #1e1b4b; border-radius: 4px; height: 8px; overflow: hidden;">
                <div style="
                    background: {item['color']};
                    width: {percentage}%;
                    height: 100%;
                    border-radius: 4px;
                "></div>
            </div>
            <p style="color: #9ca3af; font-size: 0.75rem; margin: 0.5rem 0 0 0; text-align: right;">
                {percentage:.1f}% del total
            </p>
        </div>
        """, unsafe_allow_html=True)


def render_additional_metrics():
    """
    Renderiza métricas adicionales.
    """
    st.markdown("### 📊 Métricas Adicionales")

    # Tasa de conversión
    st.markdown("""
    <div style="
        background: #181633;
        border: 1px solid #2d2d3a;
        border-radius: 12px;
        padding: 1.5rem;
        margin-bottom: 1rem;
    ">
        <p style="color: #9ca3af; font-size: 0.875rem; margin: 0 0 0.5rem 0;">Tasa de Conversión</p>
        <p style="color: #10b981; font-size: 2rem; font-weight: 700; margin: 0;">4.3%</p>
        <p style="color: #10b981; font-size: 0.875rem; margin: 0.5rem 0 0 0;">▲ 0.8% vs mes anterior</p>
    </div>
    """, unsafe_allow_html=True)

    # Ticket medio
    st.markdown("""
    <div style="
        background: #181633;
        border: 1px solid #2d2d3a;
        border-radius: 12px;
        padding: 1.5rem;
        margin-bottom: 1rem;
    ">
        <p style="color: #9ca3af; font-size: 0.875rem; margin: 0 0 0.5rem 0;">Ticket Medio</p>
        <p style="color: #a78bfa; font-size: 2rem; font-weight: 700; margin: 0;">84.12€</p>
        <p style="color: #ef4444; font-size: 0.875rem; margin: 0.5rem 0 0 0;">▼ 2.3% vs mes anterior</p>
    </div>
    """, unsafe_allow_html=True)

    # Productos más vendidos
    st.markdown("#### 🏆 Top 3 Productos")

    top_products = [
        {"name": "Camiseta Real Madrid", "sales": 234},
        {"name": "Camiseta FC Barcelona", "sales": 198},
        {"name": "Gorra Ferrari F1", "sales": 156}
    ]

    for i, product in enumerate(top_products, 1):
        medal = ["🥇", "🥈", "🥉"][i-1]
        st.markdown(f"""
        <div style="
            background: #1e1b4b;
            border-radius: 8px;
            padding: 0.75rem;
            margin-bottom: 0.5rem;
            display: flex;
            justify-content: space-between;
            align-items: center;
        ">
            <span style="color: #d1d5db;">
                {medal} {product['name']}
            </span>
            <span style="color: #a78bfa; font-weight: 600;">{product['sales']}</span>
        </div>
        """, unsafe_allow_html=True)
