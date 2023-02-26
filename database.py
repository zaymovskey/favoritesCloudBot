from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

from settings import config

engine = create_engine(config.database_url)
Base = declarative_base()
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()
