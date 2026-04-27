import os
from minio import Minio
import json # Import necessario

minio_client = Minio(
    os.getenv("MINIO_ENDPOINT", "minio:9000"),
    access_key=os.getenv("MINIO_ACCESS_KEY"),
    secret_key=os.getenv("MINIO_SECRET_KEY"),
    secure=False
)

bucket_name = os.getenv("MINIO_BUCKET_NAME", "products")

# Assicurati che il bucket esista
if not minio_client.bucket_exists(bucket_name):
    minio_client.make_bucket(bucket_name)

# Imposta la policy del bucket come pubblica in lettura (Read-Only)
public_policy = {
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Principal": {"AWS": ["*"]},
            "Action": ["s3:GetBucketLocation", "s3:ListBucket"],
            "Resource": [f"arn:aws:s3:::{bucket_name}"],
        },
        {
            "Effect": "Allow",
            "Principal": {"AWS": ["*"]},
            "Action": ["s3:GetObject"],
            "Resource": [f"arn:aws:s3:::{bucket_name}/*"],
        },
    ],
}

minio_client.set_bucket_policy(bucket_name, json.dumps(public_policy))
