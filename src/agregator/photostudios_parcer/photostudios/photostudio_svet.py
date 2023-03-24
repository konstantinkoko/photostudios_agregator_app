import httpx
import datetime
import json
import asyncio

data = {'date' : None,
            'studio_info' : {
                'name' : 'СВЕТ',
                'adress' : 'улица Ленина, 44',
                'phone' : '+7 (965) 563-71-22',
                'website' : 'https://vk.com/svet_studio_perm',
                'workschedule' : {
                    'start' : '00:00',
                    'finish' : '23:59'
                },
                'rooms' : ['СВЕТ']
            },
            'schedule' : {}
    }

async def get_schedule(date: datetime.date) -> json:
    data['date'] = str(date)
    urls_dict = {
        f'https://appevent.ru/widget/api/event/freetimes/byweek?widget_key=3666abd3af01513b18d4e146ad8d804e&hall_id=6759&order_type=&company_id=4948&date={str(date)}' : 'СВЕТ'
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
    print(asyncio.run(get_schedule(datetime.date(2023, 1, 30))))