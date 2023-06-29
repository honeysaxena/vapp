FROM python:latest
RUN mkdir -p /app
COPY . app/
WORKDIR /app
RUN pip install -r requirements.txt
ENTRYPOINT [ "trivy.sh" ]
CMD ["python", ".videoapp/main.py"]



