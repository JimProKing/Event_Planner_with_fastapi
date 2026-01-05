from pydantic import BaseModel
# from typing import List - 구형 파이썬에서는 이걸로 해야함. (현재는 list[str] 사용 가능)

class Event(BaseModel):
    id: int          # 식별자
    title: str       # 이벤트 제목
    image: str       # 이미지 url
    description: str # 이벤트 설명
    tags: list[str]  # 그룹화를 위한 이벤트 태그
    location: str    # 이벤트 장소

    # Pydantic v2 방식: class Config 대신 model_config 사용
    model_config = {
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