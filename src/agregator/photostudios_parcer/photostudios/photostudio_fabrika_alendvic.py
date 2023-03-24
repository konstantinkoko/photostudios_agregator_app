import httpx
import datetime
import json
import asyncio

data = {'date' : None,
            'studio_info' : {
                'name' : 'Фабрика Алендвик',
                'adress' : 'Петропавловская улица, 39',
                'phone' : '+7 (919) 441-81-19',
                'website' : 'https://alendvic-foto.ru',
                'workschedule' : {
                    'start' : '09:00',
                    'finish' : '22:00'
                },
                'rooms' : ['Фабрика звёзд', 'Цех', 'Балюстрада', 'Торжественный', 'Детский']
            },
            'schedule' : {}
    }

async def get_schedule(date: datetime.date) -> json:
    data['date'] = str(date)
    urls_dict = {
        f'https://appevent.ru/widget/api/event/freetimes?widget_key=2f77a3a49309d19dcdea472fa06366a7&hall_id=7969&order_type=&company_id=5734&date={str(date)}' : 'Фабрика звёзд',
        f'https://appevent.ru/widget/api/event/freetimes?widget_key=2f77a3a49309d19dcdea472fa06366a7&hall_id=7970&order_type=&company_id=5734&date={str(date)}' : 'Цех',
        f'https://appevent.ru/widget/api/event/freetimes?widget_key=2f77a3a49309d19dcdea472fa06366a7&hall_id=8734&order_type=&company_id=5734&date={str(date)}' : 'Балюстрада',
        f'https://appevent.ru/widget/api/event/freetimes?widget_key=2f77a3a49309d19dcdea472fa06366a7&hall_id=8735&order_type=&company_id=5734&date={str(date)}' : 'Торжественный',
        f'https://appevent.ru/widget/api/event/freetimes?widget_key=2f77a3a49309d19dcdea472fa06366a7&hall_id=9677&order_type=&company_id=5734&date={str(date)}' : 'Детский',
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
    print(asyncio.run(get_schedule(datetime.date(2023, 2, 28))))