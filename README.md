# 🌾 Projeto de Engenharia de Dados - Pipeline Agrícola com dbt e Airflow

Este projeto implementa um **pipeline completo de Engenharia de Dados** voltado à análise do **setor agrícola**, integrando as ferramentas **Python**, **PostgreSQL**, **Apache Airflow**, **dbt-core** e **Docker (Astronomer)**.  

O objetivo é construir um **ecossistema de dados confiável**, desde a **extração dos dados brutos (RAW)** até a **camada analítica (MART)**, utilizando **boas práticas de modelagem, versionamento e automação**.

---

## 🧭 Arquitetura do Projeto

A arquitetura segue o padrão **Medallion Architecture**, dividido em quatro camadas:


| Camada | Descrição | Exemplos |
|--------|------------|-----------|
| **RAW** | Camada bruta. Armazena dados extraídos diretamente pela pipeline de ETL. | `raw_fazendas`, `raw_produtos`, `raw_safras`, `raw_insumos`, `raw_clima` |
| **STAGING (STG)** | Padroniza colunas, remove inconsistências e adiciona colunas de controle (`etl_inserted_at`). | `stg_fazendas`, `stg_produtos`, `stg_safras`, `stg_insumos`, `stg_clima` |
| **INTERMEDIATE (INT)** | Constrói tabelas de **dimensão** e **fato**, unificando dados de diferentes origens. | `int_dim_fazendas`, `int_dim_produto`, `int_fact_insumos`, `int_fact_safras` |
| **MART (Analytics)** | Consolida as informações de negócio para análise e BI. | `mart_custos_por_safra`, `mart_safras_enriched` |

---

## 🧩 Estrutura de Pastas

models/
├── raw/ → Dados brutos extraídos pela pipeline ETL
│
├── staging/ → Limpeza e padronização de dados
│ ├── stg_fazendas.sql
│ ├── stg_produtos.sql
│ ├── stg_safras.sql
│ ├── stg_insumos.sql
│ └── stg_clima.sql
│
├── intermediate/ → Modelos intermediários (dimensões e fatos)
│ ├── dim/
│ │ ├── int_dim_fazendas.sql
│ │ └── int_dim_produto.sql
│ └── fact/
│ ├── int_fact_insumos.sql
│ └── int_fact_safras.sql
│
└── mart/
└── analytics/
├── mart_custos_por_safra.sql
└── mart_safras_enriched.sql


---

## 🧱 Camada RAW

Contém os dados originais do sistema agrícola:

- `raw_fazendas` → Cadastro das fazendas  
- `raw_produtos` → Produtos cultivados  
- `raw_safras` → Informações de plantio e colheita  
- `raw_insumos` → Aplicações de insumos e custos  
- `raw_clima` → Dados climáticos diários por fazenda  

Cada tabela é criada automaticamente pela pipeline de ETL, e validada com **testes de integridade (unique, not_null)**.

---

## 🧹 Camada STAGING

Realiza o **tratamento e padronização** dos dados provenientes da RAW.

Exemplo de melhorias:
- Renomeação de colunas (`nome_fazenda` → `nm_fazenda`, `data_plantacao` → `dt_plantacao`)  
- Conversão de tipos de dados  
- Inclusão de coluna de controle (`etl_inserted_at`)  

Tabelas:
- `stg_fazendas`
- `stg_produtos`
- `stg_safras`
- `stg_insumos`
- `stg_clima`

---

## 🧮 Camada INTERMEDIATE

Dividida em **dimensões (DIM)** e **fatos (FACT)**:

### 📘 Dimensões (`dim/`)
- `int_dim_fazendas.sql` → Dados únicos de fazendas  
- `int_dim_produto.sql` → Catálogo de produtos  

### 📗 Fatos (`fact/`)
- `int_fact_insumos.sql` → Custos e aplicações de insumos por safra  
- `int_fact_safras.sql` → Dados consolidados de plantio, colheita e produtividade  

Essas tabelas formam a **base para o modelo estrela (Star Schema)**.

---

## 📊 Camada MART (Analytics)

Camada final voltada à **análise e tomada de decisão**.

### `mart_custos_por_safra.sql`
- Calcula **custo total e médio** de insumos por safra  
- Agrega informações de produção e lucro estimado  

### `mart_safras_enriched.sql`
- Enriquecimento das safras com variáveis climáticas e de produtividade  
- Permite análises preditivas (ex: impacto do clima sobre a produção)

---

## ⚙️ Tecnologias Utilizadas

| Ferramenta | Finalidade |
|-------------|-------------|
| **Python** | Geração, extração e carg

---

## 🧱 Camada RAW

Contém os dados originais do sistema agrícola:

- `raw_fazendas` → Cadastro das fazendas  
- `raw_produtos` → Produtos cultivados  
- `raw_safras` → Informações de plantio e colheita  
- `raw_insumos` → Aplicações de insumos e custos  
- `raw_clima` → Dados climáticos diários por fazenda  

Cada tabela é criada automaticamente pela pipeline de ETL, e validada com **testes de integridade (unique, not_null)**.

---

## 🧹 Camada STAGING

Realiza o **tratamento e padronização** dos dados provenientes da RAW.

Exemplo de melhorias:
- Renomeação de colunas (`nome_fazenda` → `nm_fazenda`, `data_plantacao` → `dt_plantacao`)  
- Conversão de tipos de dados  
- Inclusão de coluna de controle (`etl_inserted_at`)  

Tabelas:
- `stg_fazendas`
- `stg_produtos`
- `stg_safras`
- `stg_insumos`
- `stg_clima`

---

## 🧮 Camada INTERMEDIATE

Dividida em **dimensões (DIM)** e **fatos (FACT)**:

### 📘 Dimensões (`dim/`)
- `int_dim_fazendas.sql` → Dados únicos de fazendas  
- `int_dim_produto.sql` → Catálogo de produtos  

### 📗 Fatos (`fact/`)
- `int_fact_insumos.sql` → Custos e aplicações de insumos por safra  
- `int_fact_safras.sql` → Dados consolidados de plantio, colheita e produtividade  

Essas tabelas formam a **base para o modelo estrela (Star Schema)**.

---

## 📊 Camada MART (Analytics)

Camada final voltada à **análise e tomada de decisão**.

### `mart_custos_por_safra.sql`
- Calcula **custo total e médio** de insumos por safra  
- Agrega informações de produção e lucro estimado  

### `mart_safras_enriched.sql`
- Enriquecimento das safras com variáveis climáticas e de produtividade  
- Permite análises preditivas (ex: impacto do clima sobre a produção)

---

## ⚙️ Tecnologias Utilizadas

| Ferramenta | Finalidade |
|-------------|-------------|
| **Python** | Geração, extração e carga dos dados brutos |
| **PostgreSQL** | Armazenamento relacional em camadas |
| **Apache Airflow** | Orquestração das pipelines de ETL e dbt |
| **dbt-core** | Transformações SQL, versionamento e modelagem de dados |
| **Astronomer** | Ambiente de execução do Airflow com suporte a dbt |
| **Docker Compose** | Containerização do ecossistema completo |

---

## 🧠 Modelagem Dimensional

A modelagem segue o padrão **Star Schema**, onde:

- **Dimensões** (Dim) → Fazendas, Produtos  
- **Fatos** (Fact) → Safras, Insumos  

Essa estrutura permite:
- Consultas rápidas e otimizadas  
- Análises de custos e produtividade  
- Correlação entre clima e performance agrícola  

---

## 🪄 Orquestração Automática

O Airflow executa duas DAGs principais:

### 1️⃣ DAG de ETL (`etl_pipeline`)
- Gera e insere dados aleatórios nas tabelas RAW  
- Executa rotinas de limpeza e consistência  

### 2️⃣ DAG de dbt (`dbt_pipeline`)
- Executa `dbt run` e `dbt test` automaticamente  
- Atualiza as camadas **staging → intermediate → mart**

💡 Ao reiniciar o ambiente com:
```bash
astro dev stop && astro dev start

### ✅ Testes e Qualidade de Dados ###

O projeto implementa **testes automáticos de dados** via **dbt**, garantindo **integridade** e **consistência** em todas as camadas:

- 🧩 **unique**
- 🚫 **not_null**
- 🔗 **relationships**

Esses testes asseguram que não existam duplicidades, valores nulos ou relacionamentos inválidos entre tabelas.

---

## 🚀 Como Executar Localmente ##

### 1️⃣ Subir o ambiente completo ##
```bash
astro dev start


public.raw_*     → Dados brutos extraídos (camada RAW)
public.stg_*     → Dados tratados e padronizados (camada STG)
public.int_*     → Dados integrados (camada INTERMEDIATE)
public.mart_*    → Dados prontos para análise (camada MART)


Python (ETL) → PostgreSQL (RAW)
        ↓
dbt (Transformações)
        ↓
Camadas STG → INT → MART
        ↓
Power BI / Analytics

Autor

Desenvolvido por Nicolas César Nagel
📍 Projeto educacional para portfólio de Engenharia de Dados
💡 Stack: Python | Airflow | dbt | PostgreSQL | Docker | Astronomer