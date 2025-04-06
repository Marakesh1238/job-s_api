FROM python:3.12.2

WORKDIR /app

COPY .env .
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY wallets/ .

CMD ["gunicorn", "--bind", "0.0.0.0:8000", "wallets.wsgi:application"]
