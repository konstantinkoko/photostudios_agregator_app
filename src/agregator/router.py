from typing import Dict
from fastapi import APIRouter
from agregator.photostudios_parcer.studios_manager import StudiosManager
from agregator.schemas import Query, Schedule, StudioInfo


router = APIRouter()


@router.post("/get_schedule", response_model=Schedule)
async def get_schedule(query: Query):
    manager = StudiosManager()
    schedule = await manager.get_schedule(query)
    return schedule


@router.post("/get_studios_list", response_model=Dict[str, StudioInfo])
async def get_studios_list():
    return StudiosManager().filter_info_dict