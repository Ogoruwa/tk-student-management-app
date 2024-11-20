from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.ext.declarative import declarative_base

from settings import get_settings

BaseModel = declarative_base()


class Storage:
    def __init__(self, engine) -> None:
        self._engine = engine
        self._session = sessionmaker(self._engine)

    def create_object(self, obj):
        session = self.create_session()
        
        with self.create_session() as session:
            session.add(obj)
            session.commit()
    

    def get_object(self, model, **filters):
        session = self.create_session()
        
        with self.create_session() as session:
            objs = session.query(model)
            objs = objs.filter_by(**filters)
            session.expunge_all()
        return objs

    
    def update_object(self, obj):
        session = self.create_session()
        
        with self.create_session() as session:
            obj = session.merge(obj)
            session.commit()
            session.expunge_all()


    def delete_object(self, obj):
        # Merge object with instance in session to allow this session to use it
        with self.create_session() as session:
            obj = session.merge(obj)
            session.delete(obj)
            session.commit()


    def create_session(self) -> Session:
        session = self._session()
        return session
    

def setup_storage(backend: str, host: str, database: str, user: str, password: str) -> Storage:
    """Setups up connection to database and returns `Storage` object with active session"""
    if backend == "sqlite":
        url = f"sqlite:///{database}"
    else:
        url = URL(
            backend,
            host = host, 
            database = database,
            username = username,
            password = password,
        )

    engine = create_engine(url, echo=True)    
    BaseModel.metadata.create_all(engine)

    storage = Storage(engine)
    return storage


settings = get_settings()
storage = setup_storage(settings.BACKEND, settings.HOST, settings.DATABASE, settings.USER, settings.PASSWORD)

