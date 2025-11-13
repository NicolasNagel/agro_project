{{ 
    config(
        materialized='table',
        schema='intermediate'
    )
}}

with stg_insumos as (
    select * from {{ ref('stg_insumos') }}
),
     stg_safras as (
    select * from {{ ref('stg_safras') }}
),
     with_insumos as (
    select {{ dbt_utils.generate_surrogate_key(['i.id'] )}} as sk_insumo
         , i.id                                             as fk_insumo
         , s.id_safra                                       as fk_safra
         , i.dt_aplicacao
         , i.tp_insumo                                      as tipo_insumo
         , i.nm_insumo                                      as nome_insumo
         , i.qtd_aplicada
         , i.custo_unitario
         , i.area_aplicada
         , (i.area_aplicada * i.custo_unitario)             as custo_total
         , i.dt_insercao
         , i.etl_inserted_at
     from stg_insumos     i
    inner join stg_safras s on i.id_safra = s.id_safra
)
select *
 from with_insumos 