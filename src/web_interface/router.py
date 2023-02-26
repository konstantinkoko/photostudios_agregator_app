import ast
from datetime import date, time

from fastapi import APIRouter, Form, Request, Depends
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse

from agregator.router import get_studios_list, get_schedule
from agregator.schemas import Query

router = APIRouter()

templates = Jinja2Templates(directory="../templates")


@router.get("/", response_class=HTMLResponse)
async def date_picker(request: Request):
    current_date = date.today()
    studios_list = await get_studios_list()
    return templates.TemplateResponse("date_picker.html", {
        "request": request,
        "current_date": current_date,
        "studios_info": studios_list
    })


@router.post("/schedule/date", response_class=HTMLResponse)
async def get_schedule_page(request: Request, query: Query = Depends()):
    schedule = await get_schedule(query)
    return templates.TemplateResponse("schedule.html", {
        "request": request,
        "schedule": schedule
    })


@router.post("/schedule/{date}/{time}", response_class=HTMLResponse)
async def get_time_info(request: Request, date: date, time: time, studios_info = Form(...), time_info = Form(...)):
    studios_info_dict = ast.literal_eval(studios_info)
    time_info_dict = ast.literal_eval(time_info)
    time_str = time.strftime("%H:%M")
    return templates.TemplateResponse("time_info.html", {
        "request": request,
        "studios_info": studios_info_dict,
        "time_info": time_info_dict,
        "date": date,
        "time": time_str
    })