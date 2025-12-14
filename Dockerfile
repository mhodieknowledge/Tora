
FROM python:3.10-slim

WORKDIR /app

RUN apt update && apt install -y \
    libboost-python-dev \
    libtorrent-rasterbar-dev \
    python3-libtorrent \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 5000
CMD ["python", "app.py"]
