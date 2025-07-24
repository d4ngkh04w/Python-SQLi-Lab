FROM ubuntu:22.04

WORKDIR /app

RUN apt update && apt install -y \
    python3 \
    python3-pip \
    python3-venv \
    mysql-server \
    curl \
    socat \
    netcat-traditional \
    && rm -rf /var/lib/apt/lists/*

RUN usermod -d /var/lib/mysql mysql

COPY . .

RUN python3 -m venv venv && \
    ./venv/bin/pip install --upgrade pip && \
    ./venv/bin/pip install -r requirements.txt

COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

RUN echo "FLAG{rc3_1s_4w3s0m3}" > /flag.txt

EXPOSE 1303 3306

CMD ["/entrypoint.sh"]
