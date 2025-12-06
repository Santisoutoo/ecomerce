#!/bin/bash
# Script para iniciar el frontend de SportStyle Store
# Ejecutar desde la raíz del proyecto: ./start_frontend.sh

echo "=========================================="
echo "   SportStyle Store - Frontend Web"
echo "=========================================="
echo ""
echo "Iniciando aplicación Streamlit..."
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

# Cambiar al directorio frontend y ejecutar
cd frontend

echo "Ejecutando: streamlit run main.py"
echo ""
echo "El frontend estará disponible en:"
echo "  - URL: http://localhost:8501"
echo ""
echo "Presiona Ctrl+C para detener el servidor"
echo "=========================================="
echo ""

streamlit run main.py
