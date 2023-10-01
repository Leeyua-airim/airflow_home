from operators.seoul_api_to_csv_operator import SeoulApliToCsvOperator
from airflow import DAG
import pendulum

with DAG(
    dag_id='dags_seoul_api_corona',
    schedule= '0 7 * * *',
    start_date= pendulum.datetime(2023,9,30, tz='Asia/Seoul'),
    catchup=False
) as dag:
    '''서울시 코로나 19 확진자 동향'''
    # https://data.seoul.go.kr/dataList/OA-20461/S/1/datasetView.do?tab=A
    # http://openapi.seoul.go.kr:8088/(인증키)/xml/TbCorona19CountStatus/1/5/
    tb_corona19_count_status = SeoulApliToCsvOperator(
        task_id    = 'tb_corona19_count_status', # 기본 값 
        dataset_nm = 'TbCorona19CountStatus',
        path = '/opt/airflow/files/TbCorona19CountStatus/{{data_interval_end.in_timezone("Asia/Seoul") | ds_nodash }}',
        file_name='TbCorona19CountStatus.csv'
    )

    
    '''서울시 코로나 19 백신 예방접종 현황'''
    # http://openapi.seoul.go.kr:8088/(인증키)/xml/tvCorona19VaccinestatNew/1/5/
    tb_corona19_vaccine_stat_new = SeoulApliToCsvOperator(
        task_id    = 'tv_corona19_vaccine_stat_new', # 기본 값 
        dataset_nm = 'tvCorona19VaccinestatNew',
        path = '/opt/airflow/files/tvCorona19VaccinestatNew/{{data_interval_end.in_timezone("Asia/Seoul") | ds_nodash }}',
        file_name='tvCorona19VaccinestatNew.csv'
    )

    tb_corona19_count_status >> tb_corona19_vaccine_stat_new
