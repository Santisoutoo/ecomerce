# ⚡ Funcionalidades SportStyle Store

## Descripción del Negocio

SportStyle Store es una plataforma de e-commerce especializada en merchandising oficial y personalizado de equipos deportivos españoles e internacionales.

**Propuesta de Valor:**
- Catálogo unificado de múltiples deportes en una sola plataforma
- Personalización avanzada de productos con nombre y número
- Experiencia multiplataforma sincronizada (Web + Móvil)
- Sistema de fidelización con puntos acumulables

**Público Objetivo:**
- Aficionados al deporte entre 15 y 45 años
- Residentes en España
- Familiarizados con compras online

---

## Deportes y Equipos Disponibles

### ⚽ Fútbol Español

**Competiciones:**
- LaLiga Santander
- Selección Española

**Equipos:**
- Real Madrid CF
- FC Barcelona
- Atlético de Madrid
- Sevilla FC
- Valencia CF
- Real Betis Balompié
- Athletic Club Bilbao
- Real Sociedad
- Villarreal CF
- Selección Española de Fútbol

**Productos disponibles:**
- Camisetas (1ª, 2ª y 3ª equipación)
- Sudaderas
- Chaquetas de entrenamiento
- Gorras
- Bufandas
- Pantalones cortos

---

### 🏀 Baloncesto Español (ACB)

**Competición:**
- Liga Endesa ACB

**Equipos:**
- Real Madrid Baloncesto
- FC Barcelona Basket
- Valencia Basket
- Saski Baskonia
- Unicaja Málaga
- Joventut Badalona
- Cazoo Baskonia
- UCAM Murcia

**Productos disponibles:**
- Camisetas reversibles
- Sudaderas con capucha
- Camisetas de calentamiento
- Gorras snapback
- Mochilas
- Balones de entrenamiento

---

### 🏎️ Fórmula 1

**Temporada:** 2025

**Equipos:**
- Scuderia Ferrari
- Red Bull Racing
- Mercedes-AMG Petronas
- McLaren Racing
- Aston Martin F1 Team
- Alpine F1 Team
- Williams Racing
- Alfa Romeo F1 Team
- Haas F1 Team
- Scuderia AlphaTauri

**Productos disponibles:**
- Camisetas del equipo
- Gorras oficiales de pilotos
- Sudaderas con capucha
- Chaquetas softshell
- Réplicas de cascos (escala)
- Llaveros y accesorios

---

## Categorías de Productos

### Ropa

1. **Camisetas**
   - Camisetas oficiales de juego
   - Camisetas de entrenamiento
   - Camisetas casual
   - Tallas: XS, S, M, L, XL, XXL
   - Permite personalización: SÍ
   - Precio personalización: 10€

2. **Sudaderas**
   - Con capucha
   - Sin capucha
   - Con cremallera
   - Tallas: S, M, L, XL, XXL
   - Permite personalización: SÍ
   - Precio personalización: 12€

3. **Chaquetas**
   - Chaquetas de entrenamiento
   - Chaquetas técnicas
   - Chaquetas bomber
   - Tallas: S, M, L, XL, XXL
   - Permite personalización: NO

4. **Pantalones**
   - Pantalones cortos
   - Pantalones de entrenamiento
   - Tallas: S, M, L, XL, XXL
   - Permite personalización: NO

### Accesorios

5. **Gorras**
   - Gorras de béisbol
   - Gorras snapback
   - Tallas: Única ajustable
   - Permite personalización: NO

6. **Bufandas**
   - Bufandas de aficionado
   - Bufandas tejidas
   - Talla: Única
   - Permite personalización: NO

7. **Otros Accesorios**
   - Mochilas
   - Llaveros
   - Imanes
   - Pegatinas
   - Talla: Única
   - Permite personalización: NO

---

## Funcionalidades de la Plataforma Web

### 1. Sistema de Autenticación

**Registro de Usuario**
- Formulario con: email, contraseña, nombre, apellidos, teléfono
- Validación de email único
- Contraseña mínimo 6 caracteres
- Confirmación de contraseña
- Registro automático con Firebase Auth
- Asignación de 0 puntos iniciales

**Inicio de Sesión**
- Login con email y contraseña
- Mensaje de error si credenciales incorrectas
- Mantener sesión activa
- Botón de cerrar sesión

**Gestión de Sesión**
- Estado de sesión persistente en Streamlit
- Token JWT de Firebase
- Redirección a login si no autenticado

---

### 2. Página de Inicio (Home)

**Elementos:**
- Banner principal con logo SportStyle
- Sección de productos destacados (6-8 productos)
- Productos organizados por deporte
- Llamadas a acción para explorar catálogo
- Acceso rápido a ofertas

**Navegación:**
- Menú superior con categorías por deporte
- Barra de búsqueda permanente
- Icono de carrito con contador de items
- Icono de usuario (perfil/logout)

---

### 3. Catálogo de Productos

**Sistema de Filtros**
- Por deporte: Fútbol, Baloncesto, Fórmula 1
- Por equipo: Listado dinámico según deporte seleccionado
- Por categoría: Camiseta, Sudadera, Gorra, etc.
- Por talla: S, M, L, XL, XXL
- Por rango de precio: 0-50€, 50-100€, +100€
- Por disponibilidad: Solo con stock

**Búsqueda Inteligente**
- Búsqueda por nombre de producto
- Búsqueda por equipo
- Búsqueda por jugador (en personalización)
- Sugerencias automáticas

**Visualización**
- Grid de productos (3-4 columnas)
- Cada tarjeta muestra:
  - Imagen del producto
  - Nombre
  - Equipo
  - Precio
  - Indicador de stock (disponible/últimas unidades/agotado)
  - Icono de favorito
  - Botón "Ver detalles"

**Ordenación**
- Por relevancia
- Precio: menor a mayor
- Precio: mayor a menor
- Más recientes
- Más populares

---

### 4. Detalle de Producto

**Información Mostrada**
- Galería de imágenes (2-4 imágenes)
- Nombre completo del producto
- Descripción detallada
- Precio base
- Indicador de stock en tiempo real
- Selector de talla con disponibilidad por talla
- Opción de personalización (si aplica)

**Personalización**
- Campo de texto: Nombre (máx 15 caracteres)
- Campo numérico: Número (0-99)
- Preview visual de cómo quedará
- Coste adicional mostrado claramente
- Validación de caracteres especiales

**Acciones**
- Selector de cantidad (según stock disponible)
- Botón "Agregar al carrito"
- Botón "Agregar a favoritos"
- Compartir en redes sociales (opcional)

---

### 5. Carrito de Compras

**Visualización**
- Lista de productos agregados
- Para cada producto:
  - Imagen miniatura
  - Nombre y personalización (si aplica)
  - Talla
  - Precio unitario
  - Cantidad (editable con +/-)
  - Subtotal de línea
  - Botón eliminar

**Cálculos**
- Subtotal de todos los productos
- Gastos de envío: 5€ (tarifa plana)
- Descuento por puntos (si se aplica)
- Total final

**Sistema de Puntos**
- Mostrar puntos disponibles del usuario
- Opción de canjear puntos: 100 puntos = 1€ descuento
- Selector de cuántos puntos usar
- Actualización dinámica del total

**Validaciones en Tiempo Real**
- Verificar stock disponible al cargar carrito
- Mensaje si un producto ya no tiene stock
- Opción de eliminar productos sin stock
- Advertencia de reserva temporal (30 min)

**Acciones**
- Vaciar carrito completo
- Continuar comprando (volver al catálogo)
- Proceder al checkout

---

### 6. Proceso de Checkout

**Paso 1: Revisión del Pedido**
- Resumen de productos a comprar
- Totales calculados
- No editable (volver al carrito para cambios)

**Paso 2: Dirección de Envío**
- Formulario con:
  - Calle y número
  - Ciudad
  - Provincia (selector de provincias españolas)
  - Código postal (validación formato 5 dígitos)
- Opción de guardar como dirección predeterminada
- Si ya tiene dirección guardada, pre-rellenar

**Paso 3: Método de Pago (SIMULADO)**
- Opciones:
  - Tarjeta de crédito/débito (fake form)
  - Transferencia bancaria (fake)
- Formulario de tarjeta simulado:
  - Número de tarjeta (16 dígitos fake)
  - Fecha expiración
  - CVV
  - Nombre del titular
- **IMPORTANTE:** No se procesa pago real, solo simulación

**Paso 4: Confirmación**
- Resumen completo del pedido
- Dirección de envío
- Método de pago seleccionado
- Total a pagar
- Puntos que se ganarán con esta compra
- Botón "Confirmar Pedido"

**Procesamiento**
- Validación final de stock
- Creación del pedido en Firebase
- Reducción de stock en productos
- Vaciado del carrito
- Asignación de puntos al usuario
- Generación de número de pedido
- Pantalla de confirmación con número de pedido

---

### 7. Cuenta de Usuario

**Mi Perfil**
- Información personal (editable)
- Email (no editable)
- Teléfono
- Dirección de envío guardada
- Opción de cambiar contraseña

**Historial de Pedidos**
- Lista de todos los pedidos realizados
- Para cada pedido:
  - Número de pedido
  - Fecha
  - Estado (pendiente, confirmado, enviado, entregado)
  - Total pagado
  - Botón "Ver detalles"

**Detalle de Pedido**
- Productos comprados
- Dirección de envío
- Método de pago
- Número de seguimiento (fake)
- Opción de descargar factura (PDF fake - opcional)

**Mis Favoritos**
- Grid de productos favoritos
- Acceso rápido a cada producto
- Botón para quitar de favoritos
- Botón "Agregar al carrito" directo

**Mis Puntos de Fidelización**
- Total de puntos acumulados
- Historial de puntos:
  - Puntos ganados por pedido
  - Puntos canjeados
  - Fecha de transacción
- Equivalencia en euros
- Instrucciones de cómo canjear

---

## Funcionalidades de la Plataforma Móvil (Thunkable)

### Diferencias con la Web

**Navegación**
- Bottom navigation bar con 5 secciones:
  - Home
  - Catálogo
  - Carrito
  - Favoritos
  - Perfil

**Interacciones Táctiles**
- Swipe para galería de imágenes
- Pull-to-refresh en catálogo
- Gestos para eliminar items del carrito
- Notificaciones push (opcional)

**Sincronización**
- Carrito sincronizado en tiempo real con web
- Favoritos sincronizados
- Puntos actualizados
- Historial de pedidos compartido

---

## Sistema de Puntos de Fidelización

### Acumulación de Puntos
- Por cada 1€ gastado → 10 puntos
- Los puntos se acreditan al confirmar el pedido
- No se dan puntos por gastos de envío
- No se dan puntos por descuentos con puntos

### Canje de Puntos
- 100 puntos = 1€ de descuento
- Se pueden canjear en múltiplos de 100
- Máximo canjeable: 50% del subtotal del pedido
- Los puntos se descuentan al confirmar el pedido

### Ejemplos
- Pedido de 50€ → Ganas 500 puntos
- Tienes 1000 puntos → Puedes canjear hasta 10€
- Pedido de 30€ con 500 puntos → Pagas 25€ (30€ - 5€)

---

## Validaciones del Sistema

### Validaciones de Frontend
- Formato de email válido
- Contraseña mínimo 6 caracteres
- Teléfono formato español (9 dígitos)
- Código postal 5 dígitos numéricos
- Campos obligatorios no vacíos
- Cantidad máxima según stock

### Validaciones de Backend
- Email único en el sistema
- Stock suficiente al agregar al carrito
- Stock suficiente al confirmar pedido
- Puntos suficientes para canjear
- Talla válida para el producto
- Producto activo y disponible

### Validaciones de Negocio
- No permitir cantidades negativas
- No permitir personalización en productos que no la permiten
- Máximo 10 unidades por producto en un pedido
- No permitir checkout con carrito vacío
- Validar que la suma de puntos no exceda el máximo

---

## Datos de Ejemplo (Seed)

### Usuarios de Prueba
- **Admin:** admin@sportstyle.com / Admin123
- **Usuario 1:** victor@test.com / Test123 (1000 puntos)
- **Usuario 2:** luis@test.com / Test123 (500 puntos)

### Productos Iniciales (Mínimo 30-50)

**Ejemplos:**

1. **Camiseta Real Madrid 1ª Equipación 2024/25**
   - Deporte: Fútbol
   - Equipo: Real Madrid CF
   - Categoría: Camiseta
   - Precio: 89.99€
   - Stock: 50
   - Tallas: S, M, L, XL, XXL
   - Personalización: Sí (10€)

2. **Sudadera FC Barcelona**
   - Deporte: Fútbol
   - Equipo: FC Barcelona
   - Categoría: Sudadera
   - Precio: 65.00€
   - Stock: 30
   - Tallas: M, L, XL
   - Personalización: Sí (12€)

3. **Gorra Ferrari F1 2025**
   - Deporte: Fórmula 1
   - Equipo: Scuderia Ferrari
   - Categoría: Gorra
   - Precio: 35.00€
   - Stock: 100
   - Talla: Única
   - Personalización: No

---

## Reglas de Negocio

### Precios
- Todos los precios incluyen IVA (21%)
- Los precios pueden cambiar sin afectar pedidos ya realizados
- La personalización tiene coste adicional fijo

### Envíos
- Tarifa plana de 5€ para toda España
- Envío gratuito en pedidos superiores a 100€ (opcional)
- Tiempo estimado: 3-5 días laborables

### Devoluciones (Información Simulada)
- 30 días para devolución
- Productos personalizados no admiten devolución
- Gastos de envío de devolución a cargo del cliente

### Stock
- Reserva temporal de 30 minutos al agregar al carrito
- Si no se completa el checkout, se libera el stock
- Los productos agotados no aparecen en búsquedas (opcional)

### Promociones (Futuras)
- Códigos de descuento porcentual
- Códigos de descuento fijo
- Ofertas por temporada
- Descuentos por equipo

---

## Métricas y KPIs (Dashboard Admin - Opcional)

### Ventas
- Total vendido hoy/semana/mes
- Número de pedidos
- Ticket promedio
- Productos más vendidos

### Usuarios
- Usuarios registrados
- Usuarios activos
- Puntos totales en circulación

### Productos
- Stock bajo (< 10 unidades)
- Productos más vistos
- Tasa de conversión por producto

### Geográfico
- Ventas por provincia (usando GeoJSON)
- Mapa de calor de pedidos

---

## Roadmap Futuro (Fuera del Alcance Actual)

### Fase 2
- Sistema de reseñas y valoraciones
- Wishlist compartida
- Códigos promocionales
- Programa de referidos

### Fase 3
- Integración con pasarelas de pago reales (Stripe, PayPal)
- Integración con servicios de envío (Correos, SEUR)
- Email marketing automatizado
- Notificaciones por email

### Fase 4
- Recomendaciones personalizadas con ML
- Chat de soporte en vivo
- App nativa iOS/Android
- Internacionalización (múltiples idiomas)
