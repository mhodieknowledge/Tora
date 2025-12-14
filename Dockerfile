FROM ubuntu:22.04

ENV DEBIAN_FRONTEND=noninteractive

WORKDIR /app

# Install system python + libtorrent bindings
RUN apt update && apt install -y \
    python3 \
    python3-pip \
    python3-libtorrent \
    libtorrent-rasterbar-dev \
    && rm -rf /var/lib/apt/lists/*

# Make python command available
RUN ln -s /usr/bin/python3 /usr/bin/python

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 5000
CMD ["python", "app.py"]
