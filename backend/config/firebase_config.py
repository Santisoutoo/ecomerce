"""
Configuración e inicialización de Firebase Admin SDK.
Proporciona acceso a Firestore y Firebase Authentication.
"""

import firebase_admin
from firebase_admin import credentials, auth, firestore
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
        # Opción 1: Usar archivo de credenciales JSON
        if FIREBASE_CREDENTIALS_PATH.exists():
            cred = credentials.Certificate(str(FIREBASE_CREDENTIALS_PATH))
            _firebase_app = firebase_admin.initialize_app(cred)
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
            _firebase_app = firebase_admin.initialize_app(cred)
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


@lru_cache()
def get_firestore_client():
    """
    Obtiene una instancia del cliente de Firestore.
    Usa caché para evitar múltiples inicializaciones.

    Returns:
        firestore.Client: Cliente de Firestore
    """
    initialize_firebase()
    return firestore.client()


def get_auth_client():
    """
    Obtiene acceso a Firebase Authentication.

    Returns:
        Module: Módulo firebase_admin.auth
    """
    initialize_firebase()
    return auth
