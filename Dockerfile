FROM python:3.10
WORKDIR /usr/local/src/ocr

COPY requirements.txt .
RUN python -m pip install -r requirements.txt

COPY main.py .
COPY ocr.py .

EXPOSE 5005
ENTRYPOINT ["python", "main.py"]