from pydantic import BaseModel, EmailStr
from datetime import date, time, datetime
from typing import Optional

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

class UsuarioOut(BaseModel):
    id: int
    nombre: str
    usuario: str
    rol: str
    class Config: from_attributes = True

class EstudianteBase(BaseModel):
    codigo: str
    dni: Optional[str] = None
    nombres: str
    apellidos: str
    grado: str
    seccion: str
    email: Optional[str] = None
    telefono: Optional[str] = None

class EstudianteCreate(EstudianteBase): pass
class EstudianteUpdate(BaseModel):
    codigo: Optional[str] = None
    dni: Optional[str] = None
    nombres: Optional[str] = None
    apellidos: Optional[str] = None
    grado: Optional[str] = None
    seccion: Optional[str] = None
    email: Optional[str] = None
    telefono: Optional[str] = None
    activo: Optional[bool] = None

class EstudianteOut(EstudianteBase):
    id: int
    foto_url: Optional[str] = None
    activo: bool
    creado_en: datetime
    class Config: from_attributes = True

class AsistenciaOut(BaseModel):
    id: int
    estudiante_id: int
    fecha: date
    hora: time
    estado: str
    confianza: float
    metodo: str
    estudiante: Optional[EstudianteOut] = None
    class Config: from_attributes = True
