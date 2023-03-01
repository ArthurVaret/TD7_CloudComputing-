FROM python:latest

WORKDIR /app

COPY app.py .
COPY requirements.txt .

RUN pip3 install -r requirements.txt

EXPOSE 5000

VOLUME /app

CMD ["python3", "-m", "flask", "run", "--host=0.0.0.0"]

