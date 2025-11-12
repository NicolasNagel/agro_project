{{ config(
    materialized='view',
    schema='staging'
) }}

with source as (
    select * from {{ source('raw', 'raw_safras') }}
),

     produtos as (
    select * from {{ ref('stg_produtos') }} 
),

     transformado as (
    select s.id
         , s.cod_safra         as id_safra
         , s.id_fazenda
         , s.id_produto
         , s.data_plantacao    as dt_plantacao
         , s.data_colheita     as dt_colheita
         , s.area_plantada
         -- Cálculos de Métricas Básicas
         , EXTRACT(day FROM (s.data_colheita - s.data_plantacao)) as dias_ciclo
         , case
                when p.categoria = 'Grão'       then s.area_plantada * 3.5
                when p.categoria = 'Bebida'     then s.area_plantada * 30
                when p.categoria = 'Proteína'   then s.area_plantada * 12
                when p.categoria = 'Fibra'      then s.area_plantada * 4
                when p.categoria = 'Industrial' then s.area_plantada * 70
                                                else s.area_plantada * 2
           end                                  as producao_estimada
         , case
                when p.categoria = 'Grão'       then 3.5
                when p.categoria = 'Bebida'     then 30
                when p.categoria = 'Proteína'   then 12
                when p.categoria = 'Fibra'      then 4
                when p.categoria = 'Industrial' then 70
                                                else 2
           end                                  as produtividade_por_hectare
         , s.area_plantada *
           case
                when p.categoria = 'Grão'       then 5000
                when p.categoria = 'Bebida'     then 8000
                when p.categoria = 'Proteína'   then 6000
                when p.categoria = 'Fibra'      then 5500
                when p.categoria = 'Industrial' then 4000
                                                else 5000
           end                                  as custo_producao_estimado
         , (case
                when p.categoria = 'Grão'       then s.area_plantada * 3.5
                when p.categoria = 'Bebida'     then s.area_plantada * 30
                when p.categoria = 'Proteína'   then s.area_plantada * 12
                when p.categoria = 'Fibra'      then s.area_plantada * 4
                when p.categoria = 'Industrial' then s.area_plantada * 70
                                                else s.area_plantada * 2
           end) * p.preco_medio_mercado         as receita_estimada
         , case
                when EXTRACT(day FROM(s.data_colheita - s.data_plantacao)) >= 150 then 'A'
                when EXTRACT(day FROM(s.data_colheita - s.data_plantacao)) >= 120 then 'B'
                                                                                  else 'C'
           end                                  as qualidade_safra
         , s.dt_insercao                           
         , current_timestamp   as etl_inserted_at
     from source s
    inner join produtos p on s.id_produto = p.id_produto
)

select *
 from transformado