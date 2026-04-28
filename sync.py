from events import get_current_events
from radicale import get_calendar
from radicale import get_events as get_events_radicale
from grist import get_events as get_events_grist


def sync_grist_to_radicale():
    cal = get_calendar()

    radicale_events = get_events_radicale(cal)
    grist_events = get_events_grist()

    for e in radicale_events:
        e.remove_from_calendar(cal)

    for e in get_current_events(grist_events):
        e.add_to_calendar(cal)
