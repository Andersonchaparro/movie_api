import os
from sqlalchemy import create_engine
from sqlalchemy.orm.session import sessionmaker
from sqlalchemy.ext.declarative import declarative_base


db_name = "../movie_db.sqlite"

# leemos todo el directorio donde se encuentra la BD
base_dir = os.path.dirname(os.path.realpath(__file__))

#creamos la URL de la BD
db_url = f'sqlite:///{os.path.join(base_dir, db_name)}'

# el engine espara conectarnos a la BD y administrarla
engine = create_engine(db_url, echo=True)

# coneccion a la BD
Session = sessionmaker(bind=engine)

Base = declarative_base()