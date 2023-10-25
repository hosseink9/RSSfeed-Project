FROM python:3.10

ENV PYTHONUNBUFFERED=1

WORKDIR /src

COPY requirements.txt .
RUN pip install -r requirements.txt

EXPOSE 8000

RUN apt update
RUN apt install gettext -y

CMD python3 manage.py makemessages --all && \
    python3 manage.py compilemessages && \
    python3 manage.py makemigrations && \
    python3 manage.py migrate && \
    python3 manage.py runserver 0.0.0.0:8000