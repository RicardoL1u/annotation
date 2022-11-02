FROM python:3.8-slim-buster
WORKDIR /app
COPY . .
RUN apt update
RUN apt install sqlite3
RUN pip install -r requirements.txt
# RUN apt install sqlite3
CMD [ "bash", "run.sh" ]