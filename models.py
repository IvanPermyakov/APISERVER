from sqlalchemy import Column, BIGINT, CHAR, DATE, Sequence, INTEGER
from sqlalchemy.orm import declarative_base
from datetime import date
from dadata import Dadata
import os
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy import create_engine
from sqlalchemy.exc import SQLAlchemyError
import re

TOKEN = os.environ['TOKEN'] 
SECRET = os.environ['SECRET'] 
CONNECT = os.environ['CONNECT']

Base = declarative_base()

class connectionDB():
    def __init__(self):
        self.engine = self.connectToDBSqlAlc()
        self.sessionMake = sessionmaker(bind=self.engine)
        self.sessionConfig = self.sessionMake.configure(bind=self.engine)
        self.session = Session(self.engine)

    def connectToDBSqlAlc(self):
        engine = create_engine(CONNECT)
        return engine.connect()

class UserData(connectionDB, Base):
    __tablename__ = 'UserData'
    #ID задается в БД с помощью сиквенса с началом в 100000000000
    user_id = Column(BIGINT, Sequence("sequserdataid"), primary_key=True)
    name = Column(CHAR(50), nullable=False)
    surname = Column(CHAR(50), nullable=False)
    phone_number = Column(CHAR(12), nullable=False)
    country = Column(CHAR(50), nullable=False)
    date_created_ = Column('date_created ', DATE, nullable=False)
    date_modified_ = Column('date_modified ', DATE, nullable=False)
    patronymic_ = Column('patronymic ', CHAR(50))
    email_ = Column('email ', CHAR(50))
    country_code = Column(INTEGER)

    def __init__(self, payload: dict):
        super().__init__()
        self._payload = payload
        self.name = payload['name']
        self.surname = payload['surname']
        self.phone_number = payload['phone_number']
        self.country = payload['country']
        self.country_code = self.initCountry()
        self.date_created_ = self.initDateCreate()
        self.date_modified_ = date.today()
        self.patronymic_ = payload['patronymic_']
        self.email_ = payload['email_']

    def examination(self):
        if len(self._payload['name']) > 50:
            return  'Имя не может быть больше 50 символов'
        elif len(self._payload['surname']) > 50:
            return  'Фамилия не может быть больше 50 символов'
        elif len(self._payload['country']) > 50:
            return  'Страна не может быть больше 50 символов'
        elif len(self._payload['patronymic_']) > 50:
            return  'Отчество не может быть больше 50 символов'
        elif self.session.query(UserData.phone_number).filter(UserData.phone_number == self._payload['phone_number']).first() is not None:
            return 'Такой номер телефона уже существует'
        elif not re.match("^[А-Яа-я -]?", self._payload['name']):
            return 'Ваше имя должно содержать только кириллицу, пробел и тире'
        elif not re.match("^[А-Яа-я -]?", self._payload['surname']):
            return 'Ваше Фамилия должно содержать только кириллицу, пробел и тире'
        elif not re.match("^[А-Яа-я -]?", self._payload['patronymic_']):
            return 'Ваше Отчество должно содержать только кириллицу, пробел и тире'
        elif not re.match("^[А-Яа-я -]?", self._payload['country']):
            return 'Ваша Страна должно содержать только кириллицу, пробел и тире'
        else:
            return None

    def initCountry(self):
        client = Dadata(TOKEN,SECRET)
        result = client.suggest("country", self._payload['country'])[0]
        return result['data']['code']
    
    def initDateCreate(self):
        todayDate = self.session.query(UserData.date_created_).filter(UserData.phone_number == self._payload['phone_number']).first()
        if todayDate == None:
            return date.today()
        else:
            todayDate
    
    def addData(self):
        self.session.add(self)
        self.session.commit()
        return 'данные успешно добавлены'

def getData(number):
    session = connectionDB().session
    res = session.query(UserData.name, UserData.surname, UserData.patronymic_, UserData.phone_number, UserData.email_, UserData.country, UserData.country_code).filter(UserData.phone_number == number).first()
    if res is None:
        return None
    return res

def delData(number):
    try:
        session = connectionDB().session
        res = session.query(UserData).filter(UserData.phone_number == number).one()
        session.delete(res)
        session.commit()
    except SQLAlchemyError:
        return None
    else:
        return 'Данные удалены'


