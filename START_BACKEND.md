# Guía de Inicio del Backend

## Problema Común: ModuleNotFoundError

Si ves este error:
```
ModuleNotFoundError: No module named 'backend'
```

Es porque estás ejecutando uvicorn desde el directorio incorrecto.

## ❌ Forma INCORRECTA

```bash
# NO hagas esto:
cd backend
python -m uvicorn main:app --reload
```

## ✅ Forma CORRECTA

Siempre ejecuta uvicorn desde la **raíz del proyecto**:

```bash
# Asegúrate de estar en /home/santi/Documents/ecomerce
cd /home/santi/Documents/ecomerce

# Luego ejecuta:
python3 -m uvicorn backend.main:app --host 0.0.0.0 --port 8000 --reload
```

## Explicación

El proyecto usa importaciones absolutas (`from backend.config.firebase_config import ...`), por lo que Python necesita ver el directorio `backend/` como un paquete. Esto solo funciona cuando ejecutas desde el directorio raíz.

## Verificar que funciona

Una vez iniciado correctamente, deberías ver:

```
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
INFO:     Started reloader process [XXXXX] using WatchFiles
INFO:     Started server process [XXXXX]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
```

Y podrás acceder a:
- API: http://localhost:8000
- Documentación: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Comandos Rápidos

```bash
# Ver API root
curl http://localhost:8000/

# Debe responder:
# {"message":"Welcome to SportStyle Store API","version":"1.0.0",...}
```
