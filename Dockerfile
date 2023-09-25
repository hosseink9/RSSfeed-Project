FROM python:3.10

WORKDIR /code

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . /copy/

EXPOSE 8000

CMD ["python3", "manage.py", "runserver"]