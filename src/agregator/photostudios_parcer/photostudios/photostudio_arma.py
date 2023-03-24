import httpx
import datetime
import json
import asyncio

data = {'date' : None,
            'studio_info' : {
                'name' : 'ARMA',
                'adress' : 'Окулова 75 к1 офис 712',
                'phone' : '+7 (996) 325-94-82',
                'website' : 'https://vk.com/arma_photostudio',
                'workschedule' : {
                    'start' : '09:00',
                    'finish' : '23:59'
                },
                'rooms' : ['Светлый', 'Циклорама']
            },
            'schedule' : {}
    }

async def get_schedule(date: datetime.date) -> json:
    data['date'] = str(date)
    urls_dict = {
        f'https://appevent.ru/widget/api/event/freetimes?widget_key=e2a045f844932f412f311e06c038d5d0&hall_id=5273&order_type=&company_id=4040&date={str(date)}' : 'Светлый',
        f'https://appevent.ru/widget/api/event/freetimes?widget_key=e2a045f844932f412f311e06c038d5d0&hall_id=5782&order_type=&company_id=4040&date={str(date)}' : 'Циклорама'
    }
    responses = []
    for url in urls_dict.keys():
        async with httpx.AsyncClient() as client:
            responses.append(await client.get(url))
    for response in responses:
        response_dict = json.loads(response.content)
        room_name = urls_dict[response.url]
        booked_time = []
        for event in response_dict['free_times']:
            if event['status'] != 'free':
                booked_time.append(':'.join(event['date'].split('T')[1].split(':')[:2]))
        events = _get_events(booked_time)
        if len(events) > 0:
            data['schedule'][room_name] = events
    return json.dumps(data, ensure_ascii=False)


def _get_events(booked_time: list[str]) -> list[tuple]:
    if booked_time == []:
        return []
    events = []
    start_time = datetime.datetime.strptime(booked_time.pop(0), '%H:%M').time()
    time_delta = datetime.timedelta(minutes=30)
    duration_minutes = 0
    while len(booked_time) > 0: 
        time = datetime.datetime.strptime(booked_time.pop(0), '%H:%M').time()
        duration_minutes += 30
        if (datetime.datetime.combine(datetime.date.today(), start_time) + time_delta + datetime.timedelta(minutes=duration_minutes-30)).time() != time:
            events.append((_format_time(str(start_time)), _format_time(str(datetime.timedelta(minutes=duration_minutes)))))
            start_time = time
            duration_minutes = 0
    events.append((_format_time(str(start_time)), _format_time(str(datetime.timedelta(minutes=duration_minutes + 30)))))            
    return events


def _format_time(time : str) -> str:
    return ':'.join(time.split(':')[:-1])


if __name__ == "__main__":
    print(asyncio.run(get_schedule(datetime.date(2023, 1, 29))))