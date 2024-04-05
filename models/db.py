from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base


engine= create_engine(
    "sqlite:///./sql_app.db",
    connect_args={"check_same_thread":False}
)

session_local= sessionmaker(bind=engine)

base= declarative_base()