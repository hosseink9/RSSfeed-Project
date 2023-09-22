FROM python3
WORKDIR /dockerrss
COPY requirements.txt .
RUN pip install -U pip
RUN pip install -r requirements.txt
COPY . .
EXPOSE 8000
CMD ["python", "manage.py", "runserver"]