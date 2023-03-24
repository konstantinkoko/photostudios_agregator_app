from ics import Calendar, timeline
import httpx
import arrow, datetime
import json
import asyncio

time_zone = 'Asia/Yekaterinburg'

data = {'date' : None,
            'studio_info' : {
                'name' : 'Ирис',
                'adress' : '25 Октября ул. 17, кв. 76',
                'phone' : '+7 (922) 646-88-80',
                'website' : 'https://vk.com/permiris',
                'workschedule' : {
                    'start' : '09:00',
                    'finish' : '22:00'
                },
                'rooms' : ['Ирис']
            },
            'schedule' : {}
    }

async def get_schedule(date: datetime.date) -> json:
    data['date'] = str(date)
    urls_dict = {
        f'https://calendar.google.com/calendar/ical/8j8noi3iav91oh00gltem784r0@group.calendar.google.com/public/basic.ics' : 'Ирис'
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
    print(asyncio.run(get_schedule(datetime.date(2023, 2, 15))))