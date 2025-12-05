"""
Página de administración - Dashboard BI mejorado.
Solo accesible para usuarios administradores.
"""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta
import random
import json
from config import SESSION_KEYS


def render_admin_page():
    """
    Renderiza la página de administración con dashboard BI mejorado.
    """
    # Verificar si el usuario es admin
    if not is_admin():
        render_access_denied()
        return

    # Header del dashboard
    st.markdown("""
    <div style="text-align: center; padding: 1rem 0 2rem 0;">
        <h1 style="color: #a78bfa; font-family: 'Exo 2', sans-serif; font-size: 2.5rem; margin: 0;">
            📊 Panel de Administración
        </h1>
        <p style="color: #d1d5db; font-size: 1.1rem; margin: 0.5rem 0 0 0;">
            Dashboard de Business Intelligence - Vista general del negocio
        </p>
    </div>
    """, unsafe_allow_html=True)

    # Mostrar loader mientras carga
    with st.spinner("Cargando métricas del dashboard..."):
        # Métricas principales en cards animados
        render_main_metrics_animated()

        st.markdown("<br>", unsafe_allow_html=True)

        # Top 3 productos - posición prominente
        render_top_products_section()

        st.markdown("---")

        # Layout principal: Gráficos e indicadores
        col_left, col_right = st.columns([2.5, 1.5], gap="large")

        with col_left:
            # Gráfico de ingresos interactivo con Plotly
            render_revenue_chart_plotly()

            st.markdown("<br>", unsafe_allow_html=True)

            # Mapa de España con heatmap de usuarios
            render_spain_heatmap()

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
    # Verificar si el email contiene "admin"
    user_email = st.session_state.get(SESSION_KEYS["user_email"], "")
    return "admin" in user_email.lower() if user_email else False


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


def render_main_metrics_animated():
    """
    Renderiza las métricas principales en cards con animaciones hover.
    """
    # Datos mock
    total_users = 1247
    new_users_today = 23
    users_change = 27.8

    total_revenue = 45678.90
    revenue_change_year = 3600.2
    revenue_change_month = 17.3

    total_orders = 543

    # CSS para animaciones hover
    st.markdown("""
    <style>
        .metric-card-animated {
            background: linear-gradient(135deg, #1e1b4b 0%, #2d2d3a 100%);
            border: 2px solid #2d2d3a;
            border-radius: 16px;
            padding: 1.5rem;
            text-align: center;
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
            cursor: pointer;
            height: 100%;
        }
        .metric-card-animated:hover {
            transform: translateY(-8px) scale(1.02);
            border-color: #a78bfa;
            box-shadow: 0 12px 32px rgba(167, 139, 250, 0.4);
            background: linear-gradient(135deg, #2d2d3a 0%, #1e1b4b 100%);
        }
        .metric-icon {
            font-size: 2rem;
            margin-bottom: 0.5rem;
            display: block;
            transition: transform 0.3s ease;
        }
        .metric-card-animated:hover .metric-icon {
            transform: scale(1.2) rotate(5deg);
        }
        .metric-value {
            color: #ffffff;
            font-size: 2rem;
            font-weight: 700;
            margin: 0.5rem 0;
        }
        .metric-label {
            color: #9ca3af;
            font-size: 0.875rem;
            margin: 0;
        }
        .metric-change {
            font-size: 0.875rem;
            font-weight: 600;
            margin: 0.5rem 0 0 0;
        }
        .metric-change.positive {
            color: #10b981;
        }
        .metric-change.negative {
            color: #ef4444;
        }
    </style>
    """, unsafe_allow_html=True)

    # Cards de métricas
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.markdown(f"""
        <div class="metric-card-animated">
            <span class="metric-icon">👥</span>
            <p class="metric-label">Usuarios Totales</p>
            <p class="metric-value">{total_users:,}</p>
            <p class="metric-label">{new_users_today} nuevos hoy</p>
            <p class="metric-change positive">▲ {users_change:.1f}%</p>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown(f"""
        <div class="metric-card-animated">
            <span class="metric-icon">💰</span>
            <p class="metric-label">Ingresos Totales</p>
            <p class="metric-value">{total_revenue:,.2f}€</p>
            <p class="metric-change positive">▲ {revenue_change_year:.1f}% vs ayer</p>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown(f"""
        <div class="metric-card-animated">
            <span class="metric-icon">📈</span>
            <p class="metric-label">Ingresos Mes</p>
            <p class="metric-value">{total_revenue:,.2f}€</p>
            <p class="metric-change positive">▲ {revenue_change_month:.1f}% vs mes anterior</p>
        </div>
        """, unsafe_allow_html=True)

    with col4:
        st.markdown(f"""
        <div class="metric-card-animated">
            <span class="metric-icon">📦</span>
            <p class="metric-label">Pedidos Totales</p>
            <p class="metric-value">{total_orders:,}</p>
        </div>
        """, unsafe_allow_html=True)


def render_revenue_chart_plotly():
    """
    Renderiza el gráfico de ingresos interactivo con Plotly (hover con cifras exactas).
    """
    st.markdown("### 📈 Ingresos - Últimos 30 Días")

    # Generar datos mock
    dates = [(datetime.now() - timedelta(days=i)).strftime("%d %b") for i in range(30, 0, -1)]
    revenues = [random.uniform(800, 2000) for _ in range(30)]

    # Crear gráfico interactivo con Plotly
    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=dates,
        y=revenues,
        mode='lines+markers',
        name='Ingresos',
        line=dict(color='#a78bfa', width=3),
        marker=dict(size=6, color='#a78bfa'),
        fill='tozeroy',
        fillcolor='rgba(167, 139, 250, 0.2)',
        hovertemplate='<b>%{x}</b><br>Ingresos: %{y:,.2f}€<extra></extra>'
    ))

    fig.update_layout(
        plot_bgcolor='#121127',
        paper_bgcolor='#181633',
        font=dict(color='#d1d5db', family='Inter, sans-serif'),
        xaxis=dict(
            showgrid=False,
            linecolor='#2d2d3a',
            tickangle=-45
        ),
        yaxis=dict(
            showgrid=True,
            gridcolor='#2d2d3a',
            linecolor='#2d2d3a',
            title='Ingresos (€)'
        ),
        hovermode='x unified',
        hoverlabel=dict(
            bgcolor='#1e1b4b',
            font_size=14,
            font_family='Inter, sans-serif',
            bordercolor='#a78bfa'
        ),
        margin=dict(l=50, r=20, t=20, b=80),
        height=400
    )

    st.plotly_chart(fig, use_container_width=True)

    # Resumen con métricas
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


def render_spain_heatmap():
    """
    Renderiza mapa de España con heatmap de usuarios por comunidad autónoma.
    """
    st.markdown("### 🗺️ Usuarios por Comunidad Autónoma")

    # Datos mock de usuarios por comunidad con coordenadas aproximadas
    regions_data = {
        "Madrid": {"users": 287, "percentage": 23.0, "lat": 40.4168, "lon": -3.7038},
        "Cataluña": {"users": 245, "percentage": 19.6, "lat": 41.3851, "lon": 2.1734},
        "Andalucía": {"users": 198, "percentage": 15.9, "lat": 37.3891, "lon": -5.9845},
        "Valencia": {"users": 156, "percentage": 12.5, "lat": 39.4699, "lon": -0.3763},
        "País Vasco": {"users": 98, "percentage": 7.9, "lat": 43.2630, "lon": -2.9350},
        "Galicia": {"users": 76, "percentage": 6.1, "lat": 42.8782, "lon": -8.5448},
        "Castilla y León": {"users": 54, "percentage": 4.3, "lat": 41.6523, "lon": -4.7245},
        "Aragón": {"users": 43, "percentage": 3.4, "lat": 41.6488, "lon": -0.8891},
        "Murcia": {"users": 38, "percentage": 3.0, "lat": 37.9922, "lon": -1.1307},
        "Castilla-La Mancha": {"users": 35, "percentage": 2.8, "lat": 39.8628, "lon": -4.0273},
        "Canarias": {"users": 17, "percentage": 1.5, "lat": 28.2916, "lon": -16.6291}
    }

    # Preparar datos para el mapa
    df_map = pd.DataFrame([
        {
            "region": region,
            "users": data["users"],
            "percentage": data["percentage"],
            "lat": data["lat"],
            "lon": data["lon"],
            "size": data["users"] / 5  # Para el tamaño de los marcadores
        }
        for region, data in regions_data.items()
    ])

    # Crear mapa con Plotly
    fig = go.Figure()

    # Agregar marcadores con tamaño proporcional a usuarios (reducidos)
    fig.add_trace(go.Scattergeo(
        lon=df_map['lon'],
        lat=df_map['lat'],
        text=df_map['region'],
        mode='markers',
        marker=dict(
            size=df_map['users'] / 10,  # Tamaño reducido para que no sean tan grandes
            color=df_map['users'],
            colorscale='Purples',
            cmin=0,
            cmax=300,
            colorbar=dict(
                title="Usuarios",
                thickness=15,
                len=0.7,
                bgcolor='#f3f4f6',
                bordercolor='#a78bfa',
                borderwidth=1,
                tickfont=dict(color='#1e1b4b'),
                titlefont=dict(color='#a78bfa')
            ),
            line=dict(width=2, color='#7c3aed'),
            opacity=0.7
        ),
        hovertemplate='<b>%{text}</b><br>' +
                      'Usuarios: %{marker.color:,}<br>' +
                      '<extra></extra>'
    ))

    # Configuración del mapa centrado mejor en España con fondo claro
    fig.update_geos(
        center=dict(lat=40.2, lon=-3.7),  # Mejor centrado en España
        projection_scale=7.5,  # Más zoom para España
        visible=False,
        showcountries=True,
        countrycolor='#9ca3af',
        bgcolor='#f3f4f6',  # Fondo claro gris
        landcolor='#e5e7eb',  # España en gris claro
        coastlinecolor='#6b7280',
        lakecolor='#dbeafe',  # Lagos azul claro
        showlakes=True,
        resolution=50
    )

    fig.update_layout(
        height=500,
        margin=dict(l=0, r=0, t=0, b=0),
        paper_bgcolor='#f9fafb',  # Fondo papel claro
        geo=dict(
            bgcolor='#f3f4f6'  # Fondo geo claro
        ),
        hoverlabel=dict(
            bgcolor='#ffffff',
            font_size=14,
            font_family='Inter, sans-serif',
            bordercolor='#a78bfa',
            font_color='#1e1b4b'
        )
    )

    st.plotly_chart(fig, use_container_width=True)

    # Menú desplegable con detalles de comunidades
    with st.expander("📋 Ver Detalles por Comunidad", expanded=False):
        st.markdown("#### Desglose Detallado")

        # Ordenar por usuarios descendente
        sorted_regions = sorted(regions_data.items(), key=lambda x: x[1]['users'], reverse=True)

        for region, data in sorted_regions:
            # Calcular intensidad del color según porcentaje
            intensity = data['percentage'] / 25

            st.markdown(f"""
            <div style="
                background: linear-gradient(90deg,
                    rgba(167, 139, 250, {intensity}) 0%,
                    rgba(30, 27, 75, 0.3) {data['percentage']*3}%,
                    #181633 100%);
                border: 1px solid #2d2d3a;
                border-radius: 8px;
                padding: 0.75rem 1rem;
                margin-bottom: 0.5rem;
                display: flex;
                justify-content: space-between;
                align-items: center;
                transition: all 0.3s ease;
            ">
                <div style="flex: 1;">
                    <span style="color: #ffffff; font-weight: 600;">{region}</span>
                </div>
                <div style="text-align: right;">
                    <span style="color: #a78bfa; font-weight: 700; margin-right: 1rem;">{data['users']} usuarios</span>
                    <span style="color: #d1d5db; font-size: 0.875rem;">({data['percentage']:.1f}%)</span>
                </div>
            </div>
            """, unsafe_allow_html=True)


def render_top_products_section():
    """
    Renderiza sección destacada de Top 3 productos más vendidos.
    """
    st.markdown("""
    <div style="text-align: center; padding: 1rem 0;">
        <h2 style="color: #a78bfa; font-family: 'Exo 2', sans-serif; font-size: 1.75rem; margin: 0;">
            🏆 Top 3 Productos Más Vendidos
        </h2>
    </div>
    """, unsafe_allow_html=True)

    top_products = [
        {"name": "Camiseta Real Madrid", "sales": 234, "revenue": "9,360€", "icon": "⚽", "color": "#10b981"},
        {"name": "Camiseta FC Barcelona", "sales": 198, "revenue": "7,920€", "icon": "⚽", "color": "#3b82f6"},
        {"name": "Gorra Ferrari F1", "sales": 156, "revenue": "3,120€", "icon": "🏎️", "color": "#f59e0b"}
    ]

    medals = ["🥇", "🥈", "🥉"]

    # CSS para las tarjetas de productos
    st.markdown("""
    <style>
        .top-product-card {
            background: linear-gradient(135deg, #1e1b4b 0%, #181633 100%);
            border: 2px solid #2d2d3a;
            border-radius: 16px;
            padding: 1.5rem;
            text-align: center;
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
            cursor: pointer;
            height: 100%;
        }
        .top-product-card:hover {
            transform: translateY(-8px) scale(1.03);
            border-color: #a78bfa;
            box-shadow: 0 12px 32px rgba(167, 139, 250, 0.4);
        }
        .product-medal {
            font-size: 3rem;
            margin-bottom: 0.5rem;
            display: block;
        }
        .product-icon {
            font-size: 2rem;
            margin-bottom: 0.5rem;
        }
        .product-name {
            color: #ffffff;
            font-size: 1.1rem;
            font-weight: 600;
            margin: 0.5rem 0;
        }
        .product-sales {
            color: #a78bfa;
            font-size: 1.5rem;
            font-weight: 700;
            margin: 0.5rem 0;
        }
        .product-revenue {
            color: #10b981;
            font-size: 1rem;
            font-weight: 600;
            margin: 0.25rem 0;
        }
    </style>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)
    cols = [col1, col2, col3]

    for i, (product, medal) in enumerate(zip(top_products, medals)):
        with cols[i]:
            st.markdown(f"""
            <div class="top-product-card">
                <span class="product-medal">{medal}</span>
                <span class="product-icon">{product['icon']}</span>
                <p class="product-name">{product['name']}</p>
                <p class="product-sales">{product['sales']} ventas</p>
                <p class="product-revenue">{product['revenue']}</p>
            </div>
            """, unsafe_allow_html=True)


def render_stock_by_category():
    """
    Renderiza el stock por categorías con gráfico de dona interactivo.
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

    # Gráfico de dona interactivo
    fig = go.Figure(data=[go.Pie(
        labels=[item['categoria'] for item in stock_data],
        values=[item['stock'] for item in stock_data],
        hole=0.5,
        marker=dict(colors=[item['color'] for item in stock_data]),
        hovertemplate='<b>%{label}</b><br>Stock: %{value:,}<br>%{percent}<extra></extra>',
        textposition='inside',
        textinfo='label'
    )])

    fig.update_layout(
        showlegend=False,
        paper_bgcolor='#181633',
        plot_bgcolor='#181633',
        font=dict(color='#d1d5db', family='Inter, sans-serif'),
        height=350,
        margin=dict(l=20, r=20, t=20, b=20),
        hoverlabel=dict(
            bgcolor='#1e1b4b',
            font_size=14,
            font_family='Inter, sans-serif',
            bordercolor='#a78bfa'
        )
    )

    st.plotly_chart(fig, use_container_width=True)


def render_additional_metrics():
    """
    Renderiza métricas adicionales con animaciones.
    """
    st.markdown("### 📊 Métricas Adicionales")

    # CSS para animaciones
    st.markdown("""
    <style>
        .additional-metric {
            background: #181633;
            border: 1px solid #2d2d3a;
            border-radius: 12px;
            padding: 1.5rem;
            margin-bottom: 1rem;
            transition: all 0.3s ease;
        }
        .additional-metric:hover {
            border-color: #a78bfa;
            box-shadow: 0 4px 16px rgba(167, 139, 250, 0.3);
            transform: translateX(4px);
        }
    </style>
    """, unsafe_allow_html=True)

    # Tasa de conversión
    st.markdown("""
    <div class="additional-metric">
        <p style="color: #9ca3af; font-size: 0.875rem; margin: 0 0 0.5rem 0;">Tasa de Conversión</p>
        <p style="color: #10b981; font-size: 2rem; font-weight: 700; margin: 0;">4.3%</p>
        <p style="color: #10b981; font-size: 0.875rem; margin: 0.5rem 0 0 0;">▲ 0.8% vs mes anterior</p>
    </div>
    """, unsafe_allow_html=True)

    # Ticket medio
    st.markdown("""
    <div class="additional-metric">
        <p style="color: #9ca3af; font-size: 0.875rem; margin: 0 0 0.5rem 0;">Ticket Medio</p>
        <p style="color: #a78bfa; font-size: 2rem; font-weight: 700; margin: 0;">84.12€</p>
        <p style="color: #ef4444; font-size: 0.875rem; margin: 0.5rem 0 0 0;">▼ 2.3% vs mes anterior</p>
    </div>
    """, unsafe_allow_html=True)

    # Productos activos
    st.markdown("""
    <div class="additional-metric">
        <p style="color: #9ca3af; font-size: 0.875rem; margin: 0 0 0.5rem 0;">Productos Activos</p>
        <p style="color: #3b82f6; font-size: 2rem; font-weight: 700; margin: 0;">247</p>
        <p style="color: #d1d5db; font-size: 0.875rem; margin: 0.5rem 0 0 0;">En catálogo</p>
    </div>
    """, unsafe_allow_html=True)
