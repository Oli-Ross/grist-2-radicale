from typing import List
from env import RADICALE_ALT_URL
from events import Event, get_current_events
from radicale import get_calendar
from radicale import get_events as get_events_radicale
from grist import get_events as get_events_grist


def process_events(events: List[Event]) -> List[Event]:
    events_set = set(events)
    merged_events = []
    for e_first, e_second in zip(events, events[1:]):
        if e_first not in events_set:
            continue
        if (e_first.end == e_second.start) and (e_first.summary == e_second.summary):
            merged_events.append(
                Event(e_first.summary, e_first.start, e_second.end, e_first.id)
            )
            events_set.remove(e_first)
            events_set.remove(e_second)
        else:
            merged_events.append(e_first)
            events_set.remove(e_first)
    for event in events_set:
        merged_events.append(event)
    return merged_events


def sync_grist_to_radicale():
    cal = get_calendar()
    cal_alt = get_calendar(url=RADICALE_ALT_URL)

    radicale_events = get_events_radicale(cal)
    for e in radicale_events:
        e.remove_from_calendar(cal)
        e.remove_from_calendar(cal_alt)

    current_events = get_current_events(get_events_grist())
    for e in current_events:
        e.add_to_calendar(cal)

    merged_events = process_events(current_events)
    for e in merged_events:
        e.add_to_calendar(cal_alt)
