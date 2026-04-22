FROM python:3.12-slim

# 1. Installa le dipendenze di sistema (fatto prima di tutto)
RUN apt-get update && apt-get install -y --no-install-recommends \
    libpq-dev \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# 2. Imposta la directory di lavoro
WORKDIR /app-be

# 3. Aggiorna pip
RUN pip install --upgrade pip

# 4. Copia PRIMA il file dei requisiti (buona pratica per la cache di Docker)
COPY ../requirements.txt .

# 5. Installa le dipendenze
RUN pip install --no-cache-dir -r requirements.txt

# 6. Copia tutto il resto del codice
COPY . .
