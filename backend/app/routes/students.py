from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.orm import Session
from sqlalchemy import or_
import cv2, numpy as np
from app.core.database import get_db
from app.core.security import get_current_user
from app.models.models import Estudiante, EmbeddingFacial
from app.schemas.schemas import EstudianteCreate, EstudianteUpdate, EstudianteOut
from app.services.face_service import image_to_embedding, serialize_embedding, save_face_image

router = APIRouter(prefix='/students', tags=['Estudiantes'], dependencies=[Depends(get_current_user)])

@router.get('', response_model=list[EstudianteOut])
def list_students(q: str = '', db: Session = Depends(get_db)):
    query = db.query(Estudiante)
    if q:
        like=f'%{q}%'; query=query.filter(or_(Estudiante.codigo.like(like), Estudiante.nombres.like(like), Estudiante.apellidos.like(like), Estudiante.dni.like(like)))
    return query.order_by(Estudiante.id.desc()).limit(1000).all()

@router.post('', response_model=EstudianteOut)
def create_student(data: EstudianteCreate, db: Session = Depends(get_db)):
    obj=Estudiante(**data.model_dump()); db.add(obj); db.commit(); db.refresh(obj); return obj

@router.put('/{student_id}', response_model=EstudianteOut)
def update_student(student_id:int, data: EstudianteUpdate, db: Session = Depends(get_db)):
    obj=db.get(Estudiante, student_id)
    if not obj: raise HTTPException(404,'Estudiante no encontrado')
    for k,v in data.model_dump(exclude_unset=True).items(): setattr(obj,k,v)
    db.commit(); db.refresh(obj); return obj

@router.delete('/{student_id}')
def delete_student(student_id:int, db: Session = Depends(get_db)):
    obj=db.get(Estudiante, student_id)
    if not obj: raise HTTPException(404,'Estudiante no encontrado')
    db.delete(obj); db.commit(); return {'ok': True}

@router.post('/{student_id}/face')
def upload_face(student_id:int, file: UploadFile = File(...), db: Session = Depends(get_db)):
    student=db.get(Estudiante, student_id)
    if not student: raise HTTPException(404,'Estudiante no encontrado')
    data=np.frombuffer(file.file.read(), np.uint8)
    img=cv2.imdecode(data, cv2.IMREAD_COLOR)
    try: vec=image_to_embedding(img)
    except ValueError as e: raise HTTPException(400, str(e))
    path=save_face_image(student_id,img); student.foto_url=path
    emb=db.query(EmbeddingFacial).filter_by(estudiante_id=student_id).first() or EmbeddingFacial(estudiante_id=student_id)
    emb.vector_json=serialize_embedding(vec); db.add(emb); db.commit()
    return {'message':'Rostro registrado correctamente','foto_url': path}
