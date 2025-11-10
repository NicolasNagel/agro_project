from src.database.db_model import (
    FarmTable,
    ProductTable,
    SafrasTable,
    InsumosTable, 
    ClimaTable
)
from src.models.model import (
    farm_schema,
    produto_schema,
    safras_schema,
    insumos_schema,
    clima_schema
)
from src.data.generate_fake_data import (
    gerar_dados_fazendas, 
    gerar_dados_produtos, 
    gerar_dados_safras, 
    gerar_dados_insumos, 
    gerar_dados_climaticos
)

DATA_MAPPING = [
    {
        'Fazendas': {
            'Schema': farm_schema,
            'Tabela': FarmTable,
            'Nome Tabela': 'raw_fazendas',
            'Função': gerar_dados_fazendas,
        },
        'Produtos': {
            'Schema': produto_schema,
            'Tabela': ProductTable,
            'Nome Tabela': 'raw_produtos',
            'Função': gerar_dados_produtos,
        },
        'Safras': {
            'Schema': safras_schema,
            'Tabela': SafrasTable,
            'Nome Tabela': 'raw_safras',
            'Função': gerar_dados_safras,
        },
        'Insumos': {
            'Schema': insumos_schema,
            'Tabela': InsumosTable,
            'Nome Tabela': 'raw_insumos',
            'Função': gerar_dados_insumos,
        },
        'Clima': {
            'Schema': clima_schema,
            'Tabela': ClimaTable,
            'Nome Tabela': 'raw_clima',
            'Função': gerar_dados_climaticos,
        },
    },
]