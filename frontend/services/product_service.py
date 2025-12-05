"""
Servicio de productos para el frontend.
Gestiona la obtención y filtrado de productos desde BBDD.json.
"""

import json
import os
from typing import List, Dict, Optional


class ProductService:
    """
    Servicio para gestionar productos.
    """

    @staticmethod
    def _load_data() -> dict:
        """
        Carga los datos desde el archivo BBDD.json.

        Returns:
            dict: Datos completos de la base de datos
        """
        # Obtener la ruta del archivo BBDD.json
        current_dir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
        json_path = os.path.join(current_dir, 'data', 'BBDD.json')

        try:
            with open(json_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            print(f"⚠️ No se encontró el archivo BBDD.json en {json_path}")
            return {"products": [], "categories": [], "leagues": []}
        except json.JSONDecodeError:
            print(f"⚠️ Error al decodificar el archivo BBDD.json")
            return {"products": [], "categories": [], "leagues": []}

    @staticmethod
    def _map_product(product: dict) -> dict:
        """
        Mapea un producto del formato JSON al formato esperado por el frontend.

        Args:
            product: Producto en formato JSON

        Returns:
            dict: Producto en formato frontend
        """
        # Calcular stock total
        stock_dict = product.get('stock', {})
        total_stock = sum(stock_dict.values()) if isinstance(stock_dict, dict) else 0

        return {
            "id": product.get("id"),
            "name": product.get("name"),
            "deporte": product.get("category"),  # futbol, formula1, baloncesto
            "equipo": product.get("team"),
            "categoria": "Camiseta",  # Por ahora todas son camisetas
            "precio": product.get("price", 0),
            "precio_personalizacion": 10.00,  # Precio fijo de personalización
            "permite_personalizacion": True,
            "stock": total_stock,
            "tallas": product.get("sizes", []),
            "imagen_url": product.get("images", {}).get("main", "https://via.placeholder.com/400x400?text=Sin+Imagen"),
            "destacado": product.get("featured", False),
            "descripcion": product.get("description", "Producto oficial de alta calidad.")
        }

    @staticmethod
    def get_sports() -> List[Dict[str, str]]:
        """
        Obtiene la lista de deportes disponibles.

        Returns:
            List[Dict]: Lista de deportes con icono y nombre
        """
        return [
            {"id": "futbol", "name": "Fútbol", "icon": "⚽", "color": "#10b981"},
            {"id": "baloncesto", "name": "Baloncesto", "icon": "🏀", "color": "#f59e0b"},
            {"id": "formula1", "name": "Fórmula 1", "icon": "🏎️", "color": "#ef4444"}
        ]

    @staticmethod
    def get_teams_by_sport(sport_id: str) -> List[str]:
        """
        Obtiene los equipos disponibles por deporte.

        Args:
            sport_id: ID del deporte (futbol, baloncesto, formula1)

        Returns:
            List[str]: Lista de nombres de equipos
        """
        teams_data = {
            "futbol": [
                "Real Madrid CF",
                "FC Barcelona",
                "Atlético de Madrid",
                "Sevilla FC",
                "Valencia CF",
                "Real Betis",
                "Athletic Club",
                "Real Sociedad",
                "Selección Española"
            ],
            "baloncesto": [
                "Real Madrid Baloncesto",
                "FC Barcelona Basket",
                "Valencia Basket",
                "Saski Baskonia",
                "Unicaja Málaga",
                "Joventut Badalona",
                "UCAM Murcia"
            ],
            "formula1": [
                "Scuderia Ferrari",
                "Red Bull Racing",
                "Mercedes-AMG Petronas",
                "McLaren Racing",
                "Aston Martin F1",
                "Alpine F1 Team",
                "Williams Racing",
                "Alfa Romeo",
                "Haas F1 Team",
                "Scuderia AlphaTauri"
            ]
        }
        return teams_data.get(sport_id, [])

    @staticmethod
    def get_categories() -> List[str]:
        """
        Obtiene las categorías de productos disponibles.

        Returns:
            List[str]: Lista de categorías
        """
        return [
            "Camiseta",
            "Sudadera",
            "Chaqueta",
            "Gorra",
            "Bufanda",
            "Pantalón"
        ]

    @staticmethod
    def get_featured_products(limit: int = 8) -> List[Dict]:
        """
        Obtiene productos destacados para mostrar en home.

        Args:
            limit: Número máximo de productos a retornar

        Returns:
            List[Dict]: Lista de productos destacados
        """
        data = ProductService._load_data()
        products = data.get('products', [])

        # Filtrar solo productos activos
        active_products = [p for p in products if p.get('active', True)]

        # Mapear productos al formato del frontend
        mapped_products = [ProductService._map_product(p) for p in active_products]

        return mapped_products[:limit]

    @staticmethod
    def get_products_by_sport(
        sport_id: str,
        team: Optional[str] = None,
        categoria: Optional[str] = None,
        limit: int = 20
    ) -> List[Dict]:
        """
        Obtiene productos filtrados por deporte, equipo y categoría.

        Args:
            sport_id: ID del deporte
            team: Nombre del equipo (opcional)
            categoria: Categoría del producto (opcional)
            limit: Número máximo de productos

        Returns:
            List[Dict]: Lista de productos filtrados
        """
        data = ProductService._load_data()
        products = data.get('products', [])

        # Filtrar solo productos activos
        active_products = [p for p in products if p.get('active', True)]

        # Filtrar por deporte (category en JSON)
        filtered = [p for p in active_products if p.get("category") == sport_id]

        # Filtrar por equipo si se especifica
        if team:
            filtered = [p for p in filtered if p.get("team") == team]

        # Filtrar por categoría si se especifica (por ahora no se usa en JSON)
        if categoria:
            filtered = [p for p in filtered if p.get("categoria") == categoria]

        # Mapear productos al formato del frontend
        mapped_products = [ProductService._map_product(p) for p in filtered]

        return mapped_products[:limit]

    @staticmethod
    def get_product_by_id(product_id: str) -> Optional[Dict]:
        """
        Obtiene un producto por su ID.

        Args:
            product_id: ID del producto

        Returns:
            Optional[Dict]: Producto o None si no se encuentra
        """
        data = ProductService._load_data()
        products = data.get('products', [])

        for product in products:
            if product.get("id") == product_id and product.get('active', True):
                return ProductService._map_product(product)

        return None

    @staticmethod
    def search_products(query: str) -> List[Dict]:
        """
        Busca productos por nombre, equipo o categoría.

        Args:
            query: Término de búsqueda

        Returns:
            List[Dict]: Lista de productos que coinciden con la búsqueda
        """
        data = ProductService._load_data()
        products = data.get('products', [])

        # Filtrar solo productos activos
        active_products = [p for p in products if p.get('active', True)]

        query_lower = query.lower()

        # Buscar en nombre, equipo y descripción
        results = [
            p for p in active_products
            if query_lower in p.get("name", "").lower()
            or query_lower in p.get("team", "").lower()
            or query_lower in p.get("description", "").lower()
        ]

        # Mapear productos al formato del frontend
        mapped_results = [ProductService._map_product(p) for p in results]

        return mapped_results
