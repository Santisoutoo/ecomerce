"""
Servicio de productos para el frontend.
Gestiona la obtención y filtrado de productos.
Por ahora usa datos mock hasta implementar el backend completo.
"""

from typing import List, Dict, Optional


class ProductService:
    """
    Servicio para gestionar productos.
    """

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
        # Datos mock de productos destacados
        products = [
            {
                "id": "prod_001",
                "name": "Camiseta Real Madrid 1ª Equipación 2024/25",
                "deporte": "futbol",
                "equipo": "Real Madrid CF",
                "categoria": "Camiseta",
                "precio": 89.99,
                "precio_personalizacion": 10.00,
                "permite_personalizacion": True,
                "stock": 50,
                "tallas": ["S", "M", "L", "XL", "XXL"],
                "imagen_url": "https://via.placeholder.com/400x400?text=Real+Madrid+Camiseta",
                "destacado": True
            },
            {
                "id": "prod_002",
                "name": "Camiseta FC Barcelona 2024/25",
                "deporte": "futbol",
                "equipo": "FC Barcelona",
                "categoria": "Camiseta",
                "precio": 89.99,
                "precio_personalizacion": 10.00,
                "permite_personalizacion": True,
                "stock": 45,
                "tallas": ["S", "M", "L", "XL", "XXL"],
                "imagen_url": "https://via.placeholder.com/400x400?text=FC+Barcelona+Camiseta",
                "destacado": True
            },
            {
                "id": "prod_003",
                "name": "Gorra Ferrari F1 2025",
                "deporte": "formula1",
                "equipo": "Scuderia Ferrari",
                "categoria": "Gorra",
                "precio": 35.00,
                "precio_personalizacion": 0,
                "permite_personalizacion": False,
                "stock": 100,
                "tallas": ["Única"],
                "imagen_url": "https://via.placeholder.com/400x400?text=Ferrari+Gorra",
                "destacado": True
            },
            {
                "id": "prod_004",
                "name": "Sudadera Real Madrid Baloncesto",
                "deporte": "baloncesto",
                "equipo": "Real Madrid Baloncesto",
                "categoria": "Sudadera",
                "precio": 65.00,
                "precio_personalizacion": 12.00,
                "permite_personalizacion": True,
                "stock": 30,
                "tallas": ["M", "L", "XL"],
                "imagen_url": "https://via.placeholder.com/400x400?text=Real+Madrid+Basket+Sudadera",
                "destacado": True
            },
            {
                "id": "prod_005",
                "name": "Camiseta Red Bull Racing 2025",
                "deporte": "formula1",
                "equipo": "Red Bull Racing",
                "categoria": "Camiseta",
                "precio": 75.00,
                "precio_personalizacion": 0,
                "permite_personalizacion": False,
                "stock": 60,
                "tallas": ["S", "M", "L", "XL"],
                "imagen_url": "https://via.placeholder.com/400x400?text=Red+Bull+Camiseta",
                "destacado": True
            },
            {
                "id": "prod_006",
                "name": "Bufanda Atlético de Madrid",
                "deporte": "futbol",
                "equipo": "Atlético de Madrid",
                "categoria": "Bufanda",
                "precio": 25.00,
                "precio_personalizacion": 0,
                "permite_personalizacion": False,
                "stock": 80,
                "tallas": ["Única"],
                "imagen_url": "https://via.placeholder.com/400x400?text=Atletico+Bufanda",
                "destacado": True
            },
            {
                "id": "prod_007",
                "name": "Camiseta FC Barcelona Basket",
                "deporte": "baloncesto",
                "equipo": "FC Barcelona Basket",
                "categoria": "Camiseta",
                "precio": 79.99,
                "precio_personalizacion": 10.00,
                "permite_personalizacion": True,
                "stock": 35,
                "tallas": ["M", "L", "XL", "XXL"],
                "imagen_url": "https://via.placeholder.com/400x400?text=Barça+Basket+Camiseta",
                "destacado": True
            },
            {
                "id": "prod_008",
                "name": "Chaqueta Mercedes F1",
                "deporte": "formula1",
                "equipo": "Mercedes-AMG Petronas",
                "categoria": "Chaqueta",
                "precio": 120.00,
                "precio_personalizacion": 0,
                "permite_personalizacion": False,
                "stock": 25,
                "tallas": ["M", "L", "XL"],
                "imagen_url": "https://via.placeholder.com/400x400?text=Mercedes+Chaqueta",
                "destacado": True
            }
        ]

        return products[:limit]

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
        # Obtener todos los productos
        all_products = ProductService.get_featured_products(limit=100)

        # Filtrar por deporte
        filtered = [p for p in all_products if p["deporte"] == sport_id]

        # Filtrar por equipo si se especifica
        if team:
            filtered = [p for p in filtered if p["equipo"] == team]

        # Filtrar por categoría si se especifica
        if categoria:
            filtered = [p for p in filtered if p["categoria"] == categoria]

        return filtered[:limit]

    @staticmethod
    def get_product_by_id(product_id: str) -> Optional[Dict]:
        """
        Obtiene un producto por su ID.

        Args:
            product_id: ID del producto

        Returns:
            Optional[Dict]: Producto o None si no se encuentra
        """
        products = ProductService.get_featured_products(limit=100)
        for product in products:
            if product["id"] == product_id:
                return product
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
        all_products = ProductService.get_featured_products(limit=100)
        query_lower = query.lower()

        results = [
            p for p in all_products
            if query_lower in p["name"].lower()
            or query_lower in p["equipo"].lower()
            or query_lower in p["categoria"].lower()
        ]

        return results
