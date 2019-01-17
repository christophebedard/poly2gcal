## Tools for time conversion/processing

from datetime import datetime, timedelta, time


WEEKDAYS_INT = { weekday: i for i, weekday in enumerate(['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']) }

def to_date(time_str):
    """
    Get date object from date string
    """
    return datetime.strptime(time_str, '%d/%b/%Y').date()

def date_to_datetime(date):
    """
    Get date object from datetime object
    """
    return datetime.combine(date, time())

def weekday_int(weekday_str):
    """
    Get the integer corresponding to a day of the week as a string
    """
    return WEEKDAYS_INT[weekday_str]

def timedelta_from_day_and_time(day, start):
    """
    Get a timedelta object from a week day (e.g. 'Monday') and a start time (e.g. '0830')
    """
    start_time = datetime.strptime(start, '%H%M')
    return timedelta(days=weekday_int(day), hours=start_time.hour, minutes=start_time.minute)

def timedelta_from_class_duration(duration):
    """
    Get timedelta from class duration in number of periods/time slots
    """
    total_minutes = (60 * duration) - 10
    hours = total_minutes // 60
    minutes = total_minutes % 60
    return timedelta(hours=hours, minutes=minutes)

def month_from_date(date):
    """
    Get month as string from date object
    """
    return date.strftime('%B')
