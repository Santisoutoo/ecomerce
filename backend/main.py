"""
Aplicación principal de FastAPI para SportStyle Store.
Configura rutas, middleware y CORS.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from config.settings import (
    PROJECT_NAME,
    VERSION,
    DESCRIPTION,
    API_V1_PREFIX,
    ALLOWED_ORIGINS
)
from api.v1.endpoints import auth
from config.firebase_config import initialize_firebase


# Inicializar Firebase al arrancar la aplicación
initialize_firebase()


# Crear aplicación FastAPI
app = FastAPI(
    title=PROJECT_NAME,
    version=VERSION,
    description=DESCRIPTION,
    docs_url="/docs",
    redoc_url="/redoc"
)


# Configurar CORS para permitir requests desde Streamlit
app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Registrar routers
app.include_router(auth.router, prefix=API_V1_PREFIX)


@app.get("/")
async def root():
    """
    Endpoint raíz de la API.

    Returns:
        dict: Mensaje de bienvenida y enlaces útiles
    """
    return {
        "message": "Welcome to SportStyle Store API",
        "version": VERSION,
        "docs": "/docs",
        "health": "/health"
    }


@app.get("/health")
async def health_check():
    """
    Endpoint de health check para verificar que la API está funcionando.

    Returns:
        dict: Estado de la API
    """
    return {
        "status": "healthy",
        "service": PROJECT_NAME,
        "version": VERSION
    }


# Para ejecutar con uvicorn
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True  # Hot reload en desarrollo
    )
