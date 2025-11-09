# 🎯 Sistema de Configuración - Guía de Uso

## 📁 Archivos Creados

### `src/config.py`
Archivo que centraliza todas las configuraciones de la aplicación.

## 🔧 Configuraciones Disponibles

### 1. **DevelopmentConfig** (Desarrollo) - Por defecto
- `DEBUG = True` - Modo debug activado
- Base de datos desde `.env`
- Recarga automática de código

### 2. **ProductionConfig** (Producción)
- `DEBUG = False` - Sin debug
- Secret key obligatoria desde variable de entorno
- Optimizado para rendimiento

### 3. **TestingConfig** (Testing)
- `TESTING = True`
- Base de datos SQLite en memoria
- Rápido para tests unitarios

## 🚀 Cómo Usar

### Desarrollo (por defecto)
```bash
python src/app.py
```

### Producción
```bash
# Windows PowerShell
$env:FLASK_ENV="production"
python src/app.py

# Linux/Mac
export FLASK_ENV=production
python src/app.py
```

### Testing
```bash
# Windows PowerShell
$env:FLASK_ENV="testing"
python src/app.py

# Linux/Mac
export FLASK_ENV=testing
python src/app.py
```

## 🔐 Variables de Entorno Necesarias

Asegúrate de tener un archivo `.env` en la raíz del proyecto:

```env
# Base de datos
DB_USER=tu_usuario
DB_PASSWORD=tu_password
DB_HOST=localhost
DB_NAME=akali_db
DB_PORT=3306

# Seguridad (opcional en desarrollo, OBLIGATORIO en producción)
SECRET_KEY=tu-clave-secreta-super-segura-aqui
```

## ✨ Beneficios del Refactor

### Antes ❌
```python
app.secret_key = 'key1'  # Hardcoded, inseguro
db_user = os.getenv("DB_USER")
db_pass = os.getenv("DB_PASSWORD")
# ... configuración mezclada con código
```

### Ahora ✅
```python
from config import config
app.config.from_object(config['development'])
# Todo centralizado, múltiples entornos, seguro
```

## 📊 Comparación

| Aspecto | Antes | Ahora |
|---------|-------|-------|
| **Organización** | Mezclado en app.py | Archivo dedicado config.py |
| **Seguridad** | Secret key hardcodeada | Desde variables de entorno |
| **Entornos** | Solo uno | Dev, Prod, Testing |
| **Mantenibilidad** | Difícil cambiar configs | Fácil y centralizado |
| **Testing** | Difícil | SQLite en memoria |



## 💡 Tips

- En **desarrollo**: Usa las configuraciones por defecto
- En **producción**: SIEMPRE define `SECRET_KEY` en el servidor
- Para **tests**: El entorno testing usa SQLite en memoria (súper rápido)
