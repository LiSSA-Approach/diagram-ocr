FROM python:3.8
WORKDIR /usr/local/src/ocr

RUN apt-get update && apt-get install tesseract-ocr -y

COPY requirements.txt .
RUN python -m pip install -r requirements.txt

COPY main.py .
COPY ocr.py .

EXPOSE 5005
ENTRYPOINT ["python", "main.py"]