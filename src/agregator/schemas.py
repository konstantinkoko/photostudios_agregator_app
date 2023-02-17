
from datetime import datetime, date, time, timedelta
from typing import Dict, List
from pydantic import AnyHttpUrl, BaseModel


class Query(BaseModel):
    date: date
    filter_list: List[str]


class WorkSchedule(BaseModel):
    start: time
    finish: time


class StudioInfo(BaseModel):
    name: str
    adress: str
    phone : str
    website: AnyHttpUrl
    workschedule: WorkSchedule
    rooms: List[str]


class Schedule(BaseModel):
    date: date
    studios_info: Dict[str, StudioInfo]
    schedule: Dict[time, Dict[str, Dict[str, timedelta]]]
    warning_mode: bool