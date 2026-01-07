from pydantic import BaseModel
# from typing import List - 구형 파이썬에서는 이걸로 해야함. (현재는 list[str] 사용 가능)
from sqlmodel import JSON, SQLModel, Field, Column
from typing import Optional, List

# class Event(BaseModel):
#     id: int          # 식별자
#     title: str       # 이벤트 제목
#     image: str       # 이미지 url
#     description: str # 이벤트 설명
#     tags: list[str]  # 그룹화를 위한 이벤트 태그
#     location: str    # 이벤트 장소

#     # Pydantic v2 방식: class Config 대신 model_config 사용
#     model_config = {
#         "json_schema_extra": {
#             "example": {  # v2에서도 "example" 단일 딕셔너리 사용 가능 (리스트로 감싸도 OK)
#                 "title": "Summer Festival",
#                 "image": "https://example.com/summer-festival.jpg",
#                 "description": (
#                     "Join us for a fun-filled summer festival "
#                     "with music, food, and activities."
#                 ),
#                 "tags": ["festival", "summer", "music"],
#                 "location": "Central Park"
#             }
#         }
#     }

# SQLModel을 사용한 Event 모델 정의
class Event(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)  # 식별자
    title: str = Field(index=True)       # 이벤트 제목
    image: str                          # 이미지 url
    description: str                    # 이벤트 설명
    tags: List[str] = Field(
        sa_column=Column(JSON)          # JSON 컬럼으로 저장
    )                                    # 그룹화를 위한 이벤트 태그
    location: str                       # 이벤트 장소

    # Pydantic v2 방식: class Config 대신 model_config 사용
    model_config = {
        "arbitrary_types_allowed": True,
        "json_schema_extra": {
            "example": {  # v2에서도 "example" 단일 딕셔너리 사용 가능 (리스트로 감싸도 OK)
                "title": "Summer Festival",
                "image": "https://example.com/summer-festival.jpg",
                "description": (
                    "Join us for a fun-filled summer festival "
                    "with music, food, and activities."
                ),
                "tags": ["festival", "summer", "music"],
                "location": "Central Park"
            }
        }
    }

class EventUpdate(SQLModel):
    title: Optional[str] = None                          # 이벤트 제목
    image: Optional[str] = None                          # 이미지 url
    description: Optional[str] = None                    # 이벤트 설명
    tags: Optional[List[str]] = None    # 그룹화를 위한 이벤트 태그
    location: Optional[str] = None             # 이벤트 장소
    class Config:
        schema_extra = {
            "example": {
                "title": "Summer Festival",
                "image": "https://example.com/summer-festival.jpg",
                "description": (
                    "ㅊㅊㅊJoin us for a fun-filled summer festival "
                    "with music, food, and activities."
                ),
                "tags": ["festival", "summer", "music"],
                "location": "Central Park"
            }
        }