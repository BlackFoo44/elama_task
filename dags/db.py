import os

from airflow.models import Variable


def get_variable(variable_name):
    if variable_name in os.environ:
        return os.environ[variable_name]
    else:
        return Variable.get(variable_name)

POSTGRES_NAME = 'postgres'
POSTGRES_HOST = '172.22.0.1'
POSTGRES_PORT = '5234'
POSTGRES_USER = 'airflow'
POSTGRES_PASSWORD = 'airflow'
POSTGRES_SCHEMA = 'public'

