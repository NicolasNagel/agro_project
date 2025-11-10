import pandas as pd
import numpy as np
import os
import time
import random

from faker import Faker
from datetime import timedelta, date
from typing import List, Dict, Optional

# Configurações Iniciais
start_time = time.time()
fake = Faker('pt_BR')
random.seed(42)
np.random.seed(42)
FILE_PATH = './dados/'
os.makedirs(FILE_PATH, exist_ok=True)

def gerar_dados_fazendas(
        lista_fazendas: Optional[List] = None,
        tamanho_lote: int = 5_000
    ) -> pd.DataFrame:
    """Gera um lote de dados de cadastro usando Faker e retorna um DataFrame."""
    print(f"    Gerando {tamanho_lote} cadastros...")

    chunk_size = 500
    chunks = []

    for chunk_start in range(0, tamanho_lote, chunk_size):
        chunk_end = min(chunk_start + chunk_size, tamanho_lote)
        chunk_data = []

        for _ in range(chunk_start, chunk_end):

            fazendas_existentes = set(lista_fazendas or [])
            cod_unico = set()

            while True:
                cod_fazenda = f"FA-{random.randint(1, 50_000)}"
                if cod_fazenda not in fazendas_existentes and cod_fazenda not in cod_unico:
                    cod_unico.add(cod_fazenda)
                    break

            data_cadastro = fake.date_between(start_date='-5y', end_date='today')
            inicio_vigencia = min(data_cadastro + timedelta(days=random.randint(30, 45)), date.today())
            fim_vigencia = inicio_vigencia + timedelta(days=(365 * 4))
            if date.today() > fim_vigencia:
                registro_ativo = 1
            else:
                registro_ativo = 2

            chunk_data.append({
                "cod_fazenda": cod_fazenda,
                "nome_fazenda": "Fazenda " + fake.company().replace(',',' '),
                "estado": fake.state_abbr(),
                "municipio": fake.city(),
                "area_total_hectares": random.randint(5, 110),
                "latitude": float(fake.latitude()),
                "longitude": float(fake.longitude()),
                "data_cadastro": data_cadastro,
                "data_inicio_vigencia": inicio_vigencia,
                "data_fim_vigencia": fim_vigencia,
                "registro_ativo": registro_ativo,
            })

        df_chunk = pd.DataFrame(chunk_data)
        df_chunk = df_chunk.drop_duplicates(subset=['cod_fazenda'])

        chunks.append(df_chunk)

    if chunks:
        df = pd.concat(chunks, ignore_index=True)
        df = df.drop_duplicates(subset=['cod_fazenda'])

        print(f"    Gerados {chunk_end}/{tamanho_lote} registros")

        return df.head(tamanho_lote)
    return pd.DataFrame()


def gerar_dados_produtos(lista_produtos: Optional[List] = None) -> pd.DataFrame:
    """Gera dados de cadastro usando Faker e retorna um DataFrame."""
    print(f"    Gerando produtos...")

    produtos = [
        {"cod_produto": f"PROD-1", "nome": "Soja", "categoria": "Grão", "unidade": "ton", "preco_medio": 2800},
        {"cod_produto": f"PROD-2", "nome": "Milho", "categoria": "Grão", "unidade": "ton", "preco_medio": 1600},
        {"cod_produto": f"PROD-3", "nome": "Café Arábica", "categoria": "Bebida", "unidade": "saca", "preco_medio": 1200},
        {"cod_produto": f"PROD-4", "nome": "Café Robusta", "categoria": "Bebida", "unidade": "saca", "preco_medio": 800},
        {"cod_produto": f"PROD-5", "nome": "Trigo", "categoria": "Grão", "unidade": "ton", "preco_medio": 1400},
        {"cod_produto": f"PROD-6", "nome": "Carne Bovina", "categoria": "Proteína", "unidade": "@", "preco_medio": 320},
        {"cod_produto": f"PROD-7", "nome": "Algodão", "categoria": "Fibra", "unidade": "@", "preco_medio": 180},
        {"cod_produto": f"PROD-8", "nome": "Cana-de-açúcar", "categoria": "Industrial", "unidade": "ton", "preco_medio": 180},
    ]

    produtos_existentes = set(lista_produtos or [])
    
    lista_novos_produtos = []

    for p in produtos:
        if p['cod_produto'] in produtos_existentes:
            continue

        lista_novos_produtos.append({
            "cod_produto": p['cod_produto'],
            "nome": p['nome'],
            "categoria": p['categoria'],
            "unidade_medida": p['unidade'],
            "preco_medio_mercado": round(p['preco_medio'] * random.uniform(0.9, 1.1), 2)
        })

    df = pd.DataFrame(lista_novos_produtos)
    return df.head()


def gerar_dados_safras(
        lista_safras: Optional[List] = None,
        df_fazendas: pd.DataFrame = None,
        df_produtos: pd.DataFrame = None,
        tamanho_lote: int = 50_000
    ) -> pd.DataFrame:
    """Gera dados de data usando Faker e retorna um DataFrame"""
    print(f"    Gerando {tamanho_lote} registros de safras...")

    chunk_size = 1_000
    chunks = []

    fazendas = df_fazendas['cod_fazenda'].to_list()
    produtos = df_produtos['cod_produto'].to_list()
    fazendas_dict = dict(zip(df_fazendas['cod_fazenda'], df_fazendas['area_total_hectares']))


    for chunk_start in range(0, tamanho_lote, chunk_size):
        chunk_end = min(chunk_start + chunk_size, tamanho_lote)
        chunk_data = []

        for _ in range(chunk_start, chunk_end):

            safras_existentes = set(lista_safras or [])
            codigo_safras = set()
            while True:
                cod_safra = f'SAF-{random.randint(1, 9_999)}'
                if cod_safra not in safras_existentes and cod_safra not in codigo_safras:
                    codigo_safras.add(cod_safra)
                    break 

            cod_fazenda = random.choice(fazendas)

            data_plantacao = date.today() - timedelta(days=random.randint(365, (365 * 3)))
            data_colheita = data_plantacao + timedelta(days=random.randint(120, 180))
            area_total = fazendas_dict[cod_fazenda]
            area_plantada = round(area_total * random.uniform(0.2, 0.9), 2)

            chunk_data.append({
                'cod_safra': cod_safra,
                'id_fazenda': random.choice(fazendas),
                'id_produto': random.choice(produtos),
                'data_plantacao': data_plantacao,
                'data_colheita': data_colheita,
                'area_plantada': area_plantada,
            })

        df_chunks = pd.DataFrame(chunk_data)
        df_chunks = df_chunks.drop_duplicates(subset=['cod_safra'])

        chunks.append(df_chunks)

        print(f"    Gerados {chunk_end}/{tamanho_lote} registros")

    if chunks:
        df = pd.concat(chunks, ignore_index=True)
        df = df.drop_duplicates(subset=['cod_safra'])
        return df.head(tamanho_lote)
    else:
        return pd.DataFrame()
    

def gerar_dados_insumos(df_safras: pd.DataFrame, tamanho_lote: int = 20_000) -> pd.DataFrame:
    """Gera dados de insumos com Faker e retorna um Dataframe."""

    chunk_size = 500
    chunks = []

    for chunk_start in range(0, tamanho_lote, chunk_size):
        chunk_end = min(chunk_start + chunk_size, tamanho_lote)
        chunk_data = []

        for _ in range(chunk_start, chunk_end):

            tipos_insumos = {
                "Fertilizantes": ['NPK 20-20-20', 'Ureia', 'Superfosfato', 'Calcário'],
                "Defensivo": ['Herbicida', 'Fungicida', 'Inseticida', 'Nematicida'],
                "Irrigação": ['Água', 'Fertirrigação'],
            }

            safras = df_safras['cod_safra'].to_list()
            id_safra = random.choice(safras)
            safra_info = df_safras[df_safras['cod_safra'] == id_safra].iloc[0]

            data_diferenca = (safra_info['data_colheita'] - safra_info['data_plantacao']).days
            data_aplicacao = safra_info['data_plantacao'] + timedelta(days=random.randint(1, data_diferenca))
            tipos_insumo = random.choice(list(tipos_insumos.keys()))
            nome_insumo = random.choice(tipos_insumos[tipos_insumo])
            area_aplicada = round(safra_info['area_plantada'] * random.uniform(0.3, 1), 2)

            if tipos_insumo == 'Fertilizante':
                quantidade = round(area_aplicada * random.uniform(200, 500), 2)
                custo_unitario = random.uniform(2.5, 8.0)
            elif tipos_insumo == 'Defensivo':
                quantidade = round(area_aplicada * random.uniform(1, 5), 2)
                custo_unitario = random.uniform(80, 300)
            else:
                quantidade = round(area_aplicada * random.uniform(1000, 5000), 2)
                custo_unitario = random.uniform(0.5, 2)

            chunk_data.append({
                "id_safra": id_safra,
                "data_aplicacao": data_aplicacao,
                "tipo_insumo": tipos_insumo,
                "nome_insumo": nome_insumo,
                "quantidade_aplicada": quantidade,
                "custo_unitario": round(custo_unitario, 2),
                "area_aplicada": area_aplicada,
            })

        df_chunks = pd.DataFrame(chunk_data)

        chunks.append(df_chunks)

    if chunks:
        df = pd.concat(chunks, ignore_index=True)
        return df.head(tamanho_lote)
    else:
        return pd.DataFrame()
    

def gerar_dados_climaticos(df_fazendas: pd.DataFrame, df_safras: pd.DataFrame) -> pd.DataFrame:
    """Gera dados aleatórios de clima e retorna um DataFrame."""

    data_min = df_safras['data_plantacao'].min()
    data_max = df_safras['data_colheita'].max()

    datas = pd.date_range(start=data_min, end=data_max, freq='D').date.tolist()

    fazendas_ids = df_fazendas['cod_fazenda'].to_list()
    chunk_data = []

    for id_fazenda in fazendas_ids:
        datas_fazendas = random.sample(datas, min(365, len(datas)))

        for data in datas_fazendas:
            chunk_data.append({
                'id_fazenda': random.choice(fazendas_ids),
                "data": data,
                "temperatura_media": round(random.uniform(15, 35), 1),
                "precipitacao": round(random.expovariate(1/20), 1),
                "umidade_relativa": round(random.uniform(40, 95), 1),
                "velocidade_vento": round(random.uniform(0, 30), 1),
                "horas_sol": round(random.uniform(0, 14), 1)
            })

    df = pd.DataFrame(chunk_data)
    return df

if __name__ == '__main__':
    df_fazendas = gerar_dados_fazendas(1_000)
    df_produtos = gerar_dados_produtos()
    df_safras = gerar_dados_safras(df_fazendas, df_produtos, 5_000)
    df_insumos = gerar_dados_insumos(df_safras, 1_000)
    df_clima = gerar_dados_climaticos(df_fazendas, df_safras)

    print(df_fazendas.head(10))
    print(df_produtos.head(10))
    print(df_safras.head(50))
    print(df_insumos.head(50))
    print(df_clima.head(50))