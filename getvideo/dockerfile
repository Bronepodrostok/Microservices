FROM python:3.11.7-slim-bullseye

WORKDIR /app
COPY * /app

RUN pip install -r requirements.txt

#RM if loading to yandex
EXPOSE 80

CMD ["python", "main.py"]

