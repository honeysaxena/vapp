FROM python:latest
RUN mkdir -p /app
COPY . app/
WORKDIR /app
COPY trivy.sh /app/trivy.sh
RUN pip install --upgrade pip
RUN chmod x trivy.sh
RUN /bin/bash -c "./trivy.sh"
RUN pip install -r requirements.txt
CMD ["python", "videoapp/main.py"]



