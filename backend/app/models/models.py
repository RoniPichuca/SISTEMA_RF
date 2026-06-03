from sqlalchemy import Column, Integer, String, Date, DateTime, Time, Boolean, ForeignKey, Text, Float, LargeBinary, func
from sqlalchemy.orm import relationship
from app.core.database import Base

class Usuario(Base):
    __tablename__ = "usuarios"
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(120), nullable=False)
    usuario = Column(String(80), unique=True, index=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    rol = Column(String(50), default="ADMIN")
    activo = Column(Boolean, default=True)
    creado_en = Column(DateTime, server_default=func.now())

class Estudiante(Base):
    __tablename__ = "estudiantes"
    id = Column(Integer, primary_key=True, index=True)
    codigo = Column(String(30), unique=True, index=True, nullable=False)
    dni = Column(String(12), unique=True, nullable=True)
    nombres = Column(String(120), nullable=False)
    apellidos = Column(String(120), nullable=False)
    grado = Column(String(20), nullable=False)
    seccion = Column(String(10), nullable=False)
    email = Column(String(120), nullable=True)
    telefono = Column(String(30), nullable=True)
    foto_url = Column(String(255), nullable=True)
    activo = Column(Boolean, default=True)
    creado_en = Column(DateTime, server_default=func.now())
    asistencias = relationship("Asistencia", back_populates="estudiante", cascade="all, delete-orphan")
    embedding = relationship("EmbeddingFacial", back_populates="estudiante", uselist=False, cascade="all, delete-orphan")

class Asistencia(Base):
    __tablename__ = "asistencia"
    id = Column(Integer, primary_key=True, index=True)
    estudiante_id = Column(Integer, ForeignKey("estudiantes.id", ondelete="CASCADE"), nullable=False)
    fecha = Column(Date, nullable=False, index=True)
    hora = Column(Time, nullable=False)
    estado = Column(String(30), nullable=False)
    confianza = Column(Float, default=0.0)
    metodo = Column(String(50), default="FACIAL")
    creado_en = Column(DateTime, server_default=func.now())
    estudiante = relationship("Estudiante", back_populates="asistencias")

class EmbeddingFacial(Base):
    __tablename__ = "embeddings_faciales"
    id = Column(Integer, primary_key=True)
    estudiante_id = Column(Integer, ForeignKey("estudiantes.id", ondelete="CASCADE"), unique=True, nullable=False)
    vector = Column(LargeBinary, nullable=True)
    vector_json = Column(Text, nullable=True)
    modelo = Column(String(80), default="face_recognition_resnet")
    precision_estimada = Column(Float, default=0.97)
    actualizado_en = Column(DateTime, server_default=func.now(), onupdate=func.now())
    estudiante = relationship("Estudiante", back_populates="embedding")

class Reporte(Base):
    __tablename__ = "reportes"
    id = Column(Integer, primary_key=True)
    tipo = Column(String(50), nullable=False)
    descripcion = Column(Text, nullable=True)
    ruta_archivo = Column(String(255), nullable=True)
    generado_en = Column(DateTime, server_default=func.now())
