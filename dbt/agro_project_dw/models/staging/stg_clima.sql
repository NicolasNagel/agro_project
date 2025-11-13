{{ config(
    materialized='view',
    schema='staging'
) }}

with source as (
    select * from {{ source('raw', 'raw_clima') }}
),

     transformado as (
    select id
         , id_fazenda
         , data              as dt
         , temperatura_media
         , precipitacao
         , umidade_relativa
         , velocidade_vento
         , horas_sol
         , dt_insercao
         , current_timestamp as etl_inserted_at
     from source
)

select *
 from transformado