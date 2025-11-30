"""
Configuración general de la aplicación SportStyle Store.
Gestiona variables de entorno y configuraciones del backend.
"""

import os
from dotenv import load_dotenv
from pathlib import Path

# Cargar variables de entorno
load_dotenv()

# Rutas del proyecto
BASE_DIR = Path(__file__).resolve().parent.parent.parent
FIREBASE_CREDENTIALS_PATH = BASE_DIR / "firebase-credentials.json"

# Configuración de la API
API_V1_PREFIX = "/api/v1"
PROJECT_NAME = "SportStyle Store API"
VERSION = "1.0.0"
DESCRIPTION = "API REST para e-commerce de merchandising deportivo"

# Configuración de CORS
ALLOWED_ORIGINS = [
    "http://localhost:8501",  # Streamlit default
    "http://localhost:8000",  # FastAPI default
    "http://127.0.0.1:8501",
    "http://127.0.0.1:8000",
]

# Configuración de JWT
SECRET_KEY = os.getenv("SECRET_KEY", "your-secret-key-change-this-in-production")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24  # 24 horas

# Configuración de Firebase
FIREBASE_PROJECT_ID = os.getenv("FIREBASE_PROJECT_ID")
FIREBASE_WEB_API_KEY = os.getenv("FIREBASE_WEB_API_KEY")  # Para REST API de Firebase Auth

# Reglas de negocio
SHIPPING_COST = float(os.getenv("SHIPPING_COST", "5.0"))
POINTS_PER_EURO = int(os.getenv("POINTS_PER_EURO", "10"))
POINTS_TO_EURO_RATIO = int(os.getenv("POINTS_TO_EURO_RATIO", "100"))
CART_RESERVATION_MINUTES = int(os.getenv("CART_RESERVATION_MINUTES", "30"))

# Configuración de desarrollo
DEBUG = os.getenv("DEBUG", "True") == "True"
