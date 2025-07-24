#!/bin/bash

echo "[INFO] Setting up MySQL configuration..."
chmod 644 /app/config/mysql.cnf
cp /app/config/mysql.cnf /etc/mysql/conf.d/
chown -R mysql:mysql /usr/lib/mysql/plugin/

echo "[INFO] Starting MySQL service..."
mysqld_safe --datadir=/var/lib/mysql &

echo "[INFO] Waiting for MySQL to be ready..."
until mysqladmin ping -h 127.0.0.1 --silent; do
    echo "[INFO] MySQL is not ready yet, waiting..."
    sleep 2
done

echo "[INFO] Setting up MySQL user and database..."
mysql -u root <<-EOSQL
    CREATE DATABASE IF NOT EXISTS sqli_lab;
    ALTER USER 'root'@'localhost' IDENTIFIED WITH mysql_native_password BY 'root';
    FLUSH PRIVILEGES;
EOSQL

echo "[INFO] Starting Python app..."
exec /app/venv/bin/python3 app.py
