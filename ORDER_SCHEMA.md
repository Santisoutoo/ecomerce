# Esquema de Pedidos (Orders)

Este documento describe la estructura de pedidos en Firebase Realtime Database después de los ajustes realizados.

## Estructura en Firebase

Los pedidos se almacenan en `/orders/{order_id}` con la siguiente estructura:

```
/orders/
  ├── ORD-20251205-8672/
  │   ├── order_id: "ORD-20251205-8672"
  │   ├── user_id: "fZlBToT35rPVcuUg3SO1oTuXwM22"
  │   ├── user_email: "hola@gmail.com"
  │   ├── items: [
  │   │   {
  │   │     "product_id": "prod_001",
  │   │     "product_name": "Camiseta FC Barcelona",
  │   │     "product_image": "https://res.cloudinary.com/...",
  │   │     "team": "Barcelona",
  │   │     "quantity": 2,
  │   │     "size": "L",
  │   │     "unit_price": 89.99,
  │   │     "personalization_price": 10.00,
  │   │     "personalization": {
  │   │       "nombre": "MESSI",
  │   │       "numero": 10
  │   │     },
  │   │     "subtotal": 199.98
  │   │   }
  │   │ ]
  │   ├── subtotal: 199.98
  │   ├── shipping_cost: 5.00
  │   ├── tax: 43.05
  │   ├── total: 248.03
  │   ├── status: "pending"
  │   ├── shipping_address: {
  │   │   "street": "Calle Ejemplo 123",
  │   │   "city": "Madrid",
  │   │   "state": "Madrid",
  │   │   "postal_code": "28001",
  │   │   "country": "España"
  │   │ }
  │   ├── payment_method: "credit_card"
  │   ├── created_at: "2025-12-05T10:30:00"
  │   └── updated_at: "2025-12-05T10:30:00"
```

## Cambios Realizados

### 1. **Modelo OrderItem** ([models.py:380-391](backend/models/models.py#L380-L391))

Se añadieron los siguientes campos:

- `product_image`: URL de la imagen del producto
- `team`: Equipo del producto
- `personalization_price`: Precio de personalización (€10.00 por defecto)
- `personalization`: Objeto opcional con:
  - `nombre`: Nombre a personalizar (máx 15 caracteres)
  - `numero`: Número a personalizar (0-99)

### 2. **Modelo Order** ([models.py:403-417](backend/models/models.py#L403-L417))

Se modificaron los campos:

- `order_id`: ID único del pedido con formato `ORD-YYYYMMDD-XXXX` (antes `id`)
- `user_id`: ID del usuario en Firebase Auth
- `user_email`: **NUEVO** - Email del usuario como identificador adicional

### 3. **Servicio OrderService** ([order_service.py](backend/services/order_service.py))

Se creó un nuevo servicio completo con los siguientes métodos:

#### Métodos principales:

- `create_order(user_id, user_email, order_data)` - Crea un pedido con ID automático
- `get_order(order_id)` - Obtiene un pedido por su ID
- `get_user_orders(user_email)` - **Obtiene todos los pedidos de un usuario por email**
- `update_order_status(order_id, new_status)` - Actualiza el estado de un pedido
- `get_all_orders(limit)` - Obtiene todos los pedidos (admin)
- `delete_order(order_id)` - Elimina un pedido (admin)

#### Funciones auxiliares:

- `_generate_order_id()` - Genera IDs con formato `ORD-20251205-XXXX`
- `_get_orders_ref()` - Referencia a `/orders` en Firebase

## Formato de Order ID

Los IDs de pedidos siguen el formato:

```
ORD-YYYYMMDD-XXXX
```

Donde:
- `ORD`: Prefijo fijo
- `YYYYMMDD`: Fecha de creación (20251205 = 5 de diciembre de 2025)
- `XXXX`: Sufijo único aleatorio de 4 caracteres hexadecimales

Ejemplos:
- `ORD-20251205-8672`
- `ORD-20251205-A3F1`
- `ORD-20251206-B92D`

## Identificadores de Pedido

Cada pedido tiene **dos identificadores**:

1. **order_id**: ID único del pedido (clave primaria en Firebase)
2. **user_email**: Email del usuario (para búsquedas y agrupación)

Esto permite:
- Buscar un pedido específico por `order_id`
- Buscar todos los pedidos de un usuario por `user_email`
- Asociar pedidos a un usuario incluso si cambia su `user_id` en Firebase Auth

## Estados de Pedido (OrderStatusEnum)

Los estados posibles son:

- `pending`: Pedido pendiente de procesamiento
- `processing`: Pedido en procesamiento
- `shipped`: Pedido enviado
- `delivered`: Pedido entregado
- `cancelled`: Pedido cancelado

## Cálculo de Totales

El sistema calcula automáticamente:

1. **Subtotal**: Suma de todos los items
   ```
   subtotal = Σ(item.subtotal)
   ```

2. **Costo de envío**:
   ```
   shipping_cost = subtotal >= 50€ ? 0€ : 5€
   ```

3. **IVA (21%)**:
   ```
   tax = (subtotal + shipping_cost) × 0.21
   ```

4. **Total**:
   ```
   total = subtotal + shipping_cost + tax
   ```

## Ejemplo de Uso

```python
from backend.services.order_service import OrderService
from backend.models.models import OrderCreate, OrderItem, ShippingAddress, Personalization

# Crear items
items = [
    OrderItem(
        product_id="prod_001",
        product_name="Camiseta FC Barcelona",
        product_image="https://...",
        team="Barcelona",
        quantity=2,
        size="L",
        unit_price=89.99,
        personalization_price=10.00,
        personalization=Personalization(nombre="MESSI", numero=10),
        subtotal=199.98
    )
]

# Dirección de envío
address = ShippingAddress(
    street="Calle Ejemplo 123",
    city="Madrid",
    state="Madrid",
    postal_code="28001",
    country="España"
)

# Crear pedido
order_data = OrderCreate(
    items=items,
    shipping_address=address,
    payment_method="credit_card"
)

# Guardar en Firebase
order = OrderService.create_order(
    user_id="fZlBToT35rPVcuUg3SO1oTuXwM22",
    user_email="hola@gmail.com",
    order_data=order_data
)

print(f"Pedido creado: {order.order_id}")

# Obtener pedidos del usuario
user_orders = OrderService.get_user_orders("hola@gmail.com")
print(f"Total de pedidos: {len(user_orders)}")
```

## Script de Prueba

Ejecuta el script de prueba para verificar el funcionamiento:

```bash
python3 test_order_service.py
```

El script prueba:
- ✅ Creación de pedidos
- ✅ Obtención de pedidos por ID
- ✅ Obtención de pedidos por email de usuario
- ✅ Actualización de estado
- ✅ Eliminación de pedidos

## Resumen

✨ **Los esquemas de pedidos ahora incluyen:**

1. ✅ `order_id` como identificador único con formato `ORD-YYYYMMDD-XXXX`
2. ✅ `user_email` para identificar pedidos por usuario
3. ✅ Personalización completa en cada item (nombre + número)
4. ✅ Información completa del producto (imagen, equipo, etc.)
5. ✅ Servicio completo para gestionar pedidos en Firebase
6. ✅ Pruebas automatizadas verificadas
