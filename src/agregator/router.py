from fastapi import APIRouter
from agregator.photostudios_parcer.studios_manager import StudiosManager
from agregator.schemas import Query, Schedule



router = APIRouter(
    prefix="/get_schedule",
)


@router.post("/", response_model=Schedule)
async def get_schedule(query: Query):
    manager = StudiosManager()
    schedule = await manager.get_schedule(query)
    return schedule
