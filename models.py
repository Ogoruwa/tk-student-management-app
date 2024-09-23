from hashlib import md5
from sqlalchemy import Column, Integer, String

from storage import storage, BaseModel


class Model(BaseModel):
    __abstract__ = True

    id = Column(Integer, primary_key = True, autoincrement = True)

    def save(self, update: bool = False):
        if update:
            storage.update_object(self)
        else:
            storage.create_object(self)
        

    def delete(self):
        storage.delete_object(self)

    @classmethod
    def get(cls, **filters):
        result = storage.get_object(cls, **filters)
        return result



class Student(Model):
    __tablename__ = "sma_students"

    first_name = Column(String(64), nullable = False)
    middle_name = Column(String(64), nullable = False)
    last_name = Column(String(64), nullable = False)
    reg_number = Column(String(16), nullable = False, unique = True)
    gender = Column(String(6), nullable = False)
    department = Column(String(32), nullable = False)


class Employee(Model):
    __tablename__ = "sma_employees"

    username = Column(String(64), nullable = False)
    # Password is md5 hashed before being stored in database
    password = Column(String(255), nullable = False)

    def save(self, session, update: bool = False):
        if not update:
            hashed = md5(self.password.encode()).hexdigest()
            self.password = hashed
        super().save(session, update)
