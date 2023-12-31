FROM python:3.11.6-bookworm

WORKDIR /app

COPY . /app

RUN pip install -r requirements.txt

# CMD pip3 install -r requirements.txt

CMD uvicorn main:app --host 0.0.0.0 --port $PORT --reload
