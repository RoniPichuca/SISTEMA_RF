from pathlib import Path
from io import BytesIO
import pandas as pd
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from sqlalchemy.orm import Session
from app.models.models import Asistencia

def asistencia_dataframe(db: Session):
    rows = db.query(Asistencia).order_by(Asistencia.fecha.desc(), Asistencia.hora.desc()).all()
    return pd.DataFrame([{
        'codigo': r.estudiante.codigo, 'estudiante': f'{r.estudiante.nombres} {r.estudiante.apellidos}',
        'grado': r.estudiante.grado, 'seccion': r.estudiante.seccion, 'fecha': str(r.fecha),
        'hora': str(r.hora), 'estado': r.estado, 'confianza': r.confianza
    } for r in rows])

def export_excel(db: Session):
    output = BytesIO()
    df = asistencia_dataframe(db)
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, sheet_name='Asistencia')
    output.seek(0)
    return output

def export_pdf(db: Session):
    output = BytesIO()
    c = canvas.Canvas(output, pagesize=A4)
    w,h=A4
    c.setFont('Helvetica-Bold', 14); c.drawString(40,h-45,'Reporte de Asistencia - Sistema IA')
    c.setFont('Helvetica', 9)
    y=h-75
    for r in db.query(Asistencia).order_by(Asistencia.fecha.desc()).limit(35):
        line=f'{r.fecha} {r.hora} | {r.estudiante.codigo} | {r.estudiante.nombres} {r.estudiante.apellidos} | {r.estado} | {round(r.confianza*100,1)}%'
        c.drawString(40,y,line[:120]); y-=16
        if y<50: c.showPage(); y=h-50; c.setFont('Helvetica',9)
    c.save(); output.seek(0); return output
