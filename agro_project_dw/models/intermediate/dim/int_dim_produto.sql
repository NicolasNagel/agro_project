{{
    config(
        materialized='table',
        schema='intermediate'
    )
}}

with stg_produtos as (
    select * from {{ ref('stg_produtos') }}
),
     with_produtos as (
    select {{dbt_utils.generate_surrogate_key(['id_produto']) }} as sk_produto
         , id_produto                                            as fk_produto
         , nm_produto
         , unidade_medida
         , preco_medio_mercado
         , categoria
         , case
                when categoria in ('Grão', 'Bebida', 'Fibra') then 'Vegetal'
                when categoria = 'Proteína'                   then 'Animal'
                when categoria = 'Industrial'                 then 'Processado'
                                                              else 'Outros'
           end                                                   as grupo_produto
         , dt_insercao
         , current_timestamp                                     as etl_inserted_at
        from stg_produtos
)
select *
 from with_produtos