#!/bin/bash
# Script para iniciar el backend de SportStyle Store
# Ejecutar desde la raíz del proyecto: ./start_backend.sh

echo "=========================================="
echo "   SportStyle Store - Backend API"
echo "=========================================="
echo ""
echo "Iniciando servidor FastAPI..."
echo ""

# Asegurarse de estar en el directorio correcto
cd "$(dirname "$0")"

# Activar entorno virtual si existe
if [ -d ".venv" ]; then
    echo "Activando entorno virtual..."
    source .venv/bin/activate
elif [ -d "venv" ]; then
    echo "Activando entorno virtual..."
    source venv/bin/activate
fi

# Iniciar uvicorn desde la raíz del proyecto
echo "Ejecutando: python3 -m uvicorn backend.main:app --host 0.0.0.0 --port 8000 --reload"
echo ""
echo "El backend estará disponible en:"
echo "  - API: http://localhost:8000"
echo "  - Docs: http://localhost:8000/docs"
echo "  - ReDoc: http://localhost:8000/redoc"
echo ""
echo "Presiona Ctrl+C para detener el servidor"
echo "=========================================="
echo ""

python3 -m uvicorn backend.main:app --host 0.0.0.0 --port 8000 --reload
