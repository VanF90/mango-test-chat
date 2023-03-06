FROM python:3.9-slim-buster

ENV PYTHONUNBUFFERED 1

RUN apt-get update
&& apt-get install -y netcat gcc postgresql
&& apt-get clean
&& rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["./start_server.sh"]