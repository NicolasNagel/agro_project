import pandas as pd

from src.database.db_connection import Base, engine
from src.utils.data_mapping import DATA_MAPPING

# Criação das Tabelas no Banco de Dados
Base.metadata.create_all(bind=engine)

data_frames = {}
ordem_tabelas = ['Fazendas', 'Produtos', 'Safras', 'Insumos', 'Clima']
for nome in ordem_tabelas:
    for grupo in DATA_MAPPING:
        for chave, dados in grupo.items():
            if chave != nome:
                continue
            
            nome_tabela = dados['Nome Tabela']
            funcao = dados['Função']
            schema = dados['Schema']
            tabela = dados['Tabela']

            try:
                with engine.begin() as conn:
                    try:
                        dado_existente = pd.read_sql_table(nome_tabela, conn)
                    except Exception as e:
                        dado_existente = pd.DataFrame()

                    if not dado_existente.empty:
                        if nome == 'Fazendas':
                            codigos_existentes = dado_existente['cod_fazenda'].tolist()
                            novos_dados = funcao(codigos_existentes)

                        elif nome == 'Produtos':
                            codigos_existentes = dado_existente['cod_produto'].tolist()
                            novos_dados = funcao(codigos_existentes)

                        elif nome == 'Safras':
                            codigos_existentes = dado_existente['cod_safra'].tolist()
                            novos_dados = funcao(
                                codigos_existentes,
                                df_fazendas=data_frames['Fazendas'],
                                df_produtos=data_frames['Produtos']
                            )

                        elif nome == 'Insumos':
                            novos_dados = funcao(
                                df_safras = data_frames['Safras']
                            )

                        elif nome == 'Clima':
                            novos_dados = funcao(
                                df_fazendas = data_frames['Fazendas'],
                                df_safras = data_frames['Safras']
                            )

                        if not novos_dados.empty:
                            novos_dados.to_sql(nome_tabela, conn, if_exists='append', index=False)
                            print(f"{len(novos_dados)} inseridos em {nome_tabela}")
                            data_frames[nome] = pd.concat([dado_existente, novos_dados], ignore_index=True)
                        else:
                            print(f"Nenhum novo registro para {nome_tabela}")
                            data_frames[nome] = dado_existente.copy()
                    else:
                        print(f"{nome_tabela} está vazia, criando novos dados...")

                        if nome == 'Fazendas':
                            novos_dados = funcao()
                        elif nome == 'Produtos':
                            novos_dados = funcao()
                        elif nome == 'Safras':
                            novos_dados = funcao(
                                df_fazendas = data_frames['Fazendas'],
                                df_produtos = data_frames['Produtos']
                            )
                        elif nome == 'Insumos':
                            novos_dados = funcao(
                                df_safras = data_frames['Safras']
                            )
                        else:
                            novos_dados = funcao(
                                df_fazendas = data_frames['Fazendas'],
                                df_safras = data_frames['Safras']
                            )

                        novos_dados.to_sql(nome_tabela, conn, if_exists='append', index=False)
                        data_frames[nome] = novos_dados
                        print(f"{len(novos_dados)} salvos em {nome_tabela}")

            except Exception as e:
                print(f"Erro ao processar {nome_tabela}: {e}")