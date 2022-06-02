FROM python:3.8
WORKDIR /usr/local/src/ocr

RUN apt-get update \
    && apt-get install -y lsb-release \
    && echo "deb https://notesalexp.org/tesseract-ocr5/$(lsb_release -cs)/ $(lsb_release -cs) main" | tee /etc/apt/sources.list.d/notesalexp.list > /dev/null \
    && wget -O - https://notesalexp.org/debian/alexp_key.asc | apt-key add - \
    && apt-get update \
    && apt-get install -y ffmpeg libsm6 libxext6 tesseract-ocr \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN python -m pip install -r requirements.txt

COPY main.py .
COPY ocr.py .

EXPOSE 5005
ENTRYPOINT ["python", "main.py"]