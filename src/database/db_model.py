from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from src.database.db_connection import Base

class FarmTable(Base):
    __tablename__ = 'raw_fazendas'

    id = Column(Integer, primary_key=True, autoincrement=True)
    cod_fazenda =  Column(String, unique=True, nullable=False)
    nome_fazenda = Column(String, nullable=False)
    estado = Column(String)
    municipio = Column(String)
    area_total_hectares = Column(Float)
    latitude = Column(String)
    longitude = Column(String)
    data_cadastro = Column(DateTime)
    data_inicio_vigencia = Column(DateTime)
    data_fim_vigencia = Column(DateTime)
    registro_ativo = Column(Integer)
    dt_insercao = Column(DateTime, server_default=func.now())

    safras = relationship("SafrasTable", back_populates="fazendas")
    clima = relationship("ClimaTable", back_populates='fazendas')

class ProductTable(Base):
    __tablename__ = 'raw_produtos'

    id = Column(Integer, primary_key=True, autoincrement=True)
    cod_produto = Column(String, unique=True, nullable=False)
    nome = Column(String, nullable=False)
    categoria = Column(String)
    unidade_medida = Column(String)
    preco_medio_mercado = Column(Float)
    dt_insercao = Column(DateTime, server_default=func.now())

    safras = relationship("SafrasTable", back_populates="produtos")

class SafrasTable(Base):
    __tablename__ = 'raw_safras'

    id = Column(Integer, primary_key=True, autoincrement=True)
    cod_safra = Column(String, unique=True, nullable=False)
    id_fazenda = Column(String, ForeignKey('raw_fazendas.cod_fazenda'), nullable=False)
    id_produto = Column(String, ForeignKey('raw_produtos.cod_produto'), nullable=False)
    data_plantacao = Column(DateTime, nullable=False)
    data_colheita = Column(DateTime, nullable=False)
    area_plantada = Column(Float, nullable=False)
    dt_insercao = Column(DateTime, server_default=func.now())

    fazendas = relationship("FarmTable", back_populates="safras")
    produtos = relationship("ProductTable", back_populates="safras")
    insumos = relationship("InsumosTable", back_populates='safras')

class InsumosTable(Base):
    __tablename__ = 'raw_insumos'

    id = Column(Integer, primary_key=True, autoincrement=True)
    id_safra = Column(String, ForeignKey('raw_safras.cod_safra'), nullable=False)
    data_aplicacao = Column(DateTime)
    tipo_insumo = Column(String)
    nome_insumo = Column(String)
    quantidade_aplicada = Column(Float)
    custo_unitario = Column(Float)
    area_aplicada = Column(Float)
    dt_insercao = Column(DateTime, server_default=func.now())

    safras = relationship("SafrasTable", back_populates="insumos")

class ClimaTable(Base):
    __tablename__ = 'raw_clima'

    id = Column(Integer, primary_key=True, autoincrement=True)
    id_fazenda = Column(String, ForeignKey('raw_fazendas.cod_fazenda'), nullable=False)
    data = Column(DateTime, nullable=False)
    temperatura_media = Column(Float, nullable=False)
    precipitacao = Column(Float, nullable=False)
    umidade_relativa = Column(Float, nullable=False)
    velocidade_vento = Column(Float, nullable=False)
    horas_sol = Column(Float, nullable=False)
    dt_insercao = Column(DateTime, server_default=func.now())

    fazendas = relationship("FarmTable", back_populates='clima')