
from datetime import date, time, timedelta
from fastapi import Form
from pydantic import AnyHttpUrl, BaseModel, validator

class BaseQuery(BaseModel):
    picked_date: date
    filter_list: list[str]

    @validator("picked_date")
    def ensure_date_range(cls, picked_date):
        if not date.today() <= picked_date:
            raise ValueError("Must be in range")
        return picked_date


class Query(BaseQuery):
    def __init__(self, picked_date: date = Form(...), filter_list: list = Form(...)):
        super().__init__(picked_date=picked_date, filter_list=filter_list)


class WorkSchedule(BaseModel):
    start: time
    finish: time


class StudioInfo(BaseModel):
    name: str
    adress: str | list
    phone : str
    website: AnyHttpUrl
    workschedule: WorkSchedule
    rooms: list[str]


class Schedule(BaseModel):
    date: date
    studios_info: dict[str, StudioInfo]
    schedule: dict[time, dict[str, dict[str, timedelta]]]
    warning_mode: bool
