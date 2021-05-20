from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import declarative_base

engine = create_engine('mysql+pymysql://database:database@192.168.122.76:3306/webssh')


Session = sessionmaker(bind=engine)
session = Session()
# declarative base class
Base = declarative_base()


class logs(Base):
    __tablename__ = 'logs'

    id = Column(Integer,primary_key=True)
    source_ip = Column(String(100))
    ssh_ip = Column(String(100))
    time = Column(String(100))

class activeusers(Base):
    __tablename__ = 'activeusers'

    id = Column(Integer,primary_key=True)
    source_ip = Column(String(100))
    ssh_ip = Column(String(100))
    time = Column(String(100))

#Base.metadata.create_all(engine)
