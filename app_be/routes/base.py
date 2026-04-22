
# Third party modules
from fastapi import APIRouter

# Local modules
from config.setup import config

router = APIRouter(
    tags=['api'],
    responses={404: {"description": "Page not found"}},
    prefix='/api/v1/base'
)

@router.get('/')
async def root():
    return {'message': f'Welcome to {config.app_name} service section {router.tags[0].upper()}'}
