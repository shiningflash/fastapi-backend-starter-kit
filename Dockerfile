# Pull base image
FROM python:3.11

# Set environment varibles
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV SQLALCHEMY_SILENCE_UBER_WARNING 1

WORKDIR /demoapp/app/

RUN ls -lha
COPY ./app/requirements.txt requirements.txt
RUN python -m pip install --upgrade pip
RUN python -m pip install -r requirements.txt
RUN ls -lha

WORKDIR /demoapp/
COPY . .

ENV PYTHONPATH=/demoapp
# RUN chmod +x /demoapp/start.sh
# CMD ["./start.sh"]
