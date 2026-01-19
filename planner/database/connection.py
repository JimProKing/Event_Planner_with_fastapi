from typing import Any, List, Optional

from beanie import init_beanie, PydanticObjectId
from motor.motor_asyncio import AsyncIOMotorClient
from pydantic import BaseModel
from pydantic_settings import BaseSettings, SettingsConfigDict

from models.events import Event
from models.users import User


class Settings(BaseSettings):
    """
    애플리케이션 설정 관리 (환경변수 + .env 파일 로드)
    """
    SECRET_KEY: Optional[str] = None
    DATABASE_URL: Optional[str] = None

    model_config = SettingsConfigDict(
        env_file=".env",              # .env 파일 자동 로드
        env_file_encoding="utf-8",
        case_sensitive=False,         # 환경변수 대소문자 구분 안 함 (기본값)
        extra="ignore",               # .env에 불필요한 키 무시
    )

    async def initialize_database(self) -> None:
        """Beanie 초기화 (MongoDB 연결 + Document 모델 등록)"""
        if not self.DATABASE_URL:
            raise ValueError("DATABASE_URL이 설정되지 않았습니다. .env 또는 환경변수를 확인하세요.")

        client = AsyncIOMotorClient(self.DATABASE_URL)
        await init_beanie(
            database=client.get_default_database(),
            document_models=[Event, User]
        )


class Database:
    """
    Beanie 기반의 제네릭 CRUD 헬퍼 클래스
    """
    def __init__(self, model):
        self.model = model

    async def save(self, document) -> None:
        """문서 저장 (create)"""
        await document.create()

    async def get(self, id: PydanticObjectId) -> Optional[Any]:
        """ID로 단일 문서 조회 (없으면 None)"""
        return await self.model.get(id)

    async def get_all(self) -> List[Any]:
        """모든 문서 조회"""
        return await self.model.find_all().to_list()

    async def update(self, id: PydanticObjectId, body: BaseModel) -> Any:
        """
        ID로 문서 업데이트 (body에 있는 필드만 $set)
        - None 값은 업데이트에서 제외
        """
        doc = await self.get(id)
        if not doc:
            return False

        update_data = body.model_dump(exclude_unset=True, exclude_none=True)
        # 또는 dict() + 필터링 (pydantic v2에서는 model_dump 추천)
        # update_data = {k: v for k, v in body.dict().items() if v is not None}

        if not update_data:
            return doc  # 변경할 게 없으면 그대로 반환

        await doc.set(update_data)  # Beanie의 set() 메서드 사용 (더 안전)
        # 또는 await doc.update({"$set": update_data})

        return doc

    async def delete(self, id: PydanticObjectId) -> bool:
        """ID로 문서 삭제"""
        doc = await self.get(id)
        if not doc:
            return False

        await doc.delete()
        return True