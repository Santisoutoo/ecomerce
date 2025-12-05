"""
Configuración e inicialización de Firebase Admin SDK.
Proporciona acceso a Realtime Database y Firebase Authentication.
"""

import firebase_admin
from firebase_admin import credentials, auth, db, storage
from functools import lru_cache
from .settings import FIREBASE_CREDENTIALS_PATH
import os


# Variable global para la app de Firebase
_firebase_app = None


def initialize_firebase():
    """
    Inicializa Firebase Admin SDK con las credenciales del proyecto.
    Solo se ejecuta una vez (singleton pattern).

    Returns:
        firebase_admin.App: Instancia de la aplicación Firebase
    """
    global _firebase_app

    if _firebase_app is not None:
        return _firebase_app

    try:
        # Obtener URL de Realtime Database
        database_url = os.getenv("FIREBASE_DATABASE_URL", "https://sportstyle-store-default-rtdb.firebaseio.com")

        # Opción 1: Usar archivo de credenciales JSON
        if FIREBASE_CREDENTIALS_PATH.exists():
            cred = credentials.Certificate(str(FIREBASE_CREDENTIALS_PATH))
            _firebase_app = firebase_admin.initialize_app(cred, {
                'databaseURL': database_url
            })
            print(f"✅ Firebase initialized with credentials file: {FIREBASE_CREDENTIALS_PATH}")

        # Opción 2: Usar credenciales desde variables de entorno (producción)
        elif os.getenv("FIREBASE_PROJECT_ID"):
            cred = credentials.Certificate({
                "type": "service_account",
                "project_id": os.getenv("FIREBASE_PROJECT_ID"),
                "private_key_id": os.getenv("FIREBASE_PRIVATE_KEY_ID"),
                "private_key": os.getenv("FIREBASE_PRIVATE_KEY").replace('\\n', '\n'),
                "client_email": os.getenv("FIREBASE_CLIENT_EMAIL"),
                "client_id": os.getenv("FIREBASE_CLIENT_ID"),
                "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                "token_uri": "https://oauth2.googleapis.com/token",
                "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
                "client_x509_cert_url": os.getenv("FIREBASE_CLIENT_CERT_URL")
            })
            _firebase_app = firebase_admin.initialize_app(cred, {
                'databaseURL': database_url
            })
            print("✅ Firebase initialized with environment variables")

        else:
            raise FileNotFoundError(
                "No Firebase credentials found. "
                "Please provide firebase-credentials.json or set environment variables."
            )

        return _firebase_app

    except Exception as e:
        print(f"❌ Error initializing Firebase: {e}")
        raise


def get_database():
    """
    Obtiene una referencia a Firebase Realtime Database.

    Returns:
        db.Reference: Referencia a la raíz de la base de datos
    """
    initialize_firebase()
    return db.reference()


def get_auth_client():
    """
    Obtiene acceso a Firebase Authentication.

    Returns:
        Module: Módulo firebase_admin.auth
    """
    initialize_firebase()
    return auth


def get_storage_bucket():
    """
    Obtiene una referencia al bucket de Firebase Storage.

    Returns:
        storage.Bucket: Referencia al bucket de almacenamiento
    """
    initialize_firebase()
    bucket_name = os.getenv("FIREBASE_STORAGE_BUCKET", "sportstyle-store.firebasestorage.app")
    return storage.bucket(bucket_name)
