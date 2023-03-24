import datetime
import json
import httpx
import asyncio

data = {'date' : None,
            'studio_info' : {
                'name' : 'History',
                'adress' : [(['HISTORY', 'FORMA'], 'ул. Пионерская, 4'), ('LOFT', 'ул. Лодыгина, 9')],
                'phone' : '+7 (342) 204-43-80',
                'website' : 'https://history-studios.ru/',
                'workschedule' : {
                    'start' : '9:00',
                    'finish' : '23:00'
                },
                'rooms' : ['HISTORY', 'FORMA', 'LOFT']
            },
            'schedule' : {}
    }

async def get_schedule(date: datetime.date) -> json:
    data['date'] = str(date)
    urls_dict = {
        f'https://appevent.ru/widget/api/event/freetimes/byweek?widget_key=13ece07f3d0f60dafa740fd1f216ab92&hall_id=8072&order_type=&company_id=5806&date={str(date)}' : 'LOFT',
        f'https://appevent.ru/widget/api/event/freetimes/byweek?widget_key=13ece07f3d0f60dafa740fd1f216ab92&hall_id=8070&order_type=&company_id=5806&date={str(date)}' : 'FORMA',
        f'https://appevent.ru/widget/api/event/freetimes/byweek?widget_key=13ece07f3d0f60dafa740fd1f216ab92&hall_id=8071&order_type=&company_id=5806&date={str(date)}' : 'HISTORY'
    }
    responses = []
    for url in urls_dict.keys():
        async with httpx.AsyncClient() as client:
            responses.append(await client.get(url))
    for response in responses:
        response_dict = json.loads(response.content)
        room_name = urls_dict[response.url]
        for event in response_dict['events']:
            if event['date_start'].split()[0] == str(date):
                booking_start_time = _format_time(event['date_start'].split()[1])
                booking_duration = _format_time(str(datetime.timedelta(minutes=int(event['duration']))))
                if room_name not in data['schedule']:
                    data['schedule'][room_name] = [(booking_start_time, booking_duration)]
                else:
                    data['schedule'][room_name].append((booking_start_time, booking_duration))
    return json.dumps(data, ensure_ascii=False)


def _format_time(time : str) -> str:
    return ':'.join(time.split(':')[:-1])


if __name__ == "__main__":
    print(asyncio.run(get_schedule(datetime.date(2023, 2, 6))))

