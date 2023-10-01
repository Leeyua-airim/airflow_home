from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.providers.http.operators.http import SimpleHttpOperator
from airflow.decorators import task
from airflow.operators.trigger_dagrun import TriggerDagRunOperator
import pendulum

with DAG(
    dag_id='dags_trigger_dag_run_operator',
    start_date=pendulum.datetime(2023,4,1, tz='Asia/Seoul'),
    schedule='30 9 * * *',
    catchup=False
) as dag : 
    
    ''' 서울시 노션별 정류장 구간별 평균 운행시간 정보'''
    tb_cycle_station_info = SimpleHttpOperator(
        task_id = 'tb_cycle_station_info',
        http_conn_id='openapi.seoul.go.kr',
        endpoint='{{var.value.apikey_openapi_seoul_go_kr}}/json/tpssRouteSectionTime/1/5/',
        method='GET',
        headers={'Content-Type' : 'application/json',
                 'charset' : 'utf-8',
                 'Accept' : '*/*'}
    )

    @task(task_id='python_2')
    def python_2(**kwargs):
        ti = kwargs['ti']
        rslt = ti.xcom_pull(task_ids='tb_cycle_station_info')

        import json
        from pprint import pprint

        pprint(json.loads(rslt))

    tb_cycle_station_info >> python_2()

