FROM python:3.9.16-buster

COPY ./scripts/requirements.txt /app/
RUN pip3 install -r /app/requirements.txt

COPY ./scripts /app/scripts/

CMD ["python", "-u", "/app/scripts/Scheduler.py"]