FROM python:3.9.17-alpine3.17
RUN mkdir -p /app
COPY . app/
WORKDIR /app
RUN pip install -r requirements.txt
CMD ['python', 'videoapp/main.py']



