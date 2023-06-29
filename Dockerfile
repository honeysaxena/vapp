FROM alpine:3.18
RUN mkdir -p /app
COPY . app/
WORKDIR /app
RUN pip install -r requirements.txt
CMD ["python", ".videoapp/main.py"]



