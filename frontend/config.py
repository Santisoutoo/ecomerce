"""
Configuración del frontend de Streamlit.
Define URLs del backend y configuraciones de la aplicación.
"""

import os
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

# URL del backend FastAPI
BACKEND_URL = os.getenv("BACKEND_URL", "http://localhost:8000")
API_V1_URL = f"{BACKEND_URL}/api/v1"

# Endpoints de autenticación
AUTH_ENDPOINTS = {
    "signup": f"{API_V1_URL}/auth/signup",
    "signin": f"{API_V1_URL}/auth/signin",
    "me": f"{API_V1_URL}/auth/me",
    "signout": f"{API_V1_URL}/auth/signout",
    "verify_token": f"{API_V1_URL}/auth/verify-token"
}

# Configuración de la aplicación
APP_NAME = "SportStyle Store"
APP_ICON = "🏪"
APP_DESCRIPTION = "E-commerce de merchandising deportivo"

# Configuración de sesión
SESSION_KEYS = {
    "authenticated": "authenticated",
    "access_token": "access_token",
    "user_id": "user_id",
    "user_email": "user_email",
    "es_admin": "es_admin",
    "current_page": "current_page",
    "show_welcome": "show_welcome"
}
