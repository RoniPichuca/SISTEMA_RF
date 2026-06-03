from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    APP_NAME: str = "Sistema Inteligente de Reconocimiento Facial"
    SECRET_KEY: str = "cambia_esta_clave_super_segura"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 480
    MYSQL_HOST: str = "localhost"
    MYSQL_PORT: int = 3306
    MYSQL_USER: str = "root"
    MYSQL_PASSWORD: str = ""
    MYSQL_DATABASE: str = "sistema_asistencia_ia"
    CORS_ORIGINS: str = "http://localhost:5173,http://127.0.0.1:5173"
    LATE_LIMIT: str = "08:00:00"
    FACE_TOLERANCE: float = 0.48

    @property
    def database_url(self) -> str:
        return f"mysql+pymysql://{self.MYSQL_USER}:{self.MYSQL_PASSWORD}@{self.MYSQL_HOST}:{self.MYSQL_PORT}/{self.MYSQL_DATABASE}?charset=utf8mb4"

    class Config:
        env_file = ".env"
        extra = "ignore"

settings = Settings()
