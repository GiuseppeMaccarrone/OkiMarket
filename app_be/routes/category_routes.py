from fastapi import APIRouter, status
from models.category import CategoryCreate, Category
from services.category_service import CategoryService

router = APIRouter(
    tags=['api','categories'],
    responses={404: {"description": "Page not found"}},
    prefix='/api/v1/categories'
)

@router.post("/create", response_model=Category, status_code=status.HTTP_201_CREATED)
async def create_category(category_data: CategoryCreate):
    """Crea una nuova categoria."""
    return await CategoryService.create_category(category_data)

@router.get("/list", response_model=list[Category])
async def list_categories():
    """Restituisce la lista di tutte le categorie."""
    return await CategoryService.list_categories()

@router.get("/{category_id}", response_model=Category)
async def get_category(category_id: int):
    """Recupera i dettagli di una singola categoria."""
    return await CategoryService.get_category(category_id)

@router.put("/update/{category_id}", response_model=Category)
async def update_category(category_id: int, category_data: CategoryCreate):
    """Aggiorna il nome di una categoria esistente."""
    return await CategoryService.update_category(category_id, category_data)

@router.delete("/delete/{category_id}", status_code=status.HTTP_200_OK)
async def delete_category(category_id: int):
    """
    Elimina una categoria.
    Fallisce se ci sono prodotti associati a questa categoria.
    """
    return await CategoryService.delete_category(category_id)