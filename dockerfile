FROM jhonatans01/python-dlib-opencv
COPY . /workernode
WORKDIR /workernode
RUN pip3 install -r requirements.txt
EXPOSE 5554
EXPOSE 5556
CMD ["python3", "worker.py"]