import os

from airflow.sdk import dag, task
from airflow.providers.standard.operators.trigger_dagrun import TriggerDagRunOperator
from datetime import datetime
from cosmos import DbtDag, ProjectConfig, ProfileConfig, ExecutionConfig
from cosmos.profiles import PostgresUserPasswordProfileMapping
from pendulum import datetime


from src.controllers.controller import pipeline

def build_dbt_dag():
    profile_config = ProfileConfig(
        profile_name='agro_project_dw',
        target_name='dev',
        profile_mapping=PostgresUserPasswordProfileMapping(
            conn_id='my_database',
            profile_args={'schema': 'public'},
        )
    )

    return DbtDag(
        project_config=ProjectConfig(
            '/usr/local/airflow/dbt/agro_project_dw'
        ),
        profile_config=profile_config,
        execution_config=ExecutionConfig(
            dbt_executable_path=f"{os.environ['AIRFLOW_HOME']}/dbt_venv/bin/dbt",
        ),
        operator_args={
            'install_deps': True,
        },
        schedule="@daily",
        start_date=datetime(2025, 9, 11),
        catchup=False,
        dag_id='agro_etl_dw',
        default_args={'retries': 2},
)

agro_elt_dw = build_dbt_dag() 

@dag(
    dag_id='agro_etl',
    description='Pipeline ETL que gera dados Agro',
    schedule='*/30 * * * *',
    start_date=datetime(2025, 9, 11),
    catchup=False,
)
def agro_etl():

    @task(task_id='gerar_dados')
    def task_pipeline():
        return pipeline()
    
    trigger_dbt = TriggerDagRunOperator(
        task_id='trigger_dbt_dw',
        trigger_dag_id='agro_etl_dw',
        wait_for_completion=True,
        reset_dag_run=True,
    )

    t1 = task_pipeline()
    t1 >> trigger_dbt

agro_etl_dag = agro_etl()