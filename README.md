# Sistema Inteligente de Reconocimiento Facial y Analítica Predictiva de Asistencia

Proyecto full stack para tesis universitaria.

## Credenciales demo
- Usuario: `admin`
- Contraseña: `admin123`

## 1. Base de datos MySQL/XAMPP
1. Inicie Apache y MySQL en XAMPP.
2. Abra phpMyAdmin.
3. Importe `database/database.sql`.

## 2. Backend
```bash
cd backend
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
copy .env.example .env
python -m uvicorn app.main:app --reload
```

API: http://localhost:8000
Swagger: http://localhost:8000/docs

> Nota: `face_recognition` requiere dlib y compiladores en Windows. Si falla, instale CMake y Visual Studio Build Tools o use Python 3.10.5 con wheels compatibles. El sistema incluye fallback técnico para pruebas, pero para sustentación biométrica real debe instalarse `face_recognition`.

## 3. Frontend
```bash
cd frontend
npm install
npm run dev
```

Frontend: http://localhost:5173

## Funcionalidades incluidas
- Login administrativo con JWT.
- Dashboard moderno con métricas y gráficos.
- CRUD de estudiantes.
- Registro de foto facial.
- Reconocimiento facial mediante cámara web.
- Registro automático de asistencia.
- Reportes PDF y Excel.
- Analítica predictiva de tardanzas y ausencias.
- SQL con 500 estudiantes y registros de asistencia de prueba.
