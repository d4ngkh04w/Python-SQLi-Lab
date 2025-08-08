FROM ubuntu:22.04

WORKDIR /app

RUN apt update && apt install -y \
    python3 \
    python3-pip \
    mysql-server \
    curl \
    socat \
    netcat-traditional \
    && rm -rf /var/lib/apt/lists/*

RUN usermod -d /var/lib/mysql mysql

COPY requirements.txt .

RUN pip3 install --no-cache-dir -r requirements.txt

COPY entrypoint.sh /entrypoint.sh

RUN chmod +x /entrypoint.sh

COPY . .

RUN echo "FLAG{rc3_1s_4w3s0m3}" > /flag.txt

EXPOSE 1303

CMD ["/entrypoint.sh"]