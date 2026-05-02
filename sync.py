from typing import List
import logging
from env import RADICALE_ALT_URL
from events import Event, get_current_events
from radicale import get_calendar
from radicale import get_events as get_events_radicale
from grist import get_events as get_events_grist


def process_events(events: List[Event]) -> List[Event]:
    events = sorted(events, key=lambda e: (e.start, e.end, e.summary))
    merged: List[Event] = []

    for event in events:
        if (
            merged
            and merged[-1].end == event.start
            and merged[-1].summary == event.summary
        ):
            previous = merged[-1]
            merged[-1] = Event(previous.summary, previous.start, event.end, previous.id)
        else:
            merged.append(event)

    return merged


def sync_grist_to_radicale():
    cal = get_calendar()
    cal_alt = get_calendar(url=RADICALE_ALT_URL)

    logging.info("Deleting old events.")
    radicale_events = get_events_radicale(cal)
    for e in radicale_events:
        e.remove_from_calendar(cal)

    logging.info("Deleting old alt events.")
    radicale_alt_events = get_events_radicale(cal_alt)
    for e in radicale_alt_events:
        e.remove_from_calendar(cal_alt)

    logging.info("Getting new events.")
    current_events = get_current_events(get_events_grist())

    logging.info("Adding new events to main cal.")
    for e in current_events:
        e.add_to_calendar(cal)

    logging.info("Adding new events to alt cal.")
    merged_events = process_events(current_events)
    for e in merged_events:
        e.add_to_calendar(cal_alt)
