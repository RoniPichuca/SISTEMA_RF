from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.security import get_current_user
from app.services.analytics_service import dashboard_stats, chart_daily, predictive

router=APIRouter(prefix='/dashboard', tags=['Dashboard'], dependencies=[Depends(get_current_user)])
@router.get('/stats')
def stats(db:Session=Depends(get_db)): return dashboard_stats(db)
@router.get('/chart')
def chart(db:Session=Depends(get_db)): return chart_daily(db)
@router.get('/predictive')
def pred(db:Session=Depends(get_db)): return predictive(db)
