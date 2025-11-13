{{
    config(
        materialized='table',
        schema='intermediate'
    )
}}

with stg_fazendas as (
    select * from {{ ref('stg_fazendas') }}
),
     with_fazendas as (
    select {{dbt_utils.generate_surrogate_key(['id_fazenda']) }} as sk_fazenda
         , id_fazenda                                            as fk_fazenda
         , nm_fazenda
         , uf
         , cidade
         , area_total
         , latitude
         , longitude
         , dt_cadastro
         , dt_inicio_vigencia
         , dt_fim_vigencia
         , registro_ativo
         , dt_inicio_vigencia                                    as valido_de
         , coalesce(dt_fim_vigencia, '9999-12-31'::date)         as valido_ate
         , case when dt_fim_vigencia is null then true
                                             else false
           end                                                   as valido
         , dt_insercao
         , current_timestamp                                     as etl_inserted_at
        from stg_fazendas 
)
select *
 from with_fazendas