from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.providers.http.operators.http import SimpleHttpOperator
from airflow.decorators import task
from airflow.operators.trigger_dagrun import TriggerDagRunOperator
import pendulum

with DAG(
    dag_id='dags_simple_http_operator',
    start_date=pendulum.datetime(2023,4,1, tz='Asia/Seoul'),
    schedule=None,
    catchup=False
) as dag:
    ''' 서울시 노션별 정류장 구간별 평균 운행시간 정보'''
    tb_cycle_station_info = SimpleHttpOperator(
        task_id = 'tb_cycle_station_info',
        http_conn_id='openapi.seoul.go.kr',
        endpoint='7363724e626272693537526f6f6d6c/json/tbCycleStationUseMonthInfo/1/10/202208',
        method='GET',
        headers={'Content-Type' : 'application/json',
                 'charset' : 'utf-8',
                 'Accept' : '*/*'
                 }
    )

    @task(task_id='python_2')
    def python_2(**kwargs):
        ti = kwargs['ti']
        print("체크용 1")
        rslt = ti.xcom_pull(task_ids='tb_cycle_station_info')
        print("체크용 2")
        print("rslt : \n", rslt)
        import json
        from pprint import pprint
        
        pprint(json.loads(rslt))
        print("체크용 3")

    tb_cycle_station_info >> python_2()


