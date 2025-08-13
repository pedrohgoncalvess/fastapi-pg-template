FROM python:3.13

WORKDIR /app

COPY . .

RUN pip install --no-cache-dir -r requirements.docker.txt

CMD yoyo apply -b && python main.py  # TODO: Run pytest before dockerize app.