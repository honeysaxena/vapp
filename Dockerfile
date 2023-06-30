FROM alpine:3.18
RUN mkdir -p /app
COPY . app/
WORKDIR /app
RUN apk add py3-pip python3-dev
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
CMD ['python', 'videoapp/main.py']



