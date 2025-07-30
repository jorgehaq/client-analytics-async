# app/core/config.py
from typing import Optional
from pydantic_settings import BaseSettings


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

    # ✅ Agregadas las variables de PostgreSQL
    POSTGRES_DB: str = "analytics_db"
    POSTGRES_USER: str = "analytics_user" 
    POSTGRES_PASSWORD: str = "password"
    POSTGRES_HOST: str = "localhost"
    POSTGRES_PORT: int = 5432
    
    # Configuración de ambiente
    ENVIRONMENT: str = "development"

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