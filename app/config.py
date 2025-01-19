import os

from dotenv import load_dotenv

load_dotenv()


class Config:
    # Se utiliza 'postgresql://usuario:contraseña@host:puerto/nombre_de_la_bd'
    SQLALCHEMY_DATABASE_URI = os.getenv(
        "DATABASE_URL",
        "postgresql://tu_usuario:tu_contraseña@localhost:5432/tu_basedatos",
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.getenv("SECRET_KEY", "mysecretkey")
