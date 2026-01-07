from fastapi import APIRouter, Body, HTTPException, status, Depends, Request
from database.connection import get_session
from models.events import Event, EventUpdate
from typing import List
from sqlmodel import select

event_router = APIRouter(
    tags=["events"]
)
events = []

@event_router.get("/", response_model=List[Event])
async def retrieve_all_events(session = Depends(get_session)) -> List[Event]:
    statement = select(Event)
    return session.exec(statement).all()

@event_router.get("/{id}", response_model=Event)
async def retrieve_event(id: int, session = Depends(get_session)) -> Event:
    statement = select(Event).where(Event.id == id)
    event = session.exec(statement).first()
    if not event:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Event not found")
    return event

@event_router.post("/new")
async def create_event(new_event:Event, session = Depends(get_session)) -> dict:
    session.add(new_event)
    session.commit()
    session.refresh(new_event)
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
@event_router.delete("/delete/{id}")
async def delete_event(id: int, session = Depends(get_session)) -> dict:
    event = session.get(Event, id)
    if event:
        session.delete(event)
        session.commit()
        return {
            "message": "Event deleted successfully"
        }
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Event not found")


@event_router.delete("/")
async def delete_all_events() -> dict:
    events.clear()
    return {
        "message": "All events deleted successfully"
    }

@event_router.put("/edit/{id}", response_model=Event)
async def update_event(id: int, event_update: EventUpdate, session = Depends(get_session)) -> Event:
    statement = select(Event).where(Event.id == id)
    event = session.exec(statement).first()
    if not event:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Event not found")

    # Update fields if provided
    for field, value in event_update.model_dump(exclude_unset=True).items():
        setattr(event, field, value)

    session.add(event)
    session.commit()
    session.refresh(event)
    return event
    