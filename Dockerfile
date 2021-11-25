FROM python:3.8

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip install --upgrade pip
RUN pip install pillow
RUN pip install -r requirements.txt

COPY . .

WORKDIR /app/sneakerhead

ADD sneakerhead.sql /docker-entrypoint-initdb.d

EXPOSE 3306

# CMD [ "python", "manage.py", "makemigrations" ]
# CMD [ "python", "manage.py", "migrate" ]
# CMD [ "python", "manage.py", "runserver" ]
