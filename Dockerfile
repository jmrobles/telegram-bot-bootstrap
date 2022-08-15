FROM python:3.10
RUN apt-get update \
    && apt-get -y install libpq-dev gcc \
    && pip install psycopg2
WORKDIR /app
COPY . .
RUN pip install -r requirements.txt
CMD [ "./start.sh" ]