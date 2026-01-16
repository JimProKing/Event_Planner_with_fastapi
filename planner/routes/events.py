from typing import List
from auth.authenticate import authenticate
from beanie import PydanticObjectId
from database.connection import Database
from fastapi import APIRouter, HTTPException, status, Depends
from models.events import Event, EventUpdate

event_router = APIRouter(
    tags=["Events"]
)

event_database = Database(Event)


@event_router.get("/", response_model=List[Event])
async def retrieve_all_events() -> List[Event]:
    events = await event_database.get_all()
    return events


@event_router.get("/{id}", response_model=Event)
async def retrieve_event(id: PydanticObjectId) -> Event:
    event = await event_database.get(id)
    if not event:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Event with supplied ID does not exist"
        )
    return event


@event_router.post("/new")
async def create_event(body: Event, user:str = Depends(authenticate)) -> dict:
    body.creator = user
    await event_database.save(body)
    return {
        "message": "Event created successfully"
    }


@event_router.put("/{id}", response_model=Event)
async def update_event(
    id: PydanticObjectId,
    body: EventUpdate,
    user: str = Depends(authenticate)
) -> Event:
    event = await event_database.get(id)
    
    if event is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Event not found"
        )
    
    # creator 비교
    # user가 문자열(이메일 등)이고 event.creator도 문자열이라고 가정
    if event.creator != user:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Operation not allowedzzzz"
        )
    
    # 부분 업데이트
    update_data = body.dict(exclude_unset=True)
    await event.set(update_data)
    
    # 필요하면 최신 상태 다시 불러오기 (선택)
    # await event.fetch_all_links()
    
    return event
    # updated_event = await event_database.update(id, body)
    # if not updated_event:
    #     raise HTTPException(
    #         status_code=status.HTTP_404_NOT_FOUND,
    #         detail="Event with supplied ID does not exist"
    #     )
    # return updated_event


@event_router.delete("/{id}")
async def delete_event(id: PydanticObjectId, user:str=Depends(authenticate)) -> dict:
    event_val = await event_database.get(id)
    if not event_val:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Event with supplied ID does not exist"
        )
    if event_val.creator != user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="NOT ALLOWED"
        )
    #6966287ff8e0df9c9e056b72
    event = await event_database.delete(id)
    return {
        "message": "Event deleted successfully."
    }
