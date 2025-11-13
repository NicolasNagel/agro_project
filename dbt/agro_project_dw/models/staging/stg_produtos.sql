{{ config(
    materialized='view',
    schema='staging'
) }}

with source as (
    select * from {{ source('raw', 'raw_produtos') }}
),

     transformado as (
    select id
         , cod_produto       as id_produto
         , nome              as nm_produto
         , categoria
         , unidade_medida
         , preco_medio_mercado
         , dt_insercao
         , current_timestamp as etl_inserted_at
     from source
)

select *
 from transformado