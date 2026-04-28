import asyncio
import random
import os
import io
import json
import httpx  # Per scaricare le immagini
from minio import Minio
from sqlalchemy import select, func

from config.database import AsyncSessionLocal, get_engine
from models.product import BaseAlchemy, ProductModelAlchemy
from models.category import CategoryModelAlchemy

# --- CONFIGURAZIONE ---
MINIO_ENDPOINT = os.getenv("MINIO_ENDPOINT", "minio:9000")
MINIO_USER = os.getenv("MINIO_ROOT_USER", "admin")
MINIO_PASS = os.getenv("MINIO_ROOT_PASSWORD", "password")
BUCKET_NAME = "products"

# Mappatura per immagini rappresentative (traduzione per il servizio immagini)
CAT_KEYWORDS = {
    "Elettronica": "technology,gadget",
    "Casa": "interior,furniture",
    "Sport": "fitness,sport",
    "Abbigliamento": "fashion,clothes",
    "Libri": "books,library",
    "Giocattoli": "toys",
    "Motori": "car,engine",
    "Giardinaggio": "garden,plants",
    "Fai da te": "tools,diy",
    "Alimentari": "food,grocery"
}

minio_client = Minio(MINIO_ENDPOINT, access_key=MINIO_USER, secret_key=MINIO_PASS, secure=False)


def setup_minio():
    if not minio_client.bucket_exists(BUCKET_NAME):
        minio_client.make_bucket(BUCKET_NAME)
        policy = {
            "Version": "2012-10-17",
            "Statement": [{"Effect": "Allow", "Principal": {"AWS": ["*"]}, "Action": ["s3:GetObject"],
                           "Resource": [f"arn:aws:s3:::{BUCKET_NAME}/*"]}]
        }
        minio_client.set_bucket_policy(BUCKET_NAME, json.dumps(policy))


async def download_and_upload_image(category_name, object_name):
    """Scarica un'immagine in RAM e la carica su MinIO."""
    keyword = CAT_KEYWORDS.get(category_name, "object")
    # Usiamo LoremFlickr perché permette di filtrare per parola chiave
    url = f"https://loremflickr.com/600/600/{keyword}"

    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url, follow_redirects=True, timeout=10.0)
            if response.status_code == 200:
                img_data = response.content
                # Caricamento diretto da memoria (RAM)
                minio_client.put_object(
                    BUCKET_NAME,
                    object_name,
                    io.BytesIO(img_data),
                    length=len(img_data),
                    content_type=response.headers.get("content-type", "image/jpeg")
                )
                return f"{object_name}"
        except Exception as e:
            print(f"Errore download immagine per {category_name}: {e}")
    return None


async def seed_db():
    print("Avvio Seeding con immagini reali...")
    engine = get_engine()
    async with engine.begin() as conn:
        await conn.run_sync(BaseAlchemy.metadata.create_all)

    async with AsyncSessionLocal() as session:
        # Controllo se il DB è già popolato
        check = await session.execute(select(func.count()).select_from(CategoryModelAlchemy))
        if check.scalar() > 0:
            print("Database già popolato.")
            return

        setup_minio()

        # 1. Creazione Categorie
        categories = []
        for name in CAT_KEYWORDS.keys():
            c = CategoryModelAlchemy(name=name)
            session.add(c)
            categories.append(c)
        await session.commit()

        # 2. Creazione 100 Prodotti
        print(f"Download e upload di 100 immagini in corso...")
        for cat in categories:
            await session.refresh(cat)
            tasks = []
            for i in range(10):
                obj_name = f"cat_{cat.id}_prod_{i}.jpg"
                # Usiamo asyncio.gather per velocizzare i download se vuoi,
                # ma qui andiamo sequenziali per non sovraccaricare la rete
                image_url = await download_and_upload_image(cat.name, obj_name)

                p = ProductModelAlchemy(
                    name=f"{cat.name} Special {i + 1}",
                    price=round(random.uniform(10, 1000), 2),
                    category_id=cat.id,
                    tags=[cat.name.lower(), "bestseller"],
                    image_url=image_url
                )
                session.add(p)
            print(f"   - Categoria {cat.name} completata.")
            await session.commit()

    print("Seed completato! 100 prodotti con immagini reali pronti su MinIO.")


if __name__ == "__main__":
    asyncio.run(seed_db())