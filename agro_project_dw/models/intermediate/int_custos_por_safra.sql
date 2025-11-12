{{
    config(
        materialized='table',
        schema='intermediate'
    )
}}

with safras as (
    select * from {{ ref('stg_safras') }}
),

     insumos as (
    select * from {{ ref('stg_insumos') }}
),

     custos_insumos as (
    select id_safra
         , count(*)                                                                                 as num_aplicacoes
         , count(distinct tp_insumo)                                                                as tipos_insumos_diferentes
         , sum(qtd_aplicada * custo_unitario)                                                       as custo_total_insumos
         , avg(qtd_aplicada * custo_unitario)                                                       as custo_medio_aplicacao
         , sum(case when tp_insumo = 'Fertilizantes' then qtd_aplicada * custo_unitario else 0 end) as custo_fertilizantes
         , sum(case when tp_insumo = 'Defensivos'    then qtd_aplicada * custo_unitario else 0 end) as custo_defensivos
         , sum(case when tp_insumo = 'Irrigação'     then qtd_aplicada * custo_unitario else 0 end) as custo_irrigacao
         , sum(case when tp_insumo = 'Fertilizantes' then qtd_aplicada else 0 end)                  as qtd_fertilizantes
         , sum(case when tp_insumo = 'Defensivos'    then qtd_aplicada else 0 end)                  as qtd_defensivos
         , sum(case when tp_insumo = 'Fertilizantes' then qtd_aplicada else 0 end)                  as qtd_irrigacao
         , max(area_aplicada)                                                                       as area_maxima_aplicada
         , avg(area_aplicada)                                                                       as area_media_aplicada 
     from insumos
    group by id_safra
),

     final as (
    select s.id_safra
         , s.id_fazenda
         , s.id_produto
         , s.area_plantada
         , s.custo_producao_estimado          as custo_total_safra
         , coalesce(c.custo_total_insumos, 0) as custo_real_insumos
         , coalesce(c.custo_fertilizantes, 0) as custo_fertilizantes
         , coalesce(c.custo_defensivos, 0)    as custo_defensivos
         , coalesce(c.custo_irrigacao, 0)     as custo_irrigacao
         , (s.custo_producao_estimado - coalesce(c.custo_total_insumos, 0)) as outros_custos
         , coalesce(c.num_aplicacoes, 0)      as num_aplicacoes
         , coalesce(c.tipos_insumos_diferentes, 0) as tipos_insumos_diferentes
         , coalesce(c.custo_medio_aplicacao, 0)    as custo_medio_aplicacao
         , coalesce(c.qtd_fertilizantes, 0)        as qtd_fertilizantes
         , coalesce(c.qtd_defensivos, 0)           as qtd_defensivos
         , coalesce(c.qtd_irrigacao, 0)            as qtd_irrigacao
         , case
               when s.custo_producao_estimado > 0
               then (coalesce(c.custo_total_insumos, 0) / s.custo_producao_estimado) * 100
               else 0
           end                                      as percentual_custo_insumo
         , case
               when s.custo_producao_estimado > 0
               then (coalesce(c.custo_fertilizantes, 0) / s.custo_producao_estimado) * 100
               else 0
           end                                      as percentual_fertilizantes
         , case
                when s.custo_producao_estimado > 0
                then (coalesce(c.custo_defensivos, 0) / s.custo_producao_estimado) * 100
                else 0
           end                                      as percentual_defensivos
         , case
                when s.custo_producao_estimado > 0
                then (coalesce(c.custo_irrigacao, 0) / s.custo_producao_estimado) * 100
                else 0
           end                                      as percentual_irrigacao
         , coalesce(c.custo_total_insumos, 0) / nullif(s.area_plantada, 0) as custo_insumo_por_hectare
         , case
                when coalesce(c.num_aplicacoes, 0) >= 8 then 'Intensivo'
                when coalesce(c.num_aplicacoes, 0) >= 4 then 'Moderado'
                when coalesce(c.num_aplicacoes, 0) > 0  then 'Leve'
                                                        else 'Sem registro'
           end                                      as intensidade_uso_insumos
         , current_timestamp as etl_inserted_at 
     from safras s
    left join custos_insumos c on s.id_safra = c.id_safra
)

select *
 from final