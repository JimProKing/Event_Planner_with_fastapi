from fastapi import APIRouter, Body, HTTPException, status, Depends, Request
from database.connection import Database
from models.events import Event, EventUpdate
from typing import List
from sqlmodel import select
from beanie import PydanticObjectId
event_database = Database(Event)

event_router = APIRouter(
    tags=["events"]
)
events = []

@event_router.get("/", response_model=List[Event])
async def retrieve_all_events() -> List[Event]:
    events = await event_database.get_all()
    return events

@event_router.get("/{id}", response_model=Event)
async def retrieve_event(id: PydanticObjectId) -> Event:
    event = await event_database.get(id)
    if not event:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Event not found")
    return event

@event_router.post("/new")
async def create_event(body:Event) -> dict:
    await event_database.save(body)
    return {
        "message": "Event created successfully",
        "event": new_event
    }
# async def create_event(body: Event = Body(...)) -> dict:
#     events.append(body)
#     return {
#         "message": "Event created successfully",
#         "event": body
#     }

# @event_router.delete("/{id}")
# async def delete_event(id: int) -> dict:
#     for event in events:
#         if event.id == id:
#             events.remove(event)
#             return {
#                 "message": "Event deleted successfully"
#             }
#     raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Event not found")
@event_router.delete("/{id}")
async def delete_event(id: PydanticObjectId) -> dict:
    event = await event_database.delete(id)
    if not event:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Event not found")
    return {
        "message":"Event Deleted successfully"
    }


@event_router.delete("/")
async def delete_all_events() -> dict:
    events.clear()
    return {
        "message": "All events deleted successfully"
    }

@event_router.put("/{id}", response_model=Event)
async def update_event(id: PydanticObjectId, body: EventUpdate) -> Event:
    update_event = await event_database.update(id,body)
    if not update_event:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Event not found")

    # # Update fields if provided
    # for field, value in event_update.model_dump(exclude_unset=True).items():
    #     setattr(event, field, value)

    # session.add(event)
    # session.commit()
    # session.refresh(event)
    return update_event
    