FROM python:3.6-jessie

COPY . /usr/src/app
RUN pip install --no-cache-dir -r /usr/src/app/requirements.txt
ENV FLASK_APP chat.py

FROM postgres:9.6
ENV POSTGRES_PASSWORD=postgres
ENV POSTGRES_USER=chat2
ENV POSTGRES_DB=chat2
EXPOSE 5000
CMD ["python", "./chat.py"]
