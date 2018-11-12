# This will build the Python Docker image for testing purpose

FROM python:2

WORKDIR /usr/src/app

COPY requirements.txt ./

RUN pip install --no-cache-dir -r requirements.txt

COPY test-es.py ./

RUN chmod +x test-es.py

CMD [ "python", "test-es.py" ]
