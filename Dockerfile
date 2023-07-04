FROM docker.io/python:3.9.13
RUN pip install flask==2.2.2
RUN pip install requests==2.31.0
COPY . /src/
CMD ["python", "/src/app.py"]