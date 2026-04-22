
# Third party modules
from fastapi import APIRouter, Depends
from enum import Enum

# Local modules
from config.setup import config
from models.product import Product, ProductQueryParams, ProductCreate
from services.product_service import ProductService
from starlette.responses import JSONResponse

router = APIRouter(
    tags=['api','products'],
    responses={404: {"description": "Page not found"}},
    prefix='/api/v1/products'
)
class ProductSort(str, Enum):
    price_asc = "price_asc"
    price_desc = "price_desc"
    newest = "created_at_desc"
    oldest = "created_at_asc"

@router.get('/get_by_id/{product_id}')
async def get_by_id(product_id):
    service = ProductService()
    status, res = await service.get_by_id(product_id)

    return JSONResponse(status_code=status, content=res)

@router.get('/list')
async def list_products(params: ProductQueryParams = Depends()):
    service = ProductService()
    status, res = await service.list(params)
    return JSONResponse(status_code=status, content=res)

@router.post('/create')
async def create(product: ProductCreate):
    service = ProductService()
    status, res = await service.create_product(product)

    return JSONResponse(status_code=status, content=res)

@router.put('/update/{product_id}')
async def update(product_id, product: ProductCreate):
    service = ProductService()
    status, res = await service.update_product(product_id, product)

    return JSONResponse(status_code=status, content=res)

@router.delete('/delete/{product_id}')
async def delete(product_id):
    service = ProductService()
    status, res = await service.delete(product_id)

    return JSONResponse(status_code=status, content=res)
