FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt ./src/requirements.txt

RUN pip install -r ./src/requirements.txt

COPY . .

CMD ["python", "src/main.py"]