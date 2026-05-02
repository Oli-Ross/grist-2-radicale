from env import RADICALE_URL, RADICALE_USER, RADICALE_PASSWORD

from typing import List
from caldav import get_davclient

from events import Event


def get_calendar(username=RADICALE_USER, url=RADICALE_URL, password=RADICALE_PASSWORD):
    with get_davclient(username=username, url=url, password=password) as client:
        principal = client.principal()
        calendars = principal.get_calendars()
        for cal in calendars:
            if str(cal.url) == url:
                return cal
        return calendars[0]


def get_events(cal) -> List[Event]:
    return [Event.from_radicale(x) for x in cal.search(event=True)]
