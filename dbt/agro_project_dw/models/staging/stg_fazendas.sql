{{ config(
    materialized='view',
    schema='staging'
) }}

with source as (
    select * from {{ source('raw', 'raw_fazendas') }}
),

     transformado as (
    select id
         , cod_fazenda          as id_fazenda
         , nome_fazenda         as nm_fazenda
         , estado               as uf
         , municipio            as cidade
         , area_total_hectares  as area_total
         , latitude
         , longitude
         , data_cadastro        as dt_cadastro
         , data_inicio_vigencia as dt_inicio_vigencia
         , data_fim_vigencia    as dt_fim_vigencia
         , case 
                when registro_ativo = 2
                then 'ativo'
                else 'inativo'
           end                  as registro_ativo 
         , dt_insercao
         , current_timestamp    as etl_inserted_at 
     from source
)

select *
 from transformado