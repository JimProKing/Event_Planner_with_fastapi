# tests/conftest.py
import pytest
import pytest_asyncio
import httpx
from beanie import init_beanie
from motor.motor_asyncio import AsyncIOMotorClient

from main import app
from models.events import Event
from models.users import User

# pytest-asyncio 설정 (필요 시 pytest.ini에 asyncio_mode = auto 추가)
pytest_plugins = "pytest_asyncio.plugin"


@pytest_asyncio.fixture(scope="session", autouse=True)
async def setup_test_db():
    """
    모든 테스트 전에 테스트용 DB 초기화
    autouse=True → 자동으로 모든 테스트에 적용
    """
    # 테스트 전용 DB URL (실제 DB와 분리!)
    TEST_DB_URL = "mongodb://localhost:27017/test_event_planner"

    client = AsyncIOMotorClient(TEST_DB_URL)
    
    # Beanie 초기화 (책에서 initialize_database()가 하는 일)
    await init_beanie(
        database=client.get_default_database(),
        document_models=[Event, User]
    )

    yield   # ← 여기서 실제 테스트들이 실행됨

    # 테스트 끝난 후 정리 (좋은 습관)
    await Event.find_all().delete()
    await User.find_all().delete()
    client.close()


@pytest_asyncio.fixture(scope="session")
async def client(setup_test_db):
    """httpx AsyncClient fixture"""
    async with httpx.AsyncClient(
        app=app,
        base_url="http://test"   # "http://app" 대신 "http://test" 추천
    ) as c:
        yield c