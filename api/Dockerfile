FROM python:3.10.4-alpine3.16
WORKDIR /api
COPY . /api
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
ENV FLASK_APP=api
CMD ["python","api.py"]