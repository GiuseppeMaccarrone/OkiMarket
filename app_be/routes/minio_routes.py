from fastapi import APIRouter, HTTPException
from datetime import timedelta
from config.minio_client import minio_client, bucket_name

router = APIRouter(
    tags=['api','categories'],
    responses={404: {"description": "Page not found"}},
    prefix='/api/v1/storage'
)

@router.get("/presigned-url")
async def get_presigned_url(file_name: str):
    try:
        # Genera un URL che scade in 10 minuti
        url = minio_client.presigned_put_object(
            bucket_name,
            file_name,
            expires=timedelta(minutes=10)
        )
        return {"url": url}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))