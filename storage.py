from sqlalchemy import create_engine, update
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.ext.declarative import declarative_base



BaseModel = declarative_base()


HOST = "localhost"
USER = "tester"
PASSWORD = None
DATABASE = "tester"



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
    

def setup_storage(host: str, database: str, user: str, password: str) -> Storage:
    """Setups up connection to database and returns `Storage` object with active session"""
    password = f":{password}" if password else ""
    url = f"mariadb+mysqlconnector://{user}{password}@{host}/{database}"

    engine = create_engine(url, echo=True)    
    BaseModel.metadata.create_all(engine)

    storage = Storage(engine)
    return storage


storage = setup_storage(HOST, DATABASE, USER, PASSWORD)

