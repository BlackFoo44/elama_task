FROM apache/airflow:2.3.4
COPY requirements.txt /requirements.txt
RUN pip install --user --upgrade pip
RUN pip install --no-cache-dir --user -r /requirements.txt
ENV GOOGLE_APPLICATION_CREDENTIALS="/opt/airflow/mytestproject.json"
COPY mytestproject.json /opt/airflow/