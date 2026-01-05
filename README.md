# 기본 개념
**1. SQLModel 테이블 정의**
```py
class Event(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str
    image: str
    description: str
    location: str
    tags: List[str]
```

**2. row 정의**
```py
new_event = Event(title="Book Launch",
    image="src/fastapi.png",
    description="The book launch event will
 be held at Packt HQ, Packt city",
    location="Google Meet",
    tags=["packt", "book"])"
```

**3. 세션 정의**
```py
with Session(engine) as session:
    session.add(new_event)
    session.commit( )
 ```
> [!TIP]
> session 클래스의 메서드
> 
> 1. ```add()``` : 메모리에 추가
> 2. ```commit()``` : 트랜잭션 정리
> 3. ```get()``` : 단일 로우 추출

