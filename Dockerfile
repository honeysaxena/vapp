FROM python:latest
RUN mkdir -p /app
COPY . app/
WORKDIR /app
COPY trivy.sh .
RUN pip install --upgrade pip
RUN chmod +x trivy.sh
RUN pip install -r requirements.txt
CMD ["python", "videoapp/main.py"]



