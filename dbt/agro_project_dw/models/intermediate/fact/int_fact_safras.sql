{{ 
    config(
        materialized='table',
        schema='intermediate'
    )
}}

with stg_safras as (
    select * from {{ ref('stg_safras') }}
),
     stg_fazendas as (
    select * from {{ ref('stg_fazendas') }}
),
     stg_produtos as (
        select * from {{ ref('stg_produtos') }}
),
     with_safras as (
    select {{ dbt_utils.generate_surrogate_key(['s.id_safra']) }} as sk_safra
         , s.id_safra                                             as fk_safra
         , s.id_fazenda                                           as fk_fazenda
         , p.id_produto                                           as sk_produto
         , s.dt_plantacao
         , s.dt_colheita
         , s.area_plantada
         , s.producao_estimada
         , s.produtividade_por_hectare
         , s.custo_producao_estimado
         , s.receita_estimada
         , s.qualidade_safra
         , s.dias_ciclo
         , (s.receita_estimada - s.custo_producao_estimado)       as lucro_bruto
         , s.dt_insercao
         , s.etl_inserted_at 
     from stg_safras s
    inner join stg_fazendas f on s.id_fazenda = f.id_fazenda
    inner join stg_produtos p on s.id_produto = p.id_produto
)
select *
 from with_safras