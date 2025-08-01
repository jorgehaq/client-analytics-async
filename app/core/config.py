# app/core/config.py
import os
from typing import Optional
from pydantic_settings import BaseSettings

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    
MEDIA_URL = "/media"
MEDIA_ROOT = os.path.join(BASE_DIR, "media")
UPLOAD_DIR = os.path.join(MEDIA_ROOT, "datasets")


class Settings(BaseSettings):
    """
    Configuración de la aplicación usando Pydantic
    Equivale a settings.py de Django
    """
    
    # Configuración básica de la aplicación
    APP_NAME: str = "Client Analytics Async"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = False
    
    # Configuración de seguridad
    SECRET_KEY: str = "your-secret-key-change-in-production"
    
    # Configuración JWT
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7
    ALGORITHM: str = "HS256"
    
    # Configuración de base de datos
    DATABASE_URL: Optional[str] = None
    
    # Configuración de ambiente
    ENVIRONMENT: str = "development"

    @property
    def database_url(self):
        return self.DATABASE_URL

    class Config:
        """
        Configuración de Pydantic para leer variables de entorno
        Busca archivo .env automáticamente
        """
        env_file = ".env"
        case_sensitive = True


# Instancia global de configuración
settings = Settings()


def get_settings() -> Settings:
    """
    Función para obtener configuración
    Útil para dependency injection en FastAPI
    """
    return settings