FROM python:3.8.13

COPY . /

RUN pip install -r requirements.txt

CMD python run.py
