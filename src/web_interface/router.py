from datetime import date, datetime
from fastapi import APIRouter, Depends, Form, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse

from agregator.router import get_studios_list, get_schedule
from agregator.schemas import Query, Schedule


router = APIRouter()

router.mount("/static", StaticFiles(directory="web_interface/static"), name="static")
templates = Jinja2Templates(directory="web_interface/templates")


@router.post("/", response_class=HTMLResponse)
async def date_picker(request: Request):
    current_date = datetime.date.today()
    studios_list = await get_studios_list()
    return templates.TemplateResponse("date_picker.html", {
        "request": request,
        "current_date": current_date,
        "studios_info": studios_list
    })


@router.post("/schedule/{date}", response_class=HTMLResponse)
async def get_schedule(request: Request, date: date, query: Query):
    schedule = await get_schedule(query)
    return templates.TemplateResponse("schedule.html", {
        "request": request,
        "schedule": schedule
    })


@router.post("/schedule/{date}/{time}", response_class=HTMLResponse)
async def get_time_info(request: Request, date: date, time: str, schedule: Schedule = Form()):
    studios_info = schedule["studios_info"]
    time_info = schedule["schedule"]["time"]
    return templates.TemplateResponse("time_info.html", {
        "request": request,
        "studios_info": studios_info,
        "time_info": time_info,
        "date": date,
        "time": time
    })