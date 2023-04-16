from datetime import datetime


def date_format(timestamp, _format="%Y-%m-%d %H:%M:%S"):
    try:
        return datetime.fromtimestamp(timestamp).strftime(_format)
    except ValueError:
        return 'Invalid timestamp'


def current_time():
    return date_format(datetime.now().timestamp())
