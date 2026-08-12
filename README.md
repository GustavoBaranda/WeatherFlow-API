# WeatherFlow API 🌤️

<p align="center">
  <img src="https://img.shields.io/badge/PYTHON-3.13-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python">
  <img src="https://img.shields.io/badge/DJANGO-5.0%2B-092E20?style=for-the-badge&logo=django&logoColor=white" alt="Django">
  <img src="https://img.shields.io/badge/DRF-3.15%2B-A30000?style=for-the-badge&logo=django&logoColor=white" alt="DRF">
  <img src="https://img.shields.io/badge/JWT_AUTH-JWT-000000?style=for-the-badge&logo=jsonwebtokens&logoColor=white" alt="JWT">
  <img src="https://img.shields.io/badge/OPENAPI_3-SWAGGER-85EA2D?style=for-the-badge&logo=openapi-initiative&logoColor=black" alt="OpenAPI">
  <img src="https://img.shields.io/badge/RENDER-LIVE_DEPLOY-46E3B7?style=for-the-badge&logo=render&logoColor=black" alt="Render">
  <img src="https://img.shields.io/badge/DOCKER-READY-2496ED?style=for-the-badge&logo=docker&logoColor=white" alt="Docker">
  <img src="https://img.shields.io/badge/LICENSE-MIT-green.svg?style=for-the-badge" alt="License">
</p>

> **WeatherFlow API** es una solución backend RESTful enterprise desarrollada en Python 3 y Django REST Framework para la gestión de usuarios, agregación meteorológica en tiempo real con geocodificación global, notificaciones in-app y seguridad stateless mediante JWT.
> 
> 🌐 **URL de Producción (Render Cloud):** [https://weatherflow-api.onrender.com](https://weatherflow-api.onrender.com)  
> 📖 **Documentación Swagger UI:** [https://weatherflow-api.onrender.com/api/schema/swagger-ui/](https://weatherflow-api.onrender.com/api/schema/swagger-ui/)

---

## 🌟 Visión General y Highlights Técnicos

**WeatherFlow API** está diseñada bajo principios de arquitectura limpia, desacoplamiento modular y máxima mantenibilidad. Ofrece una plataforma robusta para aplicaciones web y móviles que requieren información meteorológica adaptada a las preferencias individuales del usuario.

### 💡 Arquitectura y Decisiones Clave:
- **Autenticación Stateless JWT:** Emisión y renovación de pares de tokens (*Access & Refresh Tokens*) mediante `djangorestframework-simplejwt`.
- **Perfil de Usuario Autenticado (`/api/users/me/`):** Endpoint dedicado para que cualquier usuario acceda y actualice su perfil e información personal sin requerir permisos administrativos.
- **Integración Meteorológica & Geocodificación Dinámica:** Conexión con las APIs de *Open-Meteo* para búsqueda de cualquier ciudad del mundo y cálculo de pronósticos detallados.
- **Conversión Automática de Unidades:** Lógica de negocio orientada a las preferencias del usuario (`Celsius` / `Fahrenheit`).
- **Módulo de Notificaciones In-App:** Sistema nativo para generación de alertas y resúmenes climáticos con contador de no leídas (`🔔`).
- **Caché en Memoria y Rate Limiting:** Optimización de tiempos de respuesta a **~2ms** por *cache hit* (`django.core.cache`) y protección con limitación de tasa (*Throttling*) en DRF.
- **Documentación Interactiva OpenAPI 3:** Integración completa de esquemas tipados con `drf-spectacular` en Swagger UI y ReDoc.
- **CORS Habilitado para Integración Frontend:** Configuración flexible (`CORS_ALLOW_ALL_ORIGINS=True`) para permitir consumo inmediato desde aplicaciones móviles Expo / React Native o clientes Web (React, Next.js).
- **Infraestructura y Despliegue en la Nube:** Manifiesto de infraestructura como código `render.yaml` (Plan Gratuito), distribución de estáticos con `WhiteNoise`, servidor WSGI `Gunicorn`, base de datos PostgreSQL en producción y pipeline de CI/CD automatizado en GitHub Actions (`.github/workflows/django_ci.yml`).

---

## 📂 Estructura del Proyecto

```text
WeatherFlow APP/
├── .github/
│   └── workflows/
│       └── django_ci.yml      # CI/CD Pipeline (GitHub Actions)
├── api/                       # Aplicación Principal Django
│   ├── migrations/            # Migraciones de base de datos
│   ├── models.py              # Modelos UserPreferences y Notification
│   ├── permissions.py         # Permisos DRF personalizados (IsSelfOrAdmin)
│   ├── validators.py          # Validador de complejidad de contraseña
│   ├── urls.py                # Enrutamiento de la API REST
│   ├── services/              # Capa de Servicios y Lógica de Negocio
│   │   ├── geocoding_service.py  # Geocodificación y búsqueda dinámica de ciudades
│   │   └── weather_service.py    # Servicio meteorológico y conversión de unidades
│   ├── serializers/           # Serializadores tipados
│   │   ├── users.py
│   │   ├── weather.py
│   │   └── notifications.py
│   ├── views/                 # Vistas modularizadas
│   │   ├── health.py          # Endpoint de Health Check
│   │   ├── users.py           # UserViewSet, Me Endpoint y Preferencias
│   │   ├── weather.py         # Clima actual, pronósticos y búsqueda
│   │   └── notifications.py   # ViewSet de Notificaciones In-App
│   └── tests/                 # Suite de 39 pruebas automatizadas
│       ├── test_health.py
│       ├── test_jwt_auth.py
│       ├── test_models.py
│       ├── test_notifications.py
│       ├── test_permissions.py
│       ├── test_user_views.py
│       └── test_weather_views.py
├── config/                    # Configuración Global Django
│   ├── settings.py            # Settings, JWT, Caché, Rate Limiting & WhiteNoise
│   ├── urls.py                # Rutas raíz, JWT & Swagger UI
│   ├── wsgi.py / asgi.py
├── .env.example               # Plantilla de variables de entorno
├── Dockerfile                 # Contenedor de producción multi-etapa
├── docker-compose.yml         # Orquestación local (Django + PostgreSQL 16)
├── render.yaml                # Manifiesto de despliegue en Render.com
├── manage.py
├── pytest.ini
└── requirements.txt           # Dependencias del proyecto
```

---

## 🛠️ Tech Stack

| Categoría | Tecnología | Uso en el Proyecto |
| :--- | :--- | :--- |
| **Lenguaje** | [Python 3.13](https://www.python.org/) | Lenguaje base de desarrollo |
| **Framework Web** | [Django 5.0+](https://www.djangoproject.com/) | Framework MVC backend |
| **API REST** | [Django REST Framework](https://www.django-rest-framework.org/) | Construcción de APIs y ViewSets |
| **Autenticación** | [SimpleJWT](https://django-rest-framework-simplejwt.readthedocs.io/) | Tokens JWT (*Access / Refresh*) |
| **Documentación** | [drf-spectacular](https://drf-spectacular.readthedocs.io/) | OpenAPI 3, Swagger UI & ReDoc |
| **Base de Datos** | SQLite (Dev) / PostgreSQL (Prod) | Almacenamiento persistente con `dj-database-url` |
| **Caché & Throttling** | `django.core.cache` + DRF Throttling | In-memory caching & Rate Limiting |
| **Estáticos & Server** | WhiteNoise + Gunicorn | Servidor WSGI y distribución de estáticos |
| **Despliegue Cloud** | [Render Cloud](https://render.com/) | Hospedaje y base de datos gestionada |
| **Testing** | [pytest-django](https://pytest-django.readthedocs.io/) | Suite de 39 pruebas automatizadas |
| **Contenedores & CI** | Docker + GitHub Actions | Contenedorización e Integración Continua |

---

## ⚡ Guía de Instalación Rápida (Quickstart)

### 1. Clonar el Repositorio
```bash
git clone https://github.com/GustavoBaranda/WeatherFlow-API.git
cd "WeatherFlow APP"
```

### 2. Crear y Activar Entorno Virtual

**En Linux / macOS:**
```bash
python3 -m venv venv
source venv/bin/activate
```

**En Windows (PowerShell):**
```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

### 3. Instalar Dependencias
```bash
pip install -r requirements.txt
```

### 4. Configurar Variables de Entorno
Crea un archivo `.env` basado en `.env.example`:
```env
SECRET_KEY=tu_secret_key_de_desarrollo
DEBUG=True
ALLOWED_HOSTS=127.0.0.1,localhost
CORS_ALLOW_ALL_ORIGINS=True
CORS_ALLOWED_ORIGINS=http://localhost:3000,http://127.0.0.1:3000
```

### 5. Ejecutar Migraciones e Iniciar el Servidor
```bash
python manage.py migrate
python manage.py runserver 8001
```

---

### 🐳 Alternativa con Docker Compose (Opcional)

Si deseas levantar la aplicación junto a un servidor **PostgreSQL 16** real mediante Docker:

```bash
docker compose up --build
```

---

## 📌 Documentación de la API (OpenAPI 3)

Accede a la documentación interactiva desplegada en producción o localmente:

- **Swagger UI (Redirección por defecto):** [https://weatherflow-api.onrender.com/](https://weatherflow-api.onrender.com/) o `/api/schema/swagger-ui/`
- **ReDoc:** `/api/schema/redoc/`
- **Esquema OpenAPI JSON/YAML:** `/api/schema/`

### Principales Endpoints:

| Método | Endpoint | Descripción | Autenticación |
| :--- | :--- | :--- | :---: |
| `GET` | `/api/health/` | Estado del servicio y versión | Pública |
| `POST` | `/api/token/` | Obtener par de tokens JWT (*Access & Refresh*) | Pública |
| `POST` | `/api/token/refresh/` | Renovar token de acceso JWT | Pública |
| `POST` | `/api/users/` | Registrar nuevo usuario | Pública |
| `GET` | `/api/users/` | Listar usuarios (Solo administradores) | `Bearer JWT` |
| `GET / PATCH` | `/api/users/me/` | Obtener o actualizar perfil del usuario autenticado | `Bearer JWT` |
| `GET / PATCH` | `/api/users/me/preferences/` | Obtener o actualizar preferencias de perfil | `Bearer JWT` |
| `GET` | `/api/weather/cities/search/?q=` | Búsqueda dinámica de ciudades del mundo | `Bearer JWT` |
| `GET` | `/api/weather/current/?city=` | Clima actual adaptado a unidad del usuario | `Bearer JWT` |
| `GET` | `/api/weather/forecast/?city=` | Pronóstico de 7 días adaptado a unidad | `Bearer JWT` |
| `GET` | `/api/notifications/` | Listar notificaciones in-app | `Bearer JWT` |
| `GET` | `/api/notifications/unread-count/` | Contador de notificaciones no leídas (`🔔`) | `Bearer JWT` |
| `PATCH` | `/api/notifications/{id}/mark-read/` | Marcar notificación como leída | `Bearer JWT` |
| `POST` | `/api/notifications/mark-all-read/` | Marcar todas las notificaciones como leídas | `Bearer JWT` |
| `POST` | `/api/notifications/generate-summary/` | Generar reporte climático in-app | `Bearer JWT` |

---

## 🧪 Testing & Integración Continua (CI/CD)

El proyecto incluye una suite de **39 pruebas automatizadas** que cubren autenticación JWT, permisos, modelos, notificaciones, servicios meteorológicos y caché.

Para correr la suite de pruebas con `pytest`:

```bash
pytest
```

> 🟢 **GitHub Actions CI:** Cada `git push` o *Pull Request* desencadena automáticamente la ejecución del pipeline en `.github/workflows/django_ci.yml` en entornos aislados con Python 3.13.

---

## 👤 Autor

**Gustavo Baranda** — Lead Backend Developer & Cloud Enthusiast
- **Website:** [gustavobaranda.com](https://gustavobaranda.com/)
- **GitHub:** [@GustavoBaranda](https://github.com/GustavoBaranda)
- **LinkedIn:** [Gustavo Baranda](https://www.linkedin.com/in/gustavobaranda/)

---

## 📄 Licencia

Este proyecto está bajo la Licencia **MIT**. Consulta el archivo `LICENSE` para más detalles.
