import pytest
from unittest.mock import AsyncMock, MagicMock, patch
from sqlalchemy import select
from services.category_service import CategoryService
from models.category import CategoryModelAlchemy


@pytest.mark.asyncio
async def test_list_categories_service():
    # 1. Setup mock session
    mock_session = AsyncMock()

    # 2. Setup mock result chain
    mock_result = MagicMock()
    mock_result.scalars.return_value.all.return_value = [
        CategoryModelAlchemy(id=1, name="Elettronica"),
        CategoryModelAlchemy(id=2, name="Casa")
    ]

    # 3. CORREZIONE: Assegna il return_value alla coroutine del mock
    # Quando chiami await session.execute(...), otterrai mock_result
    mock_session.execute.return_value = mock_result

    # 4. Fai in modo che il context manager ritorni la nostra sessione
    # Quando fai 'async with AsyncSessionLocal()', deve ritornare mock_session
    mock_context = MagicMock()
    mock_context.__aenter__.return_value = mock_session

    # Patching: assicurati che il path sia quello corretto dove il service importa AsyncSessionLocal
    with patch("services.category_service.AsyncSessionLocal", return_value=mock_context):
        results = await CategoryService.list_categories()