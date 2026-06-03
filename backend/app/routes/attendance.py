from datetime import date, datetime
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session, joinedload
from app.core.database import get_db
from app.core.security import get_current_user
from app.core.config import settings
from app.models.models import Asistencia, Estudiante, EmbeddingFacial
from app.schemas.schemas import AsistenciaOut
from app.services.face_service import decode_base64_image, image_to_embedding, deserialize_embedding, compare_embeddings

router=APIRouter(prefix='/attendance', tags=['Asistencia'], dependencies=[Depends(get_current_user)])

@router.get('', response_model=list[AsistenciaOut])
def list_attendance(db:Session=Depends(get_db)):
    return db.query(Asistencia).options(joinedload(Asistencia.estudiante)).order_by(Asistencia.fecha.desc(), Asistencia.hora.desc()).limit(500).all()

@router.post('/recognize')
def recognize(payload: dict, db:Session=Depends(get_db)):
    image_data=payload.get('image')
    if not image_data: raise HTTPException(400,'Imagen requerida')
    img=decode_base64_image(image_data)
    try: candidate=image_to_embedding(img)
    except ValueError as e: raise HTTPException(400, str(e))
    rows=db.query(EmbeddingFacial).join(Estudiante).filter(Estudiante.activo==True, EmbeddingFacial.vector_json.isnot(None)).all()
    known=[{'student_id': r.estudiante_id, 'embedding': deserialize_embedding(r.vector_json)} for r in rows]
    match=compare_embeddings(candidate, known, settings.FACE_TOLERANCE)
    if not match: return {'recognized': False, 'message': 'Rostro no reconocido'}
    student=db.get(Estudiante, match['student_id'])
    now=datetime.now(); limit=datetime.strptime(settings.LATE_LIMIT,'%H:%M:%S').time()
    estado='PRESENTE' if now.time() <= limit else 'TARDANZA'
    existing=db.query(Asistencia).filter_by(estudiante_id=student.id, fecha=now.date()).first()
    if existing:
        return {'recognized': True, 'already_registered': True, 'student': {'id':student.id,'codigo':student.codigo,'nombres':student.nombres,'apellidos':student.apellidos}, 'attendance_id': existing.id, 'confidence': match['confidence']}
    att=Asistencia(estudiante_id=student.id, fecha=now.date(), hora=now.time().replace(microsecond=0), estado=estado, confianza=match['confidence'], metodo='FACIAL')
    db.add(att); db.commit(); db.refresh(att)
    return {'recognized': True, 'already_registered': False, 'student': {'id':student.id,'codigo':student.codigo,'nombres':student.nombres,'apellidos':student.apellidos}, 'estado': estado, 'attendance_id': att.id, 'confidence': match['confidence']}
