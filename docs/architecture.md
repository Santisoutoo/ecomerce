# 🏗️ Arquitectura del Proyecto SportStyle Store

## Descripción General

SportStyle Store es una plataforma de e-commerce multiplataforma especializada en merchandising oficial y personalizado de equipos deportivos. El sistema sigue una arquitectura de tres capas con sincronización en tiempo real entre plataforma web (Streamlit) y aplicación móvil (Thunkable), utilizando Firebase como backend unificado.

## Arquitectura de Tres Capas

### Capa 1: Presentación (Frontend)

**Plataforma Web - Streamlit**
- Interfaz responsive con diseño dark mode personalizado
- Navegación entre páginas: Home, Catálogo, Detalle, Carrito, Checkout, Cuenta
- Componentes reutilizables para mantener consistencia visual
- Sistema de sesión para mantener estado del usuario
- Actualización en tiempo real del carrito y stock

**Plataforma Móvil - Thunkable** (desarrollo futuro)
- Interfaz táctil optimizada para dispositivos móviles
- Navegación mediante bottom bar
- Sincronización automática con plataforma web
- Notificaciones push de ofertas y estado de pedidos

### Capa 2: Lógica de Negocio (Backend Services)

**Servicios Principales**
- **Autenticación**: Registro, login, gestión de sesiones
- **Productos**: Búsqueda, filtrado, gestión de catálogo
- **Carrito**: Agregar, actualizar, eliminar items con validación de stock en tiempo real
- **Pedidos**: Procesamiento, seguimiento, historial
- **Usuario**: Perfil, favoritos, sistema de puntos de fidelización
- **Pago**: Simulación de procesamiento de pago (académico)

**Validaciones Multinivel**
- Validaciones de frontend: Formatos, campos obligatorios
- Validaciones de backend: Stock en tiempo real, unicidad de datos
- Validaciones de negocio: Promociones, puntos, precios

### Capa 3: Persistencia de Datos (Firebase)

**Firebase Firestore**
- Base de datos NoSQL en tiempo real
- Colecciones: users, products, carts, orders
- Sincronización automática entre web y móvil
- Consultas indexadas para filtrado eficiente

**Firebase Authentication**
- Autenticación de usuarios con email/contraseña
- Gestión de tokens JWT
- Control de sesiones

**Firebase Storage** (opcional)
- Almacenamiento de imágenes de productos
- URLs públicas para acceso optimizado

## Estructura del Proyecto

```
sportstyle-store/
│
├── docs/                              # Documentación del proyecto
│   ├── architecture.md               # Este archivo
│   ├── firebase_structure.md         # Estructura de Firestore
│   └── features.md                   # Funcionalidades y especificaciones
│
├── frontend/                          # Aplicación Streamlit
│   ├── pages/                        # Páginas de la aplicación
│   ├── components/                   # Componentes UI reutilizables
│   ├── main.py                       # Punto de entrada
│   ├── styles.py                     # Estilos y CSS
│   └── requirements.txt              # Dependencias frontend
│
├── backend/                           # Lógica de negocio
│   ├── config/                       # Configuración Firebase
│   ├── models/                       # Modelos de datos (Pydantic)
│   ├── services/                     # Servicios de negocio
│   ├── utils/                        # Utilidades y constantes
│   └── requirements.txt              # Dependencias backend
│
└── data/                             # Datos iniciales y seeds
    ├── seed_products.json            # Productos iniciales
    └── spain_provinces.geojson       # Datos geográficos
```

## Flujo de Datos

### 1. Autenticación de Usuario
```
Usuario → Frontend (Login Form) → Auth Service → Firebase Auth → Session Token → Frontend State
```

### 2. Búsqueda y Filtrado de Productos
```
Usuario → Frontend (Filtros) → Product Service → Firestore Query → Frontend (Catálogo)
```

### 3. Agregar al Carrito (Con validación en tiempo real)
```
Usuario → Frontend → Cart Service → Validar Stock (Firestore) →
Si disponible → Reservar → Actualizar Carrito → Sincronizar (Web/Móvil)
Si no disponible → Error → Frontend (Mensaje)
```

### 4. Procesamiento de Pedido
```
Usuario → Checkout → Order Service → Validar Datos → Simular Pago →
Actualizar Stock → Crear Pedido → Asignar Puntos → Confirmación
```

## Sincronización en Tiempo Real

### Gestión de Stock
- Cuando un usuario agrega un producto al carrito, se RESERVA la cantidad
- La reserva se mantiene durante el proceso de checkout
- Si el usuario abandona el carrito, la reserva se libera después de X minutos
- Las actualizaciones de stock se propagan instantáneamente a todas las plataformas

### Carrito Compartido
- El carrito se sincroniza automáticamente entre web y móvil
- Utilizando listeners de Firestore en tiempo real
- Cualquier cambio se refleja inmediatamente en todos los dispositivos del usuario

### Favoritos
- Lista de favoritos sincronizada entre plataformas
- Actualizaciones instantáneas al agregar/eliminar

## Principios de Diseño

### Clean Code
- Código en inglés con comentarios y docstrings en español
- Nombres descriptivos y auto-explicativos
- Funciones pequeñas con responsabilidad única
- Máximo 20-30 líneas por función

### Principio de Unifuncionalidad
- Cada función realiza una única tarea
- Funciones complejas se componen de funciones más pequeñas
- Facilita testing y mantenimiento

### Modularidad
- Componentes reutilizables
- Separación de responsabilidades
- Bajo acoplamiento, alta cohesión

### Mantenibilidad
- Documentación clara en español
- Estructura de carpetas lógica
- Constantes centralizadas
- Configuración mediante variables de entorno

## Tecnologías Utilizadas

### Frontend
- **Streamlit**: Framework para aplicación web
- **Python**: Lenguaje de programación
- **Custom CSS**: Estilos personalizados

### Backend
- **Firebase Admin SDK**: Interacción con Firebase
- **Pydantic**: Validación de modelos de datos
- **Python-dotenv**: Gestión de variables de entorno

### Base de Datos
- **Firebase Firestore**: Base de datos NoSQL en tiempo real
- **Firebase Authentication**: Autenticación de usuarios
- **Firebase Storage**: Almacenamiento de archivos (opcional)

### Herramientas
- **Git**: Control de versiones
- **GeoJSON**: Datos geográficos de provincias españolas
- **Pillow**: Procesamiento de imágenes

## Seguridad

### Autenticación
- Contraseñas hasheadas (manejado por Firebase Auth)
- Tokens JWT para sesiones
- Expiración automática de sesiones

### Validación de Datos
- Validación en frontend y backend
- Modelos Pydantic para type safety
- Sanitización de inputs de usuario

### Variables de Entorno
- Credenciales en archivos .env (no versionados)
- Firebase credentials en archivo separado
- Ejemplo .env.example para desarrollo

## Escalabilidad

### Presente (Proyecto Académico)
- Soporta cientos de usuarios concurrentes
- Catálogo de ~50-100 productos
- Operaciones CRUD básicas

### Futuro (Posibles Mejoras)
- Implementación de caché con Redis
- CDN para imágenes estáticas
- Índices compuestos en Firestore
- Sistema de colas para pedidos
- Análisis de datos con dashboard admin
- Sistema de recomendaciones

## Consideraciones Académicas

### Simplificaciones
- **Pago**: Simulado, no procesamiento real
- **Envío**: Tarifa plana, sin integración con transportistas
- **Email**: Notificaciones solo en app, no emails reales
- **Imágenes**: URLs estáticas o almacenamiento local

### Aspectos Completos
- Autenticación funcional
- CRUD completo de todas las entidades
- Validación de stock en tiempo real
- Sistema de puntos funcional
- Filtros y búsqueda avanzada
- Sincronización multiplataforma

## Convenciones de Código

### Nomenclatura
- **Funciones**: snake_case (ej: `get_user_cart`)
- **Clases**: PascalCase (ej: `ProductService`)
- **Constantes**: UPPER_SNAKE_CASE (ej: `SHIPPING_COST`)
- **Variables**: snake_case (ej: `user_id`)

### Estructura de Funciones
```
def function_name(params):
    """
    Descripción breve de lo que hace la función.

    Args:
        param1: Descripción del parámetro

    Returns:
        Descripción del retorno
    """
    # Implementación
```

### Organización de Imports
1. Librerías estándar de Python
2. Librerías de terceros
3. Módulos locales del proyecto

## Testing (Opcional)

### Niveles de Testing
- **Unit Tests**: Funciones individuales
- **Integration Tests**: Servicios con Firebase
- **UI Tests**: Flujos completos de usuario (manual)

### Herramientas
- pytest para unit tests
- Firebase Emulator para testing local
