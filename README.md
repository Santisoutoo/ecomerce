# 🏪 SportStyle Store

Plataforma de e-commerce multiplataforma especializada en merchandising oficial y personalizado de equipos deportivos.

**Proyecto académico - Grupo 11**
- Bernardo Quindimil Micó
- Víctor Vega Sobral
- Santiago Souto Ortega
- Luis Sánchez Patiño

## 📋 Descripción

SportStyle Store es una aplicación web desarrollada con Streamlit y Firebase que permite a los usuarios comprar merchandising oficial de:
- ⚽ Fútbol Español (LaLiga + Selección)
- 🏀 Baloncesto ACB
- 🏎️ Fórmula 1

### Características Principales
- Catálogo de productos con filtros avanzados
- Personalización de productos (nombre + número)
- Carrito de compras sincronizado
- Sistema de puntos de fidelización
- Gestión de pedidos
- Sincronización en tiempo real entre web y móvil (Thunkable)

## 🏗️ Arquitectura

El proyecto sigue una arquitectura de **tres capas**:

1. **Capa de Presentación** (Frontend - Streamlit)
2. **Capa de Negocio** (Backend - Services)
3. **Capa de Datos** (Firebase Firestore + Auth)

Ver documentación completa en [`docs/architecture.md`](docs/architecture.md)

## 📁 Estructura del Proyecto

```
sportstyle-store/
│
├── docs/                       # Documentación
│   ├── architecture.md        # Arquitectura del sistema
│   ├── firebase_structure.md  # Estructura de Firestore
│   └── features.md            # Funcionalidades detalladas
│
├── frontend/                   # Aplicación Streamlit
│   ├── pages/                 # Páginas de la app
│   ├── components/            # Componentes reutilizables
│   ├── assets/                # Recursos estáticos
│   ├── main.py               # Punto de entrada
│   ├── styles.py             # Estilos CSS
│   └── requirements.txt      # Dependencias frontend
│
├── backend/                    # Lógica de negocio
│   ├── config/                # Configuración Firebase
│   ├── models/                # Modelos de datos
│   ├── services/              # Servicios de negocio
│   ├── utils/                 # Utilidades
│   └── requirements.txt       # Dependencias backend
│
├── data/                       # Datos iniciales
│   ├── seed_products.json     # Productos de prueba
│   └── spain_provinces.geojson # Datos geográficos
│
├── .env.example               # Ejemplo de variables de entorno
├── .gitignore                 # Archivos ignorados por Git
└── README.md                  # Este archivo
```

## 🚀 Instalación y Configuración

### Prerrequisitos
- Python 3.9 o superior
- Cuenta de Firebase (proyecto configurado)
- Git

### Paso 1: Clonar el repositorio

```bash
git clone https://github.com/tu-usuario/sportstyle-store.git
cd sportstyle-store
```

### Paso 2: Configurar entorno virtual

```bash
# Crear entorno virtual
python -m venv venv

# Activar entorno virtual
# En Windows:
venv\Scripts\activate
# En macOS/Linux:
source venv/bin/activate
```

### Paso 3: Instalar dependencias

```bash
# Instalar dependencias del backend
pip install -r backend/requirements.txt

# Instalar dependencias del frontend
pip install -r frontend/requirements.txt
```

### Paso 4: Configurar Firebase

1. Crear un proyecto en [Firebase Console](https://console.firebase.google.com/)
2. Habilitar Firestore Database
3. Habilitar Authentication (Email/Password)
4. Descargar credenciales de servicio (archivo JSON)
5. Guardar el archivo como `firebase-credentials.json` en la raíz del proyecto

### Paso 5: Configurar variables de entorno

```bash
# Copiar archivo de ejemplo
cp .env.example .env

# Editar .env con tus credenciales de Firebase
# O puedes usar directamente el archivo firebase-credentials.json
```

### Paso 6: Inicializar base de datos (opcional)

```bash
# Ejecutar script de seed para poblar productos iniciales
python backend/migrations/seed_products.py
```

## 🎮 Uso

### Ejecutar la aplicación web

```bash
# Desde la raíz del proyecto
streamlit run frontend/main.py
```

La aplicación se abrirá automáticamente en tu navegador en `http://localhost:8501`

### Usuarios de Prueba

Después de ejecutar el seed, puedes usar:

- **Admin:** admin@sportstyle.com / Admin123
- **Usuario:** test@sportstyle.com / Test123

## 🛠️ Tecnologías Utilizadas

### Frontend
- **Streamlit** - Framework web en Python
- **Folium** - Mapas interactivos
- **Pillow** - Procesamiento de imágenes

### Backend
- **Firebase Firestore** - Base de datos NoSQL
- **Firebase Authentication** - Autenticación de usuarios
- **Pydantic** - Validación de datos
- **Python-dotenv** - Gestión de variables de entorno

## 📚 Documentación Adicional

- [Arquitectura del Sistema](docs/architecture.md)
- [Estructura de Firebase](docs/firebase_structure.md)
- [Funcionalidades Completas](docs/features.md)

## 🧪 Testing

```bash
# Ejecutar tests (cuando estén implementados)
pytest tests/
```

## 📝 Convenciones de Código

- **Código:** Inglés
- **Comentarios y docstrings:** Español
- **Nomenclatura:**
  - Funciones: `snake_case`
  - Clases: `PascalCase`
  - Constantes: `UPPER_SNAKE_CASE`
- **Principio de unifuncionalidad:** Una función = una tarea

## 📄 Licencia

Este proyecto es para fines educativos. Desarrollado para la asignatura de Desarrollo Web y App Móviles - Cuarto Año.

---

**Nota:** Este proyecto utiliza simulaciones para procesamiento de pagos y envíos. No es un sistema de producción real.
