import logging
import os
from pathlib import Path

import pandas as pd
from google.cloud import bigquery
from google.oauth2 import service_account

from session import Session, engine

ROOT_DIR = str(Path(__file__).resolve().parents[1])

def load_csv_to_postgres(table_name: str, csv_file, webinar=None):
    with engine.connect() as connection:
        df = pd.read_csv(csv_file)
        if webinar is not None:
            df['webinar_date'] = "2016-04-01 15:00:00"

        df.to_sql(table_name, con=connection, if_exists='replace', index=False)
        logging.info("Данные успешно загружены.")


def create_materialized(name_for_materializer: str):
    with Session() as session:
        try:
            create_materialized_view = f"""
                CREATE MATERIALIZED VIEW IF NOT EXISTS {name_for_materializer} AS
                SELECT w.email AS visitor_email,
                SUM(t.price) AS total_transactions
                FROM webinar w
                JOIN users u ON w.email = u.email
                JOIN transactions t ON u.user_id = t.user_id
                WHERE u.date_registration > '2016-04-01'
                GROUP BY w.email;

            """

            # Выполнение запроса
            session.execute(create_materialized_view)
            session.commit()
            logging.info("Материализованное представление успешно создано.")
        except Exception as e:
            session.rollback()
            logging.info(f"Ошибка при создании материализованного представления: {e}")


def get_data_from_postgres(name_for_materializer: str):
    with Session() as session:
        try:
            select_data_query = f"""
                SELECT * FROM {name_for_materializer};
                """
            result = session.execute(select_data_query)
            data = pd.DataFrame(result.fetchall(), columns=result.keys())
            logging.info("Данные успешно загружены для передачи в BigQuery.")
            return data
        except Exception as e:
            session.rollback()
            logging.info(f"Ошибка при загрузке данных: {e}")




def upload_to_bigquery(name_for_materializer: str, project_id: str, dataset_id: str, table_id: str):
    path_for_credentials = os.path.join(ROOT_DIR, 'mytestproject.json')
    try:
        credentials = service_account.Credentials.from_service_account_file(path_for_credentials)
        logging.info(f'{credentials}')
        client = bigquery.Client(project=project_id, credentials=credentials)

        dataframe = get_data_from_postgres(name_for_materializer)
        table_ref = client.dataset(dataset_id).table(table_id)

        job_config = bigquery.LoadJobConfig()
        job_config.write_disposition = bigquery.WriteDisposition.WRITE_TRUNCATE

        job = client.load_table_from_dataframe(dataframe, table_ref, job_config=job_config)
        job.result()

        logging.info(f"Данные успешно загружены в BigQuery: {project_id}.{dataset_id}.{table_id}")
    except Exception as e:
        logging.error(f"Ошибка при загрузке данных в BigQuery: {e}")
