# FisioVis - Documentación Técnica

## 📋 Descripción General

**FisioVis** es una aplicación web desarrollada en Django que utiliza visión por computadora e inteligencia artificial para asistir a profesionales de fisioterapia. La aplicación permite:

- **Análisis de posturas corporales** mediante cámara ESP32
- **Cálculo automático de ángulos (goniometría)** usando MediaPipe
- **Gestión de pacientes** con historial médico completo
- **Generación de informes de progreso** con IA (OpenAI GPT)
- **Seguimiento de evaluaciones** a lo largo del tiempo

### Público Objetivo

- Fisioterapeutas profesionales
- Estudiantes de fisioterapia
- Profesionales de salud que deseen integrar IA en sus flujos de trabajo

---

## 🏗️ Arquitectura del Proyecto

### Estructura de Módulos

```
FisioVis/
├── FisioVis/           # Configuración principal del proyecto Django
│   ├── settings.py     # Configuración de Django
│   ├── urls.py         # Rutas principales
│   ├── views.py        # Vistas de landing y about
│   └── wsgi.py         # Configuración WSGI
│
├── users/              # Módulo de autenticación
│   ├── views.py        # Registro de usuarios
│   ├── urls.py         # Rutas de login/logout/registro
│   └── templates/      # Plantillas de autenticación
│
├── patients/           # Gestión de pacientes
│   ├── models.py       # Modelo Patient
│   ├── views.py        # CRUD de pacientes
│   ├── forms.py        # Formularios
│   └── templates/      # Plantillas de pacientes
│
├── assessments/        # Evaluaciones goniométricas
│   ├── models.py       # Assessment, PatientAssessment
│   ├── views.py        # Lógica de visión por computadora
│   └── templates/      # Plantillas de evaluación
│
├── reports/            # Generación de informes
│   ├── views.py        # Generación de PDF con IA
│   └── templates/      # Plantillas de reportes
│
├── static/             # Archivos estáticos (CSS, JS, imágenes, fuentes)
├── media/              # Archivos subidos (fotos de evaluaciones)
├── templates/          # Plantillas globales (base.html, landing.html)
└── manage.py           # Comando de gestión de Django
```

### Diagrama de Arquitectura

```
┌─────────────────────────────────────────────────────────────────┐
│                         CLIENTE (Browser)                        │
└─────────────────────────────────────────────────────────────────┘
                                   │
                                   ▼
┌─────────────────────────────────────────────────────────────────┐
│                      Django Application                          │
│  ┌─────────┐  ┌──────────┐  ┌─────────────┐  ┌─────────┐       │
│  │  Users  │  │ Patients │  │ Assessments │  │ Reports │       │
│  └─────────┘  └──────────┘  └─────────────┘  └─────────┘       │
└─────────────────────────────────────────────────────────────────┘
         │              │              │              │
         ▼              ▼              ▼              ▼
┌──────────────┐  ┌──────────┐  ┌──────────────┐  ┌───────────┐
│  PostgreSQL  │  │  ESP32   │  │  MediaPipe   │  │  OpenAI   │
│   Database   │  │  Camera  │  │  (Pose Est.) │  │   GPT-5   │
└──────────────┘  └──────────┘  └──────────────┘  └───────────┘
```

### Stack Tecnológico

| Componente             | Tecnología                            |
| ---------------------- | ------------------------------------- |
| Backend                | Django 5.2.7                          |
| Base de Datos          | PostgreSQL                            |
| Visión por Computadora | OpenCV + MediaPipe                    |
| IA/Informes            | OpenAI API (GPT-5)                    |
| Frontend               | Django Templates + Tailwind CSS       |
| Formularios            | django-crispy-forms + crispy-tailwind |
| PDF                    | fpdf2                                 |
| Hardware               | ESP32-CAM                             |

---

## 🚀 Pasos de Instalación

### Prerrequisitos

- **Python 3.11+** ([Descargar](https://www.python.org/))
- **PostgreSQL** ([Descargar](https://www.postgresql.org/))
- **Git** (opcional pero recomendado)

### 1. Clonar el Repositorio

```bash
git clone https://github.com/Loperaa-Juan/FisioVis
cd FisioVis
```

### 2. Crear y Activar Entorno Virtual

```bash
# Windows
python -m venv venv
.\venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### 3. Instalar Dependencias

```bash
pip install -r requirements.txt
```

### 4. Configurar Variables de Entorno

Crear un archivo `.env` en la raíz del proyecto:

```env
# Base de datos
DB_NAME=postgres
DB_USER=postgres
DB_PASSWORD=tu_password
DB_HOST=localhost
DB_PORT=5434

# OpenAI API
OPENAI_API_KEY=sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx

# Django
SECRET_KEY=tu-secret-key-super-seguro
DEBUG=True
```

### 5. Configurar Base de Datos

Editar `FisioVis/settings.py` si es necesario para coincidir con tu configuración de PostgreSQL:

```python
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": "postgres",      # Nombre de la BD
        "PORT": "5434",          # Puerto de PostgreSQL
        "USER": "postgres",      # Usuario
        "HOST": "localhost",     # Host
        "PASSWORD": "lopera",    # Contraseña
    }
}
```

### 6. Ejecutar Migraciones

```bash
python manage.py migrate
```

### 7. Crear Superusuario (Opcional)

```bash
python manage.py createsuperuser
```

### 8. Iniciar Servidor de Desarrollo

```bash
python manage.py runserver
```

La aplicación estará disponible en: `http://127.0.0.1:8000/`

---

## 🔑 Claves API y Configuración

### OpenAI API Key

La aplicación utiliza OpenAI para generar informes de progreso clínico.

**Obtener API Key:**

1. Ir a [OpenAI Platform](https://platform.openai.com/)
2. Crear una cuenta o iniciar sesión
3. Navegar a **API Keys** en el menú lateral
4. Crear nueva clave secreta

**Configuración:**

```env
OPENAI_API_KEY=sk-proj-xxxxxxxxxxxxxxxxxxxxxxxxxxxx
```

**Uso en el código** (`reports/views.py`):

```python
from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Ejemplo de uso
response = client.responses.create(
    model="gpt-5",
    input=prompt
)
informe = response.output_text
```

### ESP32-CAM

La cámara ESP32 se usa para capturar imágenes de pacientes durante evaluaciones.

**Configuración actual** (`assessments/views.py`):

```python
ESP32_URL = "http://10.201.194.31/capture"
```

**Ejemplo de captura:**

```python
import requests

# Obtener imagen desde ESP32
esp_response = requests.get(ESP32_URL, timeout=10)
if esp_response.status_code == 200:
    img_bytes = esp_response.content
    # Procesar imagen...
```

> ⚠️ **Nota:** Cambiar la IP según la configuración de tu red local.

---

## 📡 Endpoints de la API

### Autenticación (users/)

| Método   | Ruta               | Descripción               |
| -------- | ------------------ | ------------------------- |
| GET/POST | `/users/login`     | Inicio de sesión          |
| POST     | `/users/logout/`   | Cierre de sesión          |
| GET/POST | `/users/registro/` | Registro de nuevo usuario |

### Pacientes (patients/)

| Método   | Ruta                          | Descripción                  | Autenticación |
| -------- | ----------------------------- | ---------------------------- | ------------- |
| GET      | `/patients/list/`             | Listar pacientes del usuario | ✅ Requerida  |
| GET/POST | `/patients/create/`           | Crear nuevo paciente         | ✅ Requerida  |
| GET      | `/patients/details/<uuid:id>` | Ver detalles del paciente    | ✅ Requerida  |
| GET/POST | `/patients/update/<uuid:id>`  | Editar paciente              | ✅ Requerida  |
| GET/POST | `/patients/delete/<uuid:id>`  | Eliminar paciente            | ✅ Requerida  |

**Ejemplo - Crear Paciente (POST):**

```json
{
  "full_name": "Juan Pérez García",
  "age": 35,
  "sex": "M",
  "phone": "+57 300 123 4567",
  "email": "juan@email.com",
  "work": "Oficinista",
  "medical_history": "Sin antecedentes relevantes",
  "surgeries": "Ninguna",
  "pathologies": "Ninguna",
  "medications": "Ninguno"
}
```

### Evaluaciones (assessments/)

| Método | Ruta                              | Descripción                       | Autenticación |
| ------ | --------------------------------- | --------------------------------- | ------------- |
| GET    | `/assessments/evaluate/<uuid:id>` | Vista de evaluación para paciente | ✅ Requerida  |
| POST   | `/assessments/eval`               | Procesar imagen y calcular ángulo | ❌            |
| POST   | `/assessments/save`               | Guardar evaluación con imagen     | ❌            |

**Ejemplo - Evaluar Movimiento (POST `/assessments/eval`):**

Request:

```json
{
  "exam_type": "ROM Hombro D"
}
```

**Tipos de examen disponibles:**

- `ROM Hombro D` - Rango de movimiento hombro derecho
- `ROM Hombro I` - Rango de movimiento hombro izquierdo
- `ROM Codo D` - Rango de movimiento codo derecho
- `ROM Codo I` - Rango de movimiento codo izquierdo

Response exitosa:

```json
{
  "image": "data:image/jpeg;base64,/9j/4AAQSkZJRg...",
  "angle": 145
}
```

**Ejemplo - Guardar Evaluación (POST `/assessments/save`):**

Request (multipart/form-data):

```
patient_id: 550e8400-e29b-41d4-a716-446655440000
assessment: "ROM Hombro D"
angle: 145
image: <archivo_imagen.jpg>
```

Response:

```json
{
  "message": "Imagen guardada correctamente",
  "image_url": "/media/assessments/550e8400_20260118_143022.jpg"
}
```

### Reportes (reports/)

| Método | Ruta                               | Descripción                    | Autenticación |
| ------ | ---------------------------------- | ------------------------------ | ------------- |
| GET    | `/reports/patient_list/`           | Listar pacientes para reportes | ✅ Requerida  |
| GET    | `/reports/create_report/<uuid:id>` | Generar PDF de progreso        | ✅ Requerida  |

**Ejemplo - Generar Reporte:**

```bash
GET /reports/create_report/550e8400-e29b-41d4-a716-446655440000
```

**Respuesta:** Archivo PDF descargable con análisis de IA del progreso del paciente.

El reporte incluye:

- Datos del paciente
- Historial de evaluaciones goniométricas
- Análisis de progreso generado por IA
- Gráficos de evolución de ángulos

### Páginas Generales

| Método | Ruta      | Descripción                    |
| ------ | --------- | ------------------------------ |
| GET    | `/`       | Landing page                   |
| GET    | `/about`  | Página "Acerca de"             |
| GET    | `/admin/` | Panel de administración Django |

---

## 📊 Modelos de Datos

### Patient (patients/models.py)

```python
class Patient(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    full_name = models.TextField(max_length=100)
    age = models.IntegerField()
    sex = models.CharField(max_length=10, choices=[("M", "Masculino"), ("F", "Femenino")])
    phone = models.CharField(max_length=20, null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    work = models.TextField(max_length=200)
    medical_history = models.TextField(max_length=500)
    surgeries = models.TextField(max_length=500, blank=True, null=True)
    pathologies = models.TextField(max_length=500, blank=True, null=True)
    medications = models.TextField(max_length=500, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
```

**Campos:**

- `id`: Identificador único UUID
- `user`: Usuario propietario (ForeignKey)
- `full_name`: Nombre completo del paciente
- `age`: Edad en años
- `sex`: Sexo ('M' = Masculino, 'F' = Femenino)
- `phone`: Número de teléfono (opcional)
- `email`: Correo electrónico (opcional)
- `work`: Ocupación laboral
- `medical_history`: Antecedentes médicos
- `surgeries`: Cirugías previas (opcional)
- `pathologies`: Patologías existentes (opcional)
- `medications`: Medicamentos actuales (opcional)
- `is_active`: Estado activo del registro
- `created_at`: Fecha de creación

### Assessment (assessments/models.py)

```python
class Assessment(models.Model):
    MOVEMENT_TYPES = (
        ("flexion", "Flexión"),
        ("extension", "Extensión"),
        ("flexo-extension", "Flexo-Extensión"),
    )

    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    name = models.TextField(max_length=100, null=True)
    description = models.TextField(max_length=500, null=True)
    movement_type = models.CharField(max_length=20, choices=MOVEMENT_TYPES)
```

**Campos:**

- `id`: Identificador único UUID
- `name`: Nombre del tipo de evaluación (ej: "ROM Hombro D")
- `description`: Descripción de la evaluación
- `movement_type`: Tipo de movimiento ('flexion', 'extension', 'flexo-extension')

### PatientAssessment (assessments/models.py)

```python
class PatientAssessment(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    assessment = models.ForeignKey(Assessment, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    angle = models.IntegerField()
    photo = models.ImageField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
```

**Campos:**

- `id`: Identificador único UUID
- `patient`: Paciente evaluado (ForeignKey)
- `assessment`: Tipo de evaluación (ForeignKey)
- `date`: Fecha y hora de evaluación
- `angle`: Ángulo medido en grados
- `photo`: Imagen con landmarks dibujados (opcional)
- `is_active`: Estado activo del registro
- `created_at`: Fecha de creación del registro

---

## 🔧 Configuración Adicional

### Variables de Entorno Recomendadas

Archivo `.env` completo:

```env
# Django
SECRET_KEY=django-insecure-your-secret-key-here
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# Base de Datos
DB_ENGINE=django.db.backends.postgresql
DB_NAME=postgres
DB_USER=postgres
DB_PASSWORD=your_password
DB_HOST=localhost
DB_PORT=5434

# OpenAI
OPENAI_API_KEY=sk-proj-your-api-key

# ESP32 (opcional)
ESP32_URL=http://192.168.1.100/capture

# Media
MEDIA_ROOT=/path/to/media
MEDIA_URL=/media/
```

### Configuración de Producción

Para producción, modificar en `FisioVis/settings.py`:

```python
import os
from pathlib import Path

# Seguridad
DEBUG = False
SECRET_KEY = os.getenv('SECRET_KEY')
ALLOWED_HOSTS = ['tu-dominio.com', 'www.tu-dominio.com']

# HTTPS
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True

# Base de datos
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.getenv('DB_NAME'),
        'USER': os.getenv('DB_USER'),
        'PASSWORD': os.getenv('DB_PASSWORD'),
        'HOST': os.getenv('DB_HOST'),
        'PORT': os.getenv('DB_PORT', '5432'),
    }
}
```

### MediaPipe - Cálculo de Ángulos

La aplicación utiliza MediaPipe Pose para detectar landmarks corporales:

```python
import mediapipe as mp
import numpy as np

def calculate_angle(a, b, c):
    """
    Calcula el ángulo entre tres puntos (a, b, c)
    donde b es el vértice del ángulo
    """
    a = np.array([a.x, a.y])
    b = np.array([b.x, b.y])
    c = np.array([c.x, c.y])

    radians = np.arctan2(c[1] - b[1], c[0] - b[0]) - \
              np.arctan2(a[1] - b[1], a[0] - b[0])
    angle = np.abs(radians * 180.0 / np.pi)

    return angle
```

**Landmarks utilizados:**

- Hombro Derecho: `RIGHT_HIP` → `RIGHT_SHOULDER` → `RIGHT_ELBOW`
- Hombro Izquierdo: `LEFT_HIP` → `LEFT_SHOULDER` → `LEFT_ELBOW`
- Codo Derecho: `RIGHT_HIP` → `RIGHT_ELBOW` → `RIGHT_WRIST`
- Codo Izquierdo: `LEFT_HIP` → `LEFT_ELBOW` → `LEFT_WRIST`

---

## 🧪 Ejemplos de Uso

### 1. Workflow Completo

```bash
# 1. Registrar usuario
POST /users/registro/
{
    "username": "fisio_user",
    "password": "SecurePass123",
    "email": "fisio@example.com"
}

# 2. Iniciar sesión
POST /users/login
{
    "username": "fisio_user",
    "password": "SecurePass123"
}

# 3. Crear paciente
POST /patients/create/
{
    "full_name": "María González",
    "age": 42,
    "sex": "F",
    "phone": "+57 310 555 1234",
    "email": "maria@email.com",
    "work": "Docente",
    "medical_history": "Dolor lumbar crónico"
}

# 4. Realizar evaluación
POST /assessments/eval
{
    "exam_type": "ROM Hombro D"
}

# 5. Guardar evaluación
POST /assessments/save
FormData:
    patient_id: <uuid>
    assessment: "ROM Hombro D"
    angle: 142
    image: <file>

# 6. Generar reporte
GET /reports/create_report/<patient_uuid>
```

### 2. Integración con JavaScript

```javascript
// Evaluar movimiento
async function evaluateMovement(examType) {
  const response = await fetch("/assessments/eval", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ exam_type: examType }),
  });

  const data = await response.json();

  // Mostrar imagen con landmarks
  document.getElementById("result-img").src =
    `data:image/jpeg;base64,${data.image}`;
  document.getElementById("angle").textContent = `${data.angle}°`;
}

// Guardar evaluación
async function saveAssessment(patientId, assessment, angle, imageBlob) {
  const formData = new FormData();
  formData.append("patient_id", patientId);
  formData.append("assessment", assessment);
  formData.append("angle", angle);
  formData.append("image", imageBlob, "assessment.jpg");

  const response = await fetch("/assessments/save", {
    method: "POST",
    body: formData,
  });

  const result = await response.json();
  console.log("Guardado:", result.image_url);
}
```

---

## 📝 Notas Adicionales

- Las imágenes de evaluaciones se almacenan en `/media/`
- Las fuentes personalizadas Roboto para PDFs están en `/static/FisioVis/fonts/`
- La aplicación usa PostgreSQL en producción, SQLite disponible para desarrollo
- Todos los endpoints de pacientes y reportes requieren autenticación
- Los UUIDs son generados automáticamente para todos los modelos
- Las evaluaciones se procesan en tiempo real usando la cámara ESP32

### Dependencias Principales

```
Django==5.2.7
opencv-python==4.12.0.88
mediapipe==0.10.21
openai==2.7.1
fpdf2==2.8.5
psycopg2==2.9.11
pillow==12.0.0
django-crispy-forms==2.4
crispy-tailwind==1.0.3
```

---

## 📄 Licencia

Este proyecto es de código abierto con fines educativos.

---

_Documentación generada el 18 de enero de 2026_
