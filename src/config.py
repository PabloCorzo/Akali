"""
Configuration module
Este módulo contiene todas las configuraciones de la aplicación Flask.
Permite separar las configuraciones por entorno (desarrollo, producción, testing).
"""

import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    """Configuración base - común para todos los entornos"""
    
    # Configuración de Flask
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-key-please-change-in-production')
    SESSION_PERMANENT = False
    
    # Configuración de Base de Datos
    DB_USER = os.getenv("DB_USER")
    DB_PASSWORD = os.getenv("DB_PASSWORD")
    DB_HOST = os.getenv("DB_HOST")
    DB_NAME = os.getenv("DB_NAME")
    DB_PORT = os.getenv("DB_PORT")
    
    # URI de SQLAlchemy
    SQLALCHEMY_DATABASE_URI = f"mysql+mysqlconnector://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Configuración de templates y archivos estáticos
    TEMPLATE_FOLDER = 'templates'
    STATIC_FOLDER = 'static'


class DevelopmentConfig(Config):
    """Configuración para entorno de desarrollo"""
    DEBUG = True
    ENV = 'development'


class ProductionConfig(Config):
    """Configuración para entorno de producción"""
    DEBUG = False
    ENV = 'production'
    # En producción, SECRET_KEY DEBE venir de variable de entorno
    SECRET_KEY = os.getenv('SECRET_KEY')
    
    @classmethod
    def init_app(cls, app):
        """Validaciones adicionales para producción"""
        if not cls.SECRET_KEY:
            raise ValueError("SECRET_KEY debe estar definida en producción")


class TestingConfig(Config):
    """Configuración para testing/pruebas"""
    TESTING = True
    DEBUG = True
    # Base de datos en memoria para tests
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'


# Diccionario para seleccionar la configuración según el entorno
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}
