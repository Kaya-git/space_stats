import datetime


async def get_date(week=None, days=None):
    date = datetime.datetime.today()
    if days:
        date = date - datetime.timedelta(days=days)
    elif week:
        date = date - datetime.timedelta(days=(date.weekday()))
    return date.strftime("%Y-%m-%dT00:00:00.000+03:00")
