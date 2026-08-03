# WeatherFlow API 🌤️

<p align="left">
  <a href="https://www.python.org/"><img src="https://img.shields.io/badge/python-3.10%2B-blue.svg" alt="Python Version"></a>
  <a href="https://www.djangoproject.com/"><img src="https://img.shields.io/badge/framework-Django%205.0%2B-green.svg" alt="Framework"></a>
  <a href="https://www.django-rest-framework.org/"><img src="https://img.shields.io/badge/DRF-3.15.0%2B-red.svg" alt="REST Framework"></a>
  <a href="LICENSE"><img src="https://img.shields.io/badge/License-MIT-yellow.svg" alt="License: MIT"></a>
</p>

**WeatherFlow API** es un servicio web RESTful desarrollado en Python y Django REST Framework para la gestión de usuarios, preferencias meteorológicas personalizadas y agregación de datos del clima.

---

## 🚀 Características Principales

- **Gestión de Usuarios y Preferencias:** Creación y administración de perfiles con configuración de unidades de temperatura (`Celsius` / `Fahrenheit`) y frecuencia de notificaciones.
- **Documentación Interactiva OpenAPI 3:** Integración con Swagger UI y ReDoc a través de `drf-spectacular`.
- **Arquitectura Modular:** Separación clara y limpia de `views` y `serializers` en paquetes dedicados para máxima escalabilidad y mantenibilidad.
- **Health Check Endpoint:** Punto de entrada `/api/health/` para monitoreo de estado del servicio.
- **Seguridad y Variables de Entorno:** Configuración basada en la nube / local con `python-dotenv` y headers CORS dinámicos (`django-cors-headers`).
- **Suite de Pruebas:** Pruebas unitarias y de integración con `pytest-django`.

---

## 🛠️ Tecnologías Utilizadas

- **Lenguaje:** Python 3.10+
- **Backend:** Django 5.0+, Django REST Framework (DRF) 3.15+
- **Documentación API:** `drf-spectacular` (Swagger UI & ReDoc)
- **Base de Datos:** SQLite (Desarrollo)
- **Testing:** `pytest`, `pytest-django`
- **Configuración:** `python-dotenv`, `django-cors-headers`

---

## 📁 Estructura del Proyecto

```text
WeatherFlow APP/
├── api/                        # Aplicación principal de la API
│   ├── models.py               # Modelos de datos (UserPreferences, etc.)
│   ├── permissions.py          # Permisos personalizados de DRF
│   ├── validators.py           # Validadores personalizados de datos
│   ├── urls.py                 # Enrutamiento interno de la API
│   ├── views/                  # Vistas modularizadas
│   │   ├── __init__.py
│   │   ├── schemas.py          # Decoradores y esquemas OpenAPI
│   │   ├── user_views.py       # ViewSets de Usuarios y Preferencias
│   │   └── utility_views.py    # Health Check y vistas utilitarias
│   ├── serializers/            # Serializadores modularizados
│   │   ├── __init__.py
│   │   ├── user_serializers.py # Serializadores de Usuarios y Preferencias
│   │   └── utility_serializers.py
│   └── tests/                  # Suite de pruebas unitarias e integración
│       ├── test_user_serializers.py
│       └── test_user_views.py
├── config/                     # Configuración global del proyecto Django
│   ├── settings.py             # Configuración principal y variables de entorno
│   ├── urls.py                 # Enrutamiento raíz y Swagger/ReDoc
│   └── wsgi.py / asgi.py
├── manage.py
├── pytest.ini
└── requirements.txt
```

---

## ⚙️ Instalación y Configuración

### 1. Clonar el repositorio
```bash
git clone https://github.com/GustavoBaranda/WeatherFlow-APP.git
cd "WeatherFlow APP"
```

### 2. Crear y activar entorno virtual
```bash
# En Windows (PowerShell):
python -m venv venv
.\venv\Scripts\Activate.ps1

# En Linux/macOS:
python3 -m venv venv
source venv/bin/activate
```

### 3. Instalar dependencias
```bash
pip install -r requirements.txt
```

### 4. Configurar variables de entorno
Crea un archivo `.env` basado en `.env.example`:
```env
DEBUG=True
SECRET_KEY=tu_secret_key_aqui
ALLOWED_HOSTS=localhost,127.0.0.1
CORS_ALLOWED_ORIGINS=http://localhost:3000,http://127.0.0.1:3000
```

### 5. Ejecutar migraciones e iniciar el servidor
```bash
python manage.py migrate
python manage.py runserver
```

---

## 📌 Documentación de la API

Una vez iniciado el servidor (`http://127.0.0.1:8000/`), puedes acceder a la documentación interactiva:

- **Swagger UI (Redirección por defecto):** [http://127.0.0.1:8000/](http://127.0.0.1:8000/) o `/api/schema/swagger-ui/`
- **ReDoc:** `/api/schema/redoc/`
- **Esquema OpenAPI en JSON/YAML:** `/api/schema/`

### Principales Endpoints:

| Método | Endpoint | Descripción |
| :--- | :--- | :--- |
| `GET` | `/api/health/` | Verificación de estado del servicio |
| `GET` | `/api/users/` | Listar usuarios registrados |
| `POST` | `/api/users/` | Registrar nuevo usuario |
| `GET` | `/api/users/{id}/` | Detalle del usuario |
| `GET` | `/api/users/{id}/preferences/` | Obtener preferencias del usuario |
| `PUT / PATCH` | `/api/users/{id}/preferences/` | Actualizar preferencias del usuario |

---

## 🧪 Ejecución de Pruebas

Para correr la suite de tests con `pytest`:

```bash
pytest
```

---

## 👤 Autor

Desarrollado por **Gustavo Baranda**
- **GitHub:** [@GustavoBaranda](https://github.com/GustavoBaranda)
- **Email:** baranda.gustavo@gmail.com

---

## 📄 Licencia

Este proyecto está bajo la Licencia **MIT**. Consulta el archivo `LICENSE` para más detalles.
