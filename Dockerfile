FROM docker.io/python:3.9.5
RUN pip install flask==1.1.2
RUN pip install requests==2.26.0
COPY . /src/
CMD ["python", "/src/app.py"]