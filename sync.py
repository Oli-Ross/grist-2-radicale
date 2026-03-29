from events import compare_event_lists
from radicale import get_calendar
from radicale import get_events as get_events_radicale
from grist import get_events as get_events_grist


def sync_grist_to_radicale():
    cal = get_calendar()

    radicale_events = get_events_radicale(cal)
    grist_events = get_events_grist()

    missing, differing, extra = compare_event_lists(grist_events, radicale_events)

    for event in missing:
        event.add_to_calendar(cal)

    for new, old in differing:
        old.remove_from_calendar(cal)
        new.add_to_calendar(cal)

    for event in extra:
        event.remove_from_calendar(cal)
