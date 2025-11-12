{{ config(
    materialized='table',
    schema='intermediate'
) }}

with safras as (
    select * from {{ ref('stg_safras') }}
),

     fazendas as (
    select * from {{ ref('stg_fazendas') }}
),

     produtos as (
    select * from {{ ref('stg_produtos') }}
),

     enriched as (
    select s.id_safra
         , s.id_fazenda
         , f.nm_fazenda
         , f.uf
         , f.cidade
         , f.area_total
         , f.latitude
         , f.longitude
         , s.id_produto
         , p.nm_produto
         , p.categoria as categoria_produto
         , s.dt_plantacao
         , s.dt_colheita
         , extract(year from s.dt_plantacao)    as ano_plantacao
         , extract(month from s.dt_plantacao)   as mes_plantacao
         , extract(quarter from s.dt_plantacao) as tri_plantacao
         , case
                when extract(month from s.dt_plantacao) >= 9
                then extract(year from s.dt_plantacao)::text || '/' ||
                     (extract(year from s.dt_plantacao) + 1)::text
                else (extract(year from s.dt_plantacao) - 1)::text || '/' ||
                     extract(year from s.dt_plantacao)::text
           end                              as safra_agricola
         , case
                when extract(month from s.dt_plantacao) in (9, 10, 11) then 'Primavera'
                when extract(month from s.dt_plantacao) in (12, 1, 2)  then 'Verão'
                when extract(month from s.dt_plantacao) in (3, 4, 5)   then 'Outono'
                                                                       else 'Inverno'
           end                              as estacao_plantio 
         -- Metricas Calculadas
         , s.area_plantada
         , (s.area_plantada / nullif(f.area_total, 0)) * 100 as percentual_area_utilizada
         , s.producao_estimada
         , s.produtividade_por_hectare
         , s.qualidade_safra
         , s.custo_producao_estimado
         , s.receita_estimada
         , (s.receita_estimada - s.custo_producao_estimado) as lucro_bruto
         , case 
                when s.custo_producao_estimado > 0 
                then ((s.receita_estimada - s.custo_producao_estimado) / custo_producao_estimado) * 100
                else 0
           end               as roi_percentual
         , case
                when s.receita_estimada > 0
                then ((s.receita_estimada - s.custo_producao_estimado) / receita_estimada) * 100
                else 0
           end               as margem_lucro_percentual
         , s.receita_estimada / nullif(s.area_plantada, 0)        as receita_por_hectare
         , s.custo_producao_estimado / nullif(s.area_plantada, 0) as custo_por_hectare
         , case
                when s.produtividade_por_hectare >=
                    (select avg(produtividade_por_hectare) * 1.2 from safras where id_produto = s.id_produto)
                then 'Alta'
                when s.produtividade_por_hectare >=
                    (select avg(produtividade_por_hectare) * 0.8 from safras where id_produto = s.id_produto)
                then 'Média'
                else 'Baixa'
           end               as classificao_produtividade
         , case
                when (s.receita_estimada - s.custo_producao_estimado) > 0 then 'Lucrativo'
                when (s.receita_estimada - s.custo_producao_estimado) = 0 then 'Break-even'
                                                                          else 'Prejuízo'
           end               as status_financeiro
         , current_timestamp as etl_uploaded_at
     from safras s
    inner join fazendas f on s.id_fazenda = f.id_fazenda
    inner join produtos p on s.id_produto = p.id_produto        
)

select * from enriched