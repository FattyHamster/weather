FROM python:3.11
WORKDIR /app
COPY requirements.txt .
RUN pip3 install --upgrade pip 
RUN pip3 install -r requirements.txt
COPY app .
CMD [ "gunicorn" ,"--bind", "0.0.0.0:8000", "wsgi:application" ]
