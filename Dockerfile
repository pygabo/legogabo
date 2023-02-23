FROM python:3.9-slim-buster

WORKDIR /app

COPY requirements.txt requirements.txt

RUN apt-get update && \
    apt-get install -y gcc && \
    pip3 install --no-cache-dir -r requirements.txt && \
    apt-get remove -y gcc && \
    apt-get autoremove -y && \
    rm -rf /var/lib/apt/lists/*

COPY . .

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
