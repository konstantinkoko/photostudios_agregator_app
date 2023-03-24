import httpx
import asyncio
from bs4 import BeautifulSoup
import datetime
import json

data = {
        'date' : None,
        'studio_info' : {
            'name' : 'Prestige',
            'adress' : 'ул. Дружбы 34/a',
            'phone' : '+7 (342) 234-20-40',
            'website' : 'https://www.prestigeperm.ru/',
            'workschedule' : {
                'start' : '9:00',
                'finish' : '22:00'
            },
            'rooms' : ['MEGA', 'MANHATTAN', 'CRYSTAL', 'GEOMETRIA',	'MARS',	'ULTRA']
        },
        'schedule' : {}
    }

async def get_schedule(date: datetime.date) -> json:
    data['date'] = str(date)
    url = 'https://www.prestigeperm.ru/index.php/index.php?option=com_rsappt_pro3&controller=ajax&task=ajax_gad2&format=raw&gridstarttime=9:00&gridendtime=22:00&category=1&mode=single_day&resource=0&reg=No'
    params = {
        'grid_date' : str(date)
    }
#   <a href="#" onclick="addtoNotificationList('3','2023-01-12','13:00:00');return false;">
#       <div class="sv_gad_timeslot_booked_timeony" style="width:108px; left:655.65px; top:245px; height:97px; position:absolute; text-align:center;">
#           <img alt="" src="https://www.prestigeperm.ru/components/com_rsappt_pro3/publish_rez.png" style="padding-top:38.5px">
#       </div>
#   </a>
    async with httpx.AsyncClient() as client:
            response = await client.get(url,  params=params)
    soup = BeautifulSoup(response.content, 'html.parser')
    result = soup.find_all('a', href='#')
    # room_name = data['studio_info']['rooms'][0]
    for elem in result:
        if 'addtoNotificationList' not in elem['onclick']:
            room_name = elem['onclick'].split('|')[1]
        else:
            booking_start_time = _format_time(elem['onclick'].split("'")[5])
            if not (date == datetime.date.today and datetime.now() > datetime.datetime.strptime(booking_start_time, "%H:%M:%S")):
                booking_duration = _format_time(str(round(int(elem.find(class_='sv_gad_timeslot_booked_timeony')['style'].split(';')[3].split(':')[1][:-2])/25)*datetime.timedelta(minutes=30)))
                if room_name not in data['schedule']:
                    data['schedule'][room_name] = [(booking_start_time, booking_duration)]
                else:
                    data['schedule'][room_name].append((booking_start_time, booking_duration))
    
    return json.dumps(data, ensure_ascii=False)


def _format_time(time : str) -> str:
    return ':'.join(time.split(':')[:-1])


if __name__ == "__main__":
    print(asyncio.run(get_schedule(datetime.date(2023, 3, 3))))


