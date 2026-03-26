FROM python:3.11

WORKDIR /app

COPY . .

RUN apt-get update && apt-get install -y netcat-openbsd

RUN pip install -r requirements.txt

CMD ["sh", "entrypoint.sh"]