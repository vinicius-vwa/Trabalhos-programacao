import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from models import Base

load_dotenv()

def get_engine(tipo_bd: str):
    if tipo_bd == "sqlite":
        return create_engine("sqlite:///banco_local.db", echo=False)
    elif tipo_bd == "mysql":
        host = os.getenv("MYSQL_HOST")
        user = os.getenv("MYSQL_USER")
        senha = os.getenv("MYSQL_PASSWORD")
        porta = os.getenv("MYSQL_PORT", "12960")
        db = os.getenv("MYSQL_DATABASE", "defaultdb")
        
        url = f"mysql+pymysql://{user}:{senha}@{host}:{porta}/{db}?ssl=true"
        return create_engine(url, echo=False)
    else:
        raise ValueError("Tipo de banco inválido")

def init_db(engine):
    Base.metadata.create_all(engine)
