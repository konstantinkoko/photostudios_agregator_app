import httpx
import datetime
import json
import asyncio

data = {'date' : None,
            'studio_info' : {
                'name' : 'Flacon',
                'adress' : 'ул. Лодыгина, 9',
                'phone' : '+7 (995) 910-95-90',
                'website' : 'https://vk.com/flaconstudios',
                'workschedule' : {
                    'start' : '9:00',
                    'finish' : '23:59'
                },           
                'rooms' : ['MOON', 'BOHEMIA', 'ГРАНИ', 'BRUT', 'ПЕСОК']
            },
            'schedule' : {}
    }

async def get_schedule(date: datetime.date) -> json:
    data['date'] = str(date)
    urls_dict = {
        f'https://b817933.yclients.com/api/v1/book_times/301824/887616/{str(date)}' : 'MOON',
        f'https://b817933.yclients.com/api/v1/book_times/301824/887617/{str(date)}' : 'BOHEMIA',
        f'https://b817933.yclients.com/api/v1/book_times/301824/2255427/{str(date)}' : 'ГРАНИ',
        f'https://b817933.yclients.com/api/v1/book_times/301824/887619/{str(date)}' : 'BRUT',
        f'https://b817933.yclients.com/api/v1/book_times/301824/2255440/{str(date)}' : 'ПЕСОК' 
    }
    headers = {
        'authorization' : 'Bearer gtcwf654agufy25gsadh'
    }
    responses = []
    for url in urls_dict.keys():
        async with httpx.AsyncClient() as client:
            responses.append(await client.get(url, headers=headers))
    for response in responses:
        response_dict = json.loads(response.text)
        room_name = urls_dict[response.url]
        free_time = []
        for element in response_dict:
            if 'time' in element:
                free_time.append(element['time'])
        events = _get_events(free_time)
        if len(events) > 0:
            data['schedule'][room_name] = events
    return json.dumps(data, ensure_ascii=False)



def _get_events(free_time: list[str]) -> list[tuple]:
    day_time = ['9:00', '9:30', '10:00', '10:30', '11:00', '11:30', '12:00', '12:30', '13:00', '13:30', '14:00', '14:30', '15:00','15:30', '16:00',
                '16:30', '17:00', '17:30', '18:00', '18:30', '19:00', '19:30', '20:00', '20:30', '21:00', '21:30', '22:00', '22:30', '23:00', '23:30']
    events = []
    for time in free_time:
        current_time = day_time.pop(0)
        if time != current_time:
            start_time = current_time
            duration_minutes = 0
            while time != current_time:
                current_time = day_time.pop(0)
                duration_minutes += 30
            events.append((start_time, ':'.join(str(datetime.timedelta(minutes=duration_minutes)).split(':')[:-1])))
    return events


if __name__ == "__main__":
    print(asyncio.run(get_schedule(datetime.date(2023, 2, 7))))
    


