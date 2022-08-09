import os
from dotenv import load_dotenv
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy import Column, ForeignKey, Integer, String, create_engine, Date

load_dotenv()
Base = declarative_base()

class Licitacoes(Base):
  __tablename__ = 'licitacoes'
  id = Column(Integer(), primary_key=True)
  orgao = Column(String(1000))
  titulo = Column(String(1000))
  estado = Column(String(10))
  cidade = Column(String(50))
  objeto = Column(String(1000000))
  datas = relationship('Datas', backref='licitacoes')

class Datas(Base):
  __tablename__ = 'datas'
  id = Column(Integer(), primary_key=True)
  licitacao_id = Column(Integer(), ForeignKey('licitacoes.id'))
  label = Column(String(200))
  evento = Column(String(200)) 
  orientacao = Column(String(200))
  data = Column(Date)
  fonte = Column(String(10000))

engine =  create_engine(os.getenv('DATABASE_URL'), echo=False)

Base.metadata.create_all(engine)
Session = sessionmaker(engine)
