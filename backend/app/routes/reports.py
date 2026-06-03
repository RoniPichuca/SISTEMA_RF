from fastapi import APIRouter, Depends
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.security import get_current_user
from app.services.report_service import export_excel, export_pdf

router=APIRouter(prefix='/reports', tags=['Reportes'], dependencies=[Depends(get_current_user)])
@router.get('/excel')
def excel(db:Session=Depends(get_db)):
    return StreamingResponse(export_excel(db), media_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet', headers={'Content-Disposition':'attachment; filename=reporte_asistencia.xlsx'})
@router.get('/pdf')
def pdf(db:Session=Depends(get_db)):
    return StreamingResponse(export_pdf(db), media_type='application/pdf', headers={'Content-Disposition':'attachment; filename=reporte_asistencia.pdf'})
