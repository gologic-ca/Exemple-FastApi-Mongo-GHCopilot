from unittest.mock import AsyncMock, MagicMock

import pytest
from core.article import build_get_articles_query


@pytest.fixture
def engine():
    return AsyncMock()


@pytest.mark.asyncio
async def test_build_get_articles_query_with_author(engine):
    author = "test_author"
    engine.find_one.return_value = AsyncMock(id="test_author_id")
    query = await build_get_articles_query(engine, author, None, None)
    assert query["$and"][1] == {"author": {"$eq": "test_author_id"}}


@pytest.mark.asyncio
async def test_build_get_articles_query_with_tag(engine):
    tag = "test_tag"
    query = await build_get_articles_query(engine, None, None, tag)
    assert query["$and"][1] == {"tag_list": {"$elemMatch": {"$eq": "test_tag"}}}


@pytest.mark.asyncio
async def test_build_get_articles_query_with_favorited(engine):
    favorited = "test_user"
    engine.find_one.return_value = MagicMock(id="test_user_id")
    query = await build_get_articles_query(engine, None, favorited, None)
    assert query["$and"][1] == {
        "favorited_user_ids": {"$elemMatch": {"$eq": "test_user_id"}}
    }


@pytest.mark.asyncio
async def test_build_get_articles_query_with_invalid_author(engine):
    author = "invalid_author"
    engine.find_one.return_value = None
    query = await build_get_articles_query(engine, author, None, None)
    assert query is None


@pytest.mark.asyncio
async def test_build_get_articles_query_with_invalid_favorited(engine):
    favorited = "invalid_user"
    engine.find_one.return_value = None
    query = await build_get_articles_query(engine, None, favorited, None)
    assert query is None
