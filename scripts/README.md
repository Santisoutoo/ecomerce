# Scripts de Sincronización con Firebase

Scripts para subir datos del JSON a Firebase Realtime Database.

## Scripts disponibles

### 1. `upload_to_firebase.py` - Carga completa
Sube todos los datos (productos, categorías, ligas, etc.) a Firebase.

**Uso:**
```bash
# Desde la raíz del proyecto
python scripts/upload_to_firebase.py

# Con ruta personalizada
python scripts/upload_to_firebase.py path/to/custom.json
```

### 2. `sync_products.py` - Sincronizar solo productos (recomendado)
Sube solo los productos con preview y confirmación interactiva.

**Uso:**
```bash
# Modo interactivo (con confirmación)
python scripts/sync_products.py

# Modo automático (sin confirmación)
python scripts/sync_products.py --yes
```

## Requisitos previos

1. **Credenciales de Firebase configuradas:**
   - Archivo `backend/config/firebase-credentials.json` presente
   - O variables de entorno configuradas

2. **Dependencias instaladas:**
   ```bash
   pip install firebase-admin
   ```

## Estructura de datos en Firebase

Los datos se organizan de la siguiente manera:

```
firebase-root/
├── products/
│   ├── prod_001/
│   ├── prod_002/
│   └── ...
├── categories/
│   ├── cat_001/
│   └── ...
├── leagues/
│   ├── league_001/
│   └── ...
├── users/
├── orders/
└── cart_items/
```

## Ejemplos

### Actualizar productos después de cambiar imágenes:
```bash
python scripts/sync_products.py
```

### Carga inicial completa:
```bash
python scripts/upload_to_firebase.py
```

### Verificar en Firebase Console:
https://console.firebase.google.com/project/sportstyle-store/database

**URL de la base de datos:**
https://sportstyle-store-default-rtdb.firebaseio.com

## Notas

- ⚠️ Los scripts **sobrescriben** los datos existentes
- 📦 Se recomienda usar `sync_products.py` para actualizaciones frecuentes
- 🔄 Usa `upload_to_firebase.py` solo para cargas iniciales o completas
- 📊 Firebase Realtime Database tiene límites de tamaño (1GB en plan gratuito)
