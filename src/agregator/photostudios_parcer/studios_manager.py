import importlib
import datetime
from agregator.schemas import Query, Schedule
import agregator.photostudios_parcer.photostudios as photostudios
import json


class StudiosManager:

    def __init__(self) -> None:
        self.studios_list = sorted(photostudios.studios_list)
        self.filter_list = []
        self.filter_info_dict = {}
        for studio in self.studios_list:
            studio = importlib.import_module(f"agregator.photostudios_parcer.photostudios.{studio}")
            self.filter_info_dict[studio.data['studio_info']['name']] = studio.data['studio_info']
        self.data = {}

    
    async def get_schedule(self, query: Query) -> Schedule:
        self.filter_list = query.filter_list
        data_json = await self._get_studios_data_list(query.date)
        data = [json.loads(studio) for studio in data_json]
        self.data = self._format_data(data)
        self.data["warning_mode"] = True if query.date == datetime.date.today() else False
        self.data["date"] = query.date
        return self.data

    async def _get_studios_data_list(self, date : datetime.date) -> list:
        studios_data_list = []
        for studio_name in self.studios_list:
            studio = importlib.import_module(f"agregator.photostudios_parcer.photostudios.{studio_name}")
            if studio.data['studio_info']['name'] in self.filter_list:
                studios_data_list.append(await studio.get_schedule(date))
        return studios_data_list

    def get_free_studios_count(self) -> dict:
        free_studios_count = {}
        for time in self.data['schedule']:
            free_studios_count[time] = len(self.data['schedule'][time])
        return free_studios_count
    
    def _get_filtered_data(self, data : list[dict]) -> list:
        filtered_data = []
        for studio in data:
            if studio['studio_info']['name'] in self.filter_list:
                filtered_data.append(studio)
        return filtered_data
    
    def _format_data(self, data_list : list) -> dict:
        day_time = ['0:00', '0:30', '1:00', '1:30', '2:00', '2:30', '3:00', '3:30', '4:00', '4:30', '5:00', '5:30', '6:00','6:30', '7:00', '7:30', '8:00',
                '8:30', '9:00', '9:30', '10:00', '10:30', '11:00', '11:30', '12:00', '12:30', '13:00', '13:30', '14:00', '14:30', '15:00','15:30', '16:00',
                '16:30', '17:00', '17:30', '18:00', '18:30', '19:00', '19:30', '20:00', '20:30', '21:00', '21:30', '22:00', '22:30', '23:00', '23:30']
        total_schedule = {
            'date' : None,
            'studios_info' : {},
            'schedule' : {},
            'warning_mode' : False
        }
        schedule = {}
        for time in day_time:
            schedule[time] = {}
        for studio in data_list:
                total_schedule['studios_info'][studio['studio_info']['name']] = studio['studio_info']
                studio_start_working_time = studio['studio_info']['workschedule']['start']
                studio_end_working_time = studio['studio_info']['workschedule']['finish']
                for time in day_time:
                    if datetime.datetime.strptime(studio_end_working_time, '%H:%M') > datetime.datetime.strptime(time, '%H:%M') >= datetime.datetime.strptime(studio_start_working_time, '%H:%M'):
                        schedule[time][studio['studio_info']['name']] = set(studio['studio_info']['rooms'])
                    for room in studio['schedule']:
                        for event in studio['schedule'][room]:
                            begin_event_time = datetime.datetime.strptime(event[0], '%H:%M')
                            event_duration = datetime.timedelta(hours=int(event[1].split(':')[0]), minutes=int(event[1].split(':')[1]))
                            if begin_event_time + event_duration > datetime.datetime.strptime(time, '%H:%M') >= begin_event_time:
                                if studio['studio_info']['name'] in schedule[time]:
                                    schedule[time][studio['studio_info']['name']].discard(room)
                    if studio['studio_info']['name'] in schedule[time] and schedule[time][studio['studio_info']['name']] == set():
                        del schedule[time][studio['studio_info']['name']]
                    if studio['studio_info']['name'] in schedule[time]:
                        schedule[time][studio['studio_info']['name']] = dict.fromkeys(schedule[time][studio['studio_info']['name']], 0)
        for studio in total_schedule['studios_info']:
            for room in total_schedule['studios_info'][studio]['rooms']:
                free_time = 0
                for time in day_time[::-1]:
                    if studio in schedule[time] and room in schedule[time][studio]:
                        free_time += 30
                        schedule[time][studio][room] = ':'.join(str(datetime.timedelta(minutes=free_time)).split(':')[:-1])     
                    else:
                        free_time = 0
        total_schedule['schedule'] = schedule
        return total_schedule
