import pytest
from unittest.mock import AsyncMock, MagicMock, patch
from services.category_service import CategoryService
from models.category import CategoryModelAlchemy


@pytest.mark.asyncio
async def test_list_categories_empty():
    """Test quando non ci sono categorie nel database."""
    mock_session = AsyncMock()
    mock_result = MagicMock()
    # Simuliamo una lista vuota
    mock_result.scalars.return_value.all.return_value = []
    mock_session.execute.return_value = mock_result

    mock_context = MagicMock()
    mock_context.__aenter__.return_value = mock_session

    with patch("services.category_service.AsyncSessionLocal", return_value=mock_context):
        results = await CategoryService.list_categories()
        assert results == []
        assert len(results) == 0


@pytest.mark.asyncio
async def test_list_categories_db_error():
    """Test che gestisce un errore generico del database durante la lista."""
    mock_session = AsyncMock()
    # Simuliamo un errore nell'esecuzione della query
    mock_session.execute.side_effect = Exception("DB Error")

    mock_context = MagicMock()
    mock_context.__aenter__.return_value = mock_session

    with patch("services.category_service.AsyncSessionLocal", return_value=mock_context):
        # Ci aspettiamo che il service sollevi l'errore o che il middleware lo gestisca
        with pytest.raises(Exception, match="DB Error"):
            await CategoryService.list_categories()