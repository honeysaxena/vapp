FROM alpine:latest
RUN mkdir -p /app
COPY . app/
WORKDIR /app
RUN pip install -r requirements.txt
CMD ['python', 'videoapp/main.py']



