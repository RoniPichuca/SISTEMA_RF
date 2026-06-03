from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from app.core.config import settings
from app.core.database import Base, engine
from app.routes import auth, students, attendance, dashboard, reports

Base.metadata.create_all(bind=engine)
app = FastAPI(title=settings.APP_NAME, version='1.0.0')
origins=[x.strip() for x in settings.CORS_ORIGINS.split(',')]
app.add_middleware(CORSMiddleware, allow_origins=origins, allow_credentials=True, allow_methods=['*'], allow_headers=['*'])
app.mount('/uploads', StaticFiles(directory='uploads'), name='uploads')
app.include_router(auth.router, prefix='/api')
app.include_router(students.router, prefix='/api')
app.include_router(attendance.router, prefix='/api')
app.include_router(dashboard.router, prefix='/api')
app.include_router(reports.router, prefix='/api')

@app.get('/')
def root(): return {'message':'API Sistema Inteligente de Reconocimiento Facial activa'}
