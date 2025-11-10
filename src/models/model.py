import pandera as pa

from pandera.dtypes import DateTime

farm_schema = pa.DataFrameSchema(
    columns = {
        'id': pa.Column(pa.Int, checks=[pa.Check.greater_than_or_equal_to(0)]),
        'cod_fazenda': pa.Column(pa.String, checks=[pa.Check.str_startswith('FA')]),
        'nome_fazenda': pa.Column(pa.String),
        'estado': pa.Column(pa.String),
        'municipio': pa.Column(pa.String),
        'area_total_hectares': pa.Column(pa.Int),
        'latitude': pa.Column(pa.Float),
        'longitude': pa.Column(pa.Float),
        'data_cadastro': pa.Column(DateTime, coerce=True),
        'data_inicio_vigencia': pa.Column(DateTime, coerce=True),
        'data_fim_vigencia': pa.Column(DateTime, coerce=True),
        'registro_ativo': pa.Column(pa.Int),
    }
)

produto_schema = pa.DataFrameSchema(
    columns = {
        'id': pa.Column(pa.Int, checks=[pa.Check.greater_than_or_equal_to(0)]),
        'cod_produto': pa.Column(pa.String, checks=[pa.Check.str_startswith('PROD')]),
        'nome': pa.Column(pa.String),
        'categoria': pa.Column(pa.String),
        'unidade_medida': pa.Column(pa.String),
        'preco_medio_mercado': pa.Column(pa.Float),
    }
)

safras_schema = pa.DataFrameSchema(
    columns = {
        'id': pa.Column(pa.Int, checks=[pa.Check.greater_than_or_equal_to(0)]),
        'cod_safra': pa.Column(pa.String, checks=[pa.Check.str_startswith('SAF')]),
        'id_fazenda': pa.Column(pa.String, checks=[pa.Check.str_startswith('FA')]),
        'id_produto': pa.Column(pa.String, checks=[pa.Check.str_startswith('PROD')]),
        'data_plantacao': pa.Column(pa.DateTime, coerce=True),
        'data_colheita': pa.Column(pa.DateTime, coerce=True),
        'area_plantada': pa.Column(pa.Float, checks=[pa.Check.greater_than_or_equal_to(0)])
    }
)

insumos_schema = pa.DataFrameSchema(
    columns = {
        'id': pa.Column(pa.Int, checks=[pa.Check.greater_than_or_equal_to(0)]),
        'id_safra': pa.Column(pa.String, checks=[pa.Check.str_startswith('SAF')]),
        'data_aplicacao': pa.Column(pa.DateTime, coerce=True),
        'tipo_insumo': pa.Column(pa.String),
        'nome_insumo': pa.Column(pa.String),
        'quantidade_aplicada': pa.Column(pa.Float, checks=[pa.Check.greater_than_or_equal_to(0)]),
        'custo_unitario': pa.Column(pa.Float, checks=[pa.Check.greater_than_or_equal_to(0)]),
        'area_aplicada': pa.Column(pa.Float, checks=[pa.Check.greater_than_or_equal_to(0)]),
    }
)

clima_schema = pa.DataFrameSchema(
    columns = {
        'id_fazenda': pa.Column(pa.String, checks=[pa.Check.str_startswith('FA')]),
        'data': pa.Column(pa.DateTime, coerce=True),
        'temperatura_media': pa.Column(pa.Float, checks=[pa.Check.greater_than_or_equal_to(0)]),
        'precipitacao': pa.Column(pa.Float, checks=[pa.Check.greater_than_or_equal_to(0)]),
        'umidade_relativa': pa.Column(pa.Float, checks=[pa.Check.greater_than_or_equal_to(0)]),
        'velocidade_vento': pa.Column(pa.Float, checks=[pa.Check.greater_than_or_equal_to(0)]),
        'horas_sol': pa.Column(pa.Float, checks=[pa.Check.greater_than_or_equal_to(0)]),
    }
)