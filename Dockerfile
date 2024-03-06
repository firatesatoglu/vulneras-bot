FROM python:3.11
RUN mkdir /autonesacu
ADD . /autonesacu
WORKDIR /autonesacu
RUN pip install -r requirements.txt
CMD ["python", "main.py"]