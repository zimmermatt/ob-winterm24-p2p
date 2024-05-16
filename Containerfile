FROM python:3

WORKDIR /usr/src/app/

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .
ENV PYTHONPATH=src/main/py

CMD [ "python3", "-m", "peer.peer", "50000", "src/test/py/resources/peer_test", "0.0.0.0:50000" ]
