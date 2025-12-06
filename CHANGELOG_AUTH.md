# Changelog - Migración de Autenticación a Base de Datos

**Fecha:** 6 de diciembre de 2025
**Resumen:** Migración completa del sistema de autenticación de Firebase Authentication a Firebase Realtime Database con bcrypt.

---

## ✨ Cambios Principales

### 1. Sistema de Autenticación con Base de Datos

**Archivos creados:**
- `backend/services/user_service.py` - Servicio completo de gestión de usuarios

**Características:**
- ✅ Passwords hasheados con bcrypt (salt automático)
- ✅ User IDs únicos de 28 caracteres (similar a Firebase Auth)
- ✅ Soft delete (usuarios marcados como inactivos)
- ✅ Validación de emails duplicados solo para usuarios activos
- ✅ Autenticación segura con verificación de password hash

**Métodos implementados:**
- `create_user()` - Registrar nuevos usuarios
- `authenticate_user()` - Validar email y contraseña
- `get_user_by_id()` - Obtener usuario por ID
- `get_user_by_email()` - Buscar usuario por email (solo activos por defecto)
- `update_user()` - Actualizar datos del usuario
- `change_password()` - Cambiar contraseña (requiere contraseña actual)
- `delete_user()` - Desactivar usuario (soft delete)
- `email_exists()` - Verificar si email está registrado (solo usuarios activos)

### 2. Corrección de Importaciones

**Problema:** El backend usaba importaciones relativas que fallaban cuando se importaban desde el frontend.

**Solución:** Se cambiaron todas las importaciones a rutas absolutas con prefijo `backend.`

**Archivos modificados:**
- `backend/services/cart_service.py`
- `backend/services/order_service.py`
- `backend/services/user_service.py`
- `backend/core/security.py`
- `backend/api/v1/endpoints/auth.py`
- `backend/main.py`

**Antes:**
```python
from config.firebase_config import get_database
from models.models import Cart
from services.user_service import UserService
```

**Ahora:**
```python
from backend.config.firebase_config import get_database
from backend.models.models import Cart
from backend.services.user_service import UserService
```

### 3. Actualización del Módulo de Seguridad

**Archivo:** `backend/core/security.py`

**Cambios:**
- Ahora valida usuarios contra Firebase Realtime Database en lugar de Firebase Auth
- Verifica que el usuario esté activo antes de autenticar
- Mantiene compatibilidad con JWT tokens

### 4. Actualización de Endpoints de Autenticación

**Archivo:** `backend/api/v1/endpoints/auth.py`

**Cambios en `/signup`:**
- Usa `UserService.create_user()` en lugar de Firebase Auth
- Passwords se hashean automáticamente
- Retorna token JWT

**Cambios en `/signin`:**
- Usa `UserService.authenticate_user()` para validar credenciales
- Verifica password con bcrypt
- Rechaza usuarios inactivos

**Cambios en `/me`:**
- Obtiene datos de Firebase Realtime Database
- Verifica estado activo del usuario

### 5. Scripts de Inicio

**Archivos creados:**
- `start_backend.sh` - Script para iniciar FastAPI desde el directorio correcto
- `start_frontend.sh` - Script para iniciar Streamlit
- `START_BACKEND.md` - Documentación del problema de importaciones

**Uso:**
```bash
# Backend
./start_backend.sh

# Frontend
./start_frontend.sh

# O manualmente desde la raíz:
python3 -m uvicorn backend.main:app --host 0.0.0.0 --port 8000 --reload
```

### 6. Documentación Actualizada

**Archivo:** `README.md`

**Añadido:**
- Instrucciones claras para ejecutar backend + frontend
- Dos opciones de ejecución (solo frontend vs arquitectura completa)
- URLs de acceso a API y documentación

---

## 🗄️ Estructura en Firebase

### Usuarios (`/users/{user_id}/`)

```json
{
  "email": "usuario@example.com",
  "password_hash": "$2b$12$...",
  "nombre": "Juan",
  "apellidos": "Pérez",
  "telefono": "612345678",
  "foto_perfil": "https://...",
  "fecha_registro": "2025-12-06T10:00:00",
  "puntos_fidelizacion": 0,
  "es_admin": false,
  "activo": true,
  "favoritos": [],
  "direccion_envio": {}
}
```

---

## 🧪 Tests

**Archivo:** `test_auth_database.py`

**Pruebas que pasan:**
1. ✅ Crear nuevos usuarios
2. ✅ Verificar emails duplicados
3. ✅ Autenticar con contraseña (bcrypt)
4. ✅ Rechazar contraseñas incorrectas
5. ✅ Obtener usuario por ID
6. ✅ Obtener usuario por email
7. ✅ Actualizar datos de usuario
8. ✅ Cambiar contraseña
9. ✅ Desactivar usuarios (soft delete)
10. ✅ Usuarios inactivos no pueden autenticarse

**Ejecutar tests:**
```bash
python3 test_auth_database.py
```

---

## 🔒 Seguridad

### Passwords

- **Algoritmo:** bcrypt con salt automático
- **Nunca** se almacenan contraseñas en texto plano
- **Nunca** se retornan password hashes en las respuestas
- Cambio de contraseña requiere contraseña actual

### Tokens

- **Formato:** JWT (JSON Web Tokens)
- **Contenido:** user_id y email
- **Expiración:** Configurable en `config/settings.py`
- **Validación:** Se verifica que el usuario exista y esté activo

### Usuarios Inactivos

- Los usuarios desactivados **no pueden** autenticarse
- Los emails de usuarios inactivos **pueden** reutilizarse
- El soft delete preserva datos históricos (pedidos, etc.)

---

## 📝 Notas Importantes

### Ejecución del Backend

⚠️ **MUY IMPORTANTE:** El backend debe ejecutarse desde la raíz del proyecto, no desde `backend/`:

```bash
# ❌ INCORRECTO
cd backend
python -m uvicorn main:app --reload

# ✅ CORRECTO
cd /home/santi/Documents/ecomerce
python3 -m uvicorn backend.main:app --reload
```

Esto es porque el proyecto usa importaciones absolutas (`from backend.config...`).

### Compatibilidad con Frontend

El frontend puede importar servicios del backend:

```python
from backend.services.cart_service import CartService
from backend.services.user_service import UserService
```

Esto funciona porque:
1. El frontend añade el directorio padre al Python path
2. El backend usa importaciones absolutas

---

## 🚀 Próximos Pasos (Opcional)

- [ ] Implementar reset de contraseña por email
- [ ] Añadir verificación de email
- [ ] Implementar rate limiting en endpoints de auth
- [ ] Añadir logs de intentos de login fallidos
- [ ] Implementar 2FA (autenticación de dos factores)

---

## 🔗 Enlaces Útiles

- **API Docs:** http://localhost:8000/docs
- **ReDoc:** http://localhost:8000/redoc
- **Frontend:** http://localhost:8501
- **Firebase Console:** https://console.firebase.google.com

---

## 👥 Créditos

**Migración realizada por:** Claude Code
**Equipo de Desarrollo:** Grupo 11 - SportStyle Store
