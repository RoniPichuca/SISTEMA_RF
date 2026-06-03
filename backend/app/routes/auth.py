from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.config import settings
from app.core.security import verify_password, create_access_token, get_current_user
from app.models.models import Usuario
from app.schemas.schemas import Token, UsuarioOut

router = APIRouter(prefix='/auth', tags=['Autenticación'])

@router.post('/login', response_model=Token)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(Usuario).filter(Usuario.usuario == form_data.username, Usuario.activo == True).first()
    if not user or not verify_password(form_data.password, user.password_hash):
        raise HTTPException(status_code=401, detail='Usuario o contraseña incorrectos')
    token = create_access_token({'sub': user.usuario}, timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES))
    return {'access_token': token, 'token_type': 'bearer'}

@router.get('/me', response_model=UsuarioOut)
def me(user: Usuario = Depends(get_current_user)):
    return user
