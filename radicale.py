from env import RADICALE_URL, RADICALE_USER, RADICALE_PASSWORD

from typing import List
from caldav import get_davclient

from events import Event


def get_calendar():
    with get_davclient(
        username=RADICALE_USER, url=RADICALE_URL, password=RADICALE_PASSWORD
    ) as client:
        principal = client.principal()
        calendars = principal.get_calendars()
        cal = calendars[0]
        return cal


def get_events(cal) -> List[Event]:
    return [Event.from_radicale(x) for x in cal.search(event=True)]
