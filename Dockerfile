FROM python:3.10
WORKDIR /usr/local/src/ocr

# Limit CPU Threads for OpenMP
ENV OMP_THREAD_LIMIT 2

RUN apt-get update && apt-get install libgl1-mesa-glx -y && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN python -m pip install -r requirements.txt

COPY main.py .
COPY ocr.py .

EXPOSE 5005
ENTRYPOINT ["python", "main.py"]