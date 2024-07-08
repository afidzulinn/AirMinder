FROM python:3.10-slim

WORKDIR /APP

COPY . /APP

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 9090

CMD ["python", "app.py"]