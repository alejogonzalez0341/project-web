from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

from dotenv import dotenv_values

config_env= dotenv_values(".env")


USER_POSTGRE= config_env["USER_POSTGRE"]
PASSWORD_POSTGRE= config_env["PASSWORD_POSTGRE"]
HOST_POSTGRE= config_env["HOST_POSTGRE"]
PORT_POSTGRE= config_env["PORT_POSTGRE"]
DB_POSTGRE= config_env["DB_POSTGRE"] 

engine= create_engine(
    f"postgresql://{USER_POSTGRE}:{PASSWORD_POSTGRE}@{HOST_POSTGRE}:{PORT_POSTGRE}/{DB_POSTGRE}"
    # "sqlite:///./db.db"
)

session_local= sessionmaker(autocommit=False, autoflush=False ,bind=engine)

base= declarative_base()