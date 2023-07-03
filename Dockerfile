FROM python:3.10-slim-bookworm

WORKDIR /stratagems

ADD ./stratagems .

COPY requirements.txt requirements.txt

RUN pip install --upgrade pip

RUN pip install -r requirements.txt

CMD ["python3", "start_app.py"]