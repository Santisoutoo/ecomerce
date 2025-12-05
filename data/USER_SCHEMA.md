# Estructura de Usuarios

## Campos requeridos para registro de usuario:

```json
{
  "id": "user_XXX",
  "nombre": "String",
  "apellido": "String",
  "tlf": "String (formato: +34 XXX XXX XXX)",
  "password": "String (hasheada con bcrypt)",
  "avatar": "String (URL de imagen)"
}
```

## Ejemplo:

```json
{
  "id": "user_001",
  "nombre": "Juan",
  "apellido": "Pérez",
  "tlf": "+34 610 123 456",
  "password": "$2b$10$xYzABC123HashedPasswordExample",
  "avatar": "https://res.cloudinary.com/dlrrvenn1/image/upload/v1234567890/avatars/user_001.jpg"
}
```

## Notas:

- **password**: Nunca guardar contraseñas en texto plano. Usar bcrypt para hashear.
- **repetir contraseña**: Este campo solo se usa en el frontend para validación, NO se guarda en la base de datos.
- **avatar**: URL de la imagen del avatar del usuario (puede ser Cloudinary o cualquier CDN).
- **tlf**: Formato internacional recomendado (+34 para España).
