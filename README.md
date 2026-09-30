🎓 Sistema Inteligente de Reconocimiento Facial y Analítica Predictiva de Asistencia

Sistema full stack desarrollado como proyecto académico, orientado a automatizar el registro y análisis de asistencia mediante reconocimiento facial y herramientas de analítica predictiva.

El sistema permite gestionar estudiantes, registrar rostros mediante cámara web, identificar estudiantes y registrar automáticamente su asistencia. También incorpora métricas, reportes y análisis de tardanzas y ausencias.

🚀 Funcionalidades principales

- 🔐 Autenticación administrativa mediante JWT
- 📊 Dashboard con métricas y gráficos
- 👨‍🎓 Gestión CRUD de estudiantes
- 📷 Registro de fotografías faciales
- 👁️ Reconocimiento facial mediante cámara web
- ✅ Registro automático de asistencia
- 📄 Generación de reportes PDF y Excel
- 📈 Analítica predictiva de tardanzas y ausencias
- 🗄️ Base de datos MySQL con datos de prueba

🛠️ Tecnologías utilizadas

Backend

- Python
- FastAPI
- JWT
- Face Recognition

Frontend

- JavaScript
- Node.js / NPM

Visión por computadora

- OpenCV
- face_recognition
- dlib

Base de datos

- MySQL
- XAMPP / phpMyAdmin

Herramientas

- Git
- GitHub
- Uvicorn
- Swagger

📁 Estructura del proyecto

SISTEMA_RF/
├── backend/
├── database/
├── docs/
├── frontend/
├── .gitignore
└── README.md

⚙️ Instalación

1. Base de datos

1. Inicie Apache y MySQL desde XAMPP.
2. Abra phpMyAdmin.
3. Importe:

database/database.sql

2. Backend

cd backend
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
copy .env.example .env
python -m uvicorn app.main:app --reload

API:

http://localhost:8000

Documentación Swagger:

http://localhost:8000/docs

«Nota: "face_recognition" requiere "dlib" y herramientas de compilación en Windows. Para el funcionamiento biométrico real debe instalarse correctamente "face_recognition". El proyecto incluye un fallback técnico destinado a pruebas.»

3. Frontend

cd frontend
npm install
npm run dev

Frontend:

http://localhost:5173

🔑 Credenciales de demostración

Usuario: admin
Contraseña: admin123

Estas credenciales corresponden únicamente al entorno de demostración del proyecto.

🎯 Objetivo del proyecto

Desarrollar una solución tecnológica que permita automatizar el control de asistencia mediante reconocimiento facial y utilizar los registros obtenidos para analizar patrones relacionados con tardanzas y ausencias.

👨‍💻 Autor

Roni Pichuca Mahuanca
Estudiante de Ingeniería de Software con Inteligencia Artificial — SENATI

GitHub: github.com/RoniPichuca
LinkedIn: linkedin.com/in/roni-pichuca-mahuanca-6474a4360
