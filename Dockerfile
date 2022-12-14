FROM python:3.9

WORKDIR /usr/src

COPY ./src/ /usr/
COPY ./requirements.txt /usr/src

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 5000

CMD [ "python", "./main.py"]