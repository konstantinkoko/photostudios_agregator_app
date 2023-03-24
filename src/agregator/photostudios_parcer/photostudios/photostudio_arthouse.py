"""https://calendar.yandex.ru/export/ics.xml?private_token=5fefc0e6ff66ae0e20c44f9cac0f99baacc0ba0a&uid=69421049

https://calendar.yandex.ru/embed/week?private_token=5fefc0e6ff66ae0e20c44f9cac0f99baacc0ba0a&tz_id=Asia%2FYekaterinburg&uid=69421049"""


from ics import Calendar, timeline
import httpx
import arrow, datetime
import json
import asyncio

time_zone = 'Asia/Yekaterinburg'

data = {'date' : None,
            'studio_info' : {
                'name' : 'Arthouse',
                'adress' : 'Шоссе Космонавтов, 111, корпус 27, оф. 202',
                'phone' : '+7 (965) 551-41-88',
                'website' : 'https://vk.com/arthouse_photo',
                'workschedule' : {
                    'start' : '07:00',
                    'finish' : '23:59'
                },
                'rooms' : ['Arthouse']
            },
            'schedule' : {}
    }

async def get_schedule(date: datetime.date) -> json:
    data['date'] = str(date)
    urls_dict = {
        f'https://calendar.yandex.ru/export/ics.xml?private_token=5fefc0e6ff66ae0e20c44f9cac0f99baacc0ba0a&uid=69421049' : 'Arthouse',
     }
    responses = []
    for url in urls_dict.keys():
        async with httpx.AsyncClient() as client:
            responses.append(await client.get(url))
    for response in responses:
        room_name = urls_dict[response.url]
        calendar = Calendar(response.text)
        my_timeline = timeline.Timeline(calendar).on(arrow.get(date))
        events = []
        for event in my_timeline:
            event_begin_time = event.begin.to(time_zone).time()
            event_duration = event.duration
            events.append((_format_time(str(event_begin_time)), _format_time(str(event_duration))))
        if len(events) > 0:
            data['schedule'][room_name] = events
    return json.dumps(data, ensure_ascii=False)


def _format_time(time : str) -> str:
    return ':'.join(time.split(':')[:-1])


if __name__ == "__main__":
    print(asyncio.run(get_schedule(datetime.date(2023, 2, 18))))