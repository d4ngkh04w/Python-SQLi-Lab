FROM python:3.12-slim

WORKDIR /app

RUN pip install --no-cache-dir --upgrade pip
RUN python3 -m venv /app/venv

COPY requirements.txt .
RUN /app/venv/bin/pip install --no-cache-dir -r requirements.txt

COPY . .

RUN useradd -m user && chown -R user:user /app
USER user

EXPOSE 1303

CMD ["/app/venv/bin/python", "app.py"]
