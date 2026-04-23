import os
from minio import Minio

# Inizializza il client MinIO
minio_client = Minio(
    os.getenv("MINIO_ENDPOINT", "minio:9000"),
    access_key=os.getenv("MINIO_ACCESS_KEY"),
    secret_key=os.getenv("MINIO_SECRET_KEY"),
    secure=False  # Imposta a True se usi HTTPS
)

# Assicurati che il bucket esista all'avvio
bucket_name = os.getenv("MINIO_BUCKET_NAME", "products")
if not minio_client.bucket_exists(bucket_name):
    minio_client.make_bucket(bucket_name)