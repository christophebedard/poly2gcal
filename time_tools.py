## Tools for time conversion/processing

from datetime import datetime, timedelta

WEEKDAYS_INT = { weekday: i for i, weekday in enumerate(['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']) }

def to_datetime(time_str):
    return datetime.strptime(time_str, '%d/%b/%Y')

def to_date(time_str):
    return to_datetime(time_str).date()

def weekday_int(weekday_str):
    return WEEKDAYS_INT[weekday_str]

def timedelta_from_day_and_time(day, start):
    start_time = datetime.strptime(start, '%H%M')
    return timedelta(days=weekday_int(day), hours=start_time.hour, minutes=start_time.minute)

def timedelta_from_class_duration(duration):
    total_minutes = (60 * duration) - 10
    hours = total_minutes // 60
    minutes = total_minutes % 60
    return timedelta(hours=hours, minutes=minutes)

def month_from_datetime(date):
    return date.strftime('%B')
