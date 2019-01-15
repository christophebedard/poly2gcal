## Classes used for time conversion/processing

from datetime import datetime, timedelta


class TimeStringUtils:
    TIME_FORMAT = '%d/%b/%Y'
    WEEKDAYS = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']
    WEEKDAYS_INT = {}
    for i, weekday in enumerate(WEEKDAYS):
        WEEKDAYS_INT[weekday] = i

    def to_datetime(time_str):
        return datetime.strptime(time_str, TimeStringUtils.TIME_FORMAT)
    
    def weekday(weekday_str):
        return TimeStringUtils.WEEKDAYS_INT[weekday_str]


class SemesterInfo:

    def __init__(self, firstweek_day, lastweek_day, last_day, breakweek_day, holidays):
        self.firstweek_day: datetime = TimeStringUtils.to_datetime(firstweek_day)
        self.lastweek_day: datetime = TimeStringUtils.to_datetime(lastweek_day)
        self.last_day: datetime = TimeStringUtils.to_datetime(last_day)
        self.breakweek_day: datetime = TimeStringUtils.to_datetime(breakweek_day)
        self.holidays: list = [TimeStringUtils.to_datetime(day).date() for day in holidays]


class Timeslot:

    def __init__(self, day, start, duration, room):
        self.start: timedelta = Timeslot.start_timedelta(day, start)
        self.duration: timedelta = Timeslot.duration_timedelta(duration)
        self.room: str = room

    def start_timedelta(day, start):
        start_time = datetime.strptime(start, '%H%M')
        return timedelta(days=TimeStringUtils.weekday(day), hours=start_time.hour, minutes=start_time.minute)
    
    def duration_timedelta(duration):
        total_minutes = (60 * duration) - 10
        hours = int(total_minutes / 60)
        minutes = total_minutes % 60
        return timedelta(hours=hours, minutes=minutes)


class AltTimeslot(Timeslot):

    def __init__(self, day, start, duration, room, week):
        super().__init__(day, start, duration, room)
        self.week: str = week


class Course:

    def __init__(self, name, cid, lectures, lab):
        self.name: str = name
        self.cid: str = cid
        self.lectures: list = lectures
        self.lab: AltTimeslot | Timeslot  = lab
