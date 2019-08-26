FROM python:3.7-slim-stretch
LABEL MAINTAINER="KML VISION, devops@kmlvision.com"

WORKDIR /usr/src/k8s-nodelabel
# install the requirements
COPY requirements.txt .
RUN pip install -r requirements.txt
# install the application
COPY k8s-nodelabel/ .

ENV PYTHONUNBUFFERED 1

# run the application
WORKDIR /
ENTRYPOINT ["python", "/usr/src/k8s-nodelabel/k8s_nodelabel.py"]
