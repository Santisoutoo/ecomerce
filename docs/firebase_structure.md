# 🔥 Estructura de Firebase Firestore

## Visión General

La base de datos de SportStyle Store utiliza Firebase Firestore, una base de datos NoSQL orientada a documentos que permite sincronización en tiempo real entre la aplicación web y móvil.

## Colecciones Principales

### 1. `users` - Usuarios del Sistema

Almacena la información de todos los usuarios registrados en la plataforma.

```
users/
└── {user_id}                           # ID de usuario (Firebase Auth UID)
    ├── email: string                   # Email del usuario (único)
    ├── nombre: string                  # Nombre
    ├── apellidos: string               # Apellidos
    ├── telefono: string                # Teléfono de contacto
    ├── fecha_registro: timestamp       # Fecha de creación de cuenta
    ├── puntos_fidelizacion: number     # Puntos acumulados (default: 0)
    ├── es_admin: boolean               # Si es administrador (default: false)
    ├── activo: boolean                 # Cuenta activa (default: true)
    │
    ├── direccion_envio: map            # Dirección principal de envío
    │   ├── calle: string               # Calle y número
    │   ├── ciudad: string              # Ciudad
    │   ├── provincia: string           # Provincia
    │   └── codigo_postal: string       # Código postal (5 dígitos)
    │
    └── favoritos: array<string>        # Array de product_ids favoritos
```

**Índices necesarios:**
- `email` (único)
- `activo`

**Reglas de negocio:**
- El email debe ser único en todo el sistema
- Los puntos se calculan: 1€ gastado = 10 puntos
- 100 puntos = 1€ de descuento
- Solo puede haber una dirección de envío (simplificado)

---

### 2. `products` - Catálogo de Productos

Contiene todos los productos disponibles en el catálogo.

```
products/
└── {product_id}                        # ID auto-generado por Firestore
    ├── nombre: string                  # Nombre del producto
    ├── descripcion: string             # Descripción detallada
    ├── deporte: string                 # "futbol", "baloncesto", "formula1"
    ├── equipo: string                  # Nombre del equipo
    ├── categoria: string               # "camiseta", "sudadera", "gorra", etc.
    ├── precio: number                  # Precio base en euros
    ├── stock: number                   # Unidades disponibles
    ├── stock_reservado: number         # Unidades en carritos (TIEMPO REAL)
    ├── tallas: array<string>           # ["S", "M", "L", "XL", "XXL"]
    ├── permite_personalizacion: bool   # Si permite nombre/número
    ├── precio_personalizacion: number  # Coste adicional personalización
    ├── imagen_url: string              # URL de imagen principal
    ├── imagenes_galeria: array<string> # URLs de imágenes adicionales
    ├── activo: boolean                 # Producto visible (default: true)
    ├── destacado: boolean              # Aparece en home (default: false)
    └── fecha_creacion: timestamp       # Cuándo se creó
```

**Índices necesarios:**
- `deporte`
- `equipo`
- `categoria`
- `activo`
- `destacado`
- Índice compuesto: `deporte + activo`
- Índice compuesto: `categoria + activo`

**Reglas de negocio:**
- `stock_disponible_real = stock - stock_reservado`
- Las reservas se liberan automáticamente después de 30 minutos sin checkout
- Solo productos con `activo: true` son visibles en el catálogo

---

### 3. `carts` - Carritos de Compra

Un documento por usuario que contiene su carrito activo.

```
carts/
└── {user_id}                           # Un carrito por usuario
    ├── ultima_actualizacion: timestamp # Última modificación del carrito
    │
    └── items: array<map>               # Array de productos en el carrito
        └── [
            {
                product_id: string,              # ID del producto
                cantidad: number,                # Cantidad seleccionada
                talla: string,                   # Talla elegida
                personalizacion: {               # Opcional
                    nombre: string,              # Nombre a personalizar
                    numero: number               # Número a personalizar
                },
                precio_unitario: number,         # Precio en el momento de agregar
                precio_personalizacion: number,  # Coste personalización
                fecha_agregado: timestamp,       # Cuándo se agregó al carrito
                reserva_expira: timestamp        # Cuándo expira la reserva
            }
        ]
```

**Índices necesarios:**
- `ultima_actualizacion` (para limpieza de carritos abandonados)

**Reglas de negocio:**
- Al agregar un producto, se incrementa `stock_reservado` en `products`
- Las reservas expiran después de 30 minutos
- Un proceso periódico limpia reservas expiradas
- El precio se guarda en el momento de agregar (por si cambia después)

---

### 4. `orders` - Pedidos Realizados

Almacena todos los pedidos confirmados del sistema.

```
orders/
└── {order_id}                          # ID auto-generado
    ├── numero_pedido: string           # Formato: ORD-YYYYMMDD-NNNN
    ├── user_id: string                 # ID del usuario que compró
    ├── fecha_pedido: timestamp         # Cuándo se realizó
    ├── estado: string                  # "pendiente", "confirmado", "enviado", "entregado"
    │
    ├── items: array<map>               # Snapshot de productos comprados
    │   └── [
    │       {
    │           product_id: string,
    │           nombre_producto: string,        # Snapshot del nombre
    │           cantidad: number,
    │           talla: string,
    │           personalizacion: {
    │               nombre: string,
    │               numero: number
    │           },
    │           precio_unitario: number,
    │           precio_personalizacion: number,
    │           subtotal_linea: number          # cantidad * (precio_unitario + personalización)
    │       }
    │   ]
    │
    ├── subtotal: number                # Suma de todos los items
    ├── gastos_envio: number            # Coste de envío (tarifa plana 5€)
    ├── descuento_puntos: number        # Descuento aplicado con puntos
    ├── total: number                   # subtotal + gastos_envio - descuento_puntos
    ├── puntos_ganados: number          # Puntos que se acreditaron
    │
    ├── direccion_envio: map            # Snapshot de dirección (por si cambia después)
    │   ├── calle: string
    │   ├── ciudad: string
    │   ├── provincia: string
    │   └── codigo_postal: string
    │
    ├── metodo_pago: string             # "tarjeta", "transferencia" (SIMULADO)
    └── numero_seguimiento: string      # Número de seguimiento (generado fake)
```

**Índices necesarios:**
- `user_id` (para historial de pedidos del usuario)
- `estado` (para filtrar pedidos por estado)
- `fecha_pedido` (ordenación)
- Índice compuesto: `user_id + fecha_pedido DESC`

**Reglas de negocio:**
- Al confirmar un pedido, se decrementa `stock` y `stock_reservado` en `products`
- Se acreditan puntos al usuario según el total: `total * 10`
- Se guarda un snapshot de los productos por si se borran después
- El `numero_pedido` es único y secuencial por día

---

## Colecciones Auxiliares (Opcional - Futuro)

### 5. `promotions` - Promociones Activas

```
promotions/
└── {promotion_id}
    ├── codigo: string                  # Código promocional
    ├── descuento_porcentaje: number    # Porcentaje de descuento
    ├── descuento_fijo: number          # Descuento fijo en euros
    ├── fecha_inicio: timestamp
    ├── fecha_fin: timestamp
    ├── activo: boolean
    └── usos_maximos: number
```

### 6. `reviews` - Reseñas de Productos

```
reviews/
└── {review_id}
    ├── product_id: string
    ├── user_id: string
    ├── puntuacion: number              # 1-5 estrellas
    ├── comentario: string
    ├── fecha: timestamp
    └── verificado: boolean             # Si compró el producto
```

---

## Reglas de Seguridad de Firestore

### Usuarios
- Los usuarios solo pueden leer/escribir sus propios datos
- Los administradores pueden leer todos los usuarios
- Solo administradores pueden modificar `puntos_fidelizacion` y `es_admin`

### Productos
- Todos pueden leer productos activos
- Solo administradores pueden crear/modificar/eliminar productos
- La modificación de `stock` solo por servicios backend con validación

### Carritos
- Los usuarios solo pueden acceder a su propio carrito
- Las operaciones de stock_reservado se hacen mediante Cloud Functions

### Pedidos
- Los usuarios solo pueden leer sus propios pedidos
- Solo pueden crear pedidos (no modificar ni eliminar)
- Los administradores pueden leer y modificar todos los pedidos

---

## Estrategia de Sincronización en Tiempo Real

### Stock en Tiempo Real

**Problema:** Dos usuarios intentan comprar el último producto simultáneamente.

**Solución:**
1. Usar transacciones de Firestore para operaciones de stock
2. Al agregar al carrito, incrementar atómicamente `stock_reservado`
3. Validar que `stock - stock_reservado >= cantidad_solicitada`
4. Si falla, devolver error de stock insuficiente

### Listeners de Cambios

**Web (Streamlit):**
- Listener en el carrito del usuario para actualizaciones en tiempo real
- Listener en productos del catálogo para reflejar cambios de stock

**Móvil (Thunkable):**
- Polling periódico cada 5 segundos al carrito
- Refresco manual del catálogo con pull-to-refresh

### Limpieza de Reservas Expiradas

**Cloud Function programada (cada 10 minutos):**
1. Buscar items en carritos con `reserva_expira < now()`
2. Eliminar esos items
3. Decrementar `stock_reservado` en los productos correspondientes

---

## Modelo de Datos Geográficos

### GeoJSON - Provincias de España

Utilizado para:
- Validar códigos postales
- Calcular costes de envío por zona (opcional)
- Mostrar mapa de cobertura
- Estadísticas de ventas por provincia

**Estructura esperada en `data/spain_provinces.geojson`:**
```json
{
  "type": "FeatureCollection",
  "features": [
    {
      "type": "Feature",
      "properties": {
        "name": "Madrid",
        "code": "28",
        "postal_codes": ["28001", "28002", "..."]
      },
      "geometry": {
        "type": "Polygon",
        "coordinates": [...]
      }
    }
  ]
}
```

---

## Consultas Comunes

### Obtener productos de un deporte con stock disponible
```
products
  .where('deporte', '==', 'futbol')
  .where('activo', '==', true)
  .where('stock', '>', 0)
```

### Historial de pedidos de un usuario (más recientes primero)
```
orders
  .where('user_id', '==', user_id)
  .orderBy('fecha_pedido', 'desc')
  .limit(10)
```

### Productos más vendidos (requiere contador)
```
products
  .where('activo', '==', true)
  .orderBy('ventas_totales', 'desc')
  .limit(10)
```

---

## Estimación de Costes Firebase (Proyecto Académico)

**Plan Spark (Gratuito):**
- 1 GB almacenamiento
- 10 GB transferencia/mes
- 50,000 lecturas/día
- 20,000 escrituras/día

**Proyección para 100 usuarios activos/día:**
- Lecturas: ~5,000/día (bien dentro del límite)
- Escrituras: ~1,000/día (bien dentro del límite)
- Almacenamiento: ~50 MB (imágenes externas)

✅ El plan gratuito es suficiente para el proyecto académico

---

## Backup y Restauración

### Exportación de Datos
Firebase permite exportar colecciones completas en formato JSON para backup.

### Importación de Datos Iniciales
El archivo `data/seed_products.json` se importa mediante script de inicialización.

### Versionado
Los cambios en la estructura de datos deben documentarse en este archivo con la fecha de cambio.
