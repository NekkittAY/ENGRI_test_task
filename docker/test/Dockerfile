FROM python:3.11-slim

WORKDIR /app

COPY backend/ .
COPY tests/ ./test

RUN pip install -r test/requirements.txt

CMD ["python", "-m", "pytest", "test/"]
