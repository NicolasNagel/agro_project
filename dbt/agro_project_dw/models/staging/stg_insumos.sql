{{ config(
    materialized='view',
    schema='staging'
) }}

with source as (
    select * from {{ source('raw', 'raw_insumos') }}
),

     transformado as (
    select id
         , id_safra
         , data_aplicacao      as dt_aplicacao
         , tipo_insumo         as tp_insumo
         , nome_insumo         as nm_insumo
         , quantidade_aplicada as qtd_aplicada
         , custo_unitario
         , area_aplicada
         , dt_insercao
         , current_timestamp   as etl_inserted_at
     from source
)

select * 
 from transformado