From python:3.7
RUN mkdir -p /opt/dkops
WORKDIR /opt/dkops
COPY . .
RUN pip install -r requirements.txt
ENTRYPOINT ["python", "dkops.py", "start"]
