from pydantic import BaseModel, EmailStr
from typing import Optional, List
from models.events import Event


class User(BaseModel):
    email: EmailStr        # 사용자 이메일
    password: str          # 사용자 비밀번호
    events: Optional[List[Event]] = None  # 사용자가 등록한 이벤트 목록 (선택 사항)

    # Pydantic v2 호환 (v1 스타일은 경고 남)
    # 연습용이니 v1 방식 유지하되, 예시에서 불필요한 키 제거
    class Config:
        schema_extra = {
            "example": {
                "email": "caramel2516@naver.com",
                "password": "your_secure_password",
                "events": []  # Optional이라 빈 리스트 OK
            }
        }


class UserSignIn(BaseModel):
    email: EmailStr        # 사용자 이메일
    password: str          # 사용자 비밀번호

    class Config:
        schema_extra = {
            "example": {
                "email": "caramel2516@naver.com",
                "password": "your_password"
                # events는 UserSignIn에 없으므로 여기서 넣으면 안 됨!
            }
        }