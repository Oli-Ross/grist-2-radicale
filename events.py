from typing import List, Tuple
import caldav
from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True)
class Event:
    summary: str
    start: datetime
    end: datetime
    id: str

    @classmethod
    def from_grist(cls, data) -> "Event" | None:
        if any(x is None for x in [data.summary, data.start, data.end, data.id]):
            return None
        return Event(
            summary=data.summary,
            start=datetime.fromtimestamp(data.Start),
            end=datetime.fromtimestamp(data.Ende),
            id=str(data.id),
        )

    @classmethod
    def from_radicale(cls, data) -> "Event":
        comp = data.get_icalendar_component()
        return Event(
            summary=comp["summary"].to_ical().decode(),
            start=datetime.fromisoformat(comp["dtstart"].to_ical().decode()),
            end=datetime.fromisoformat(comp["dtend"].to_ical().decode()),
            id=comp["uid"].to_ical().decode(),
        )

    def add_to_calendar(self, calendar):
        calendar.add_event(
            dtstart=self.start, dtend=self.end, uid=self.id, summary=self.summary
        )

    def remove_from_calendar(self, calendar):
        ev = calendar.search(event=True, uid=self.id)
        if len(ev) > 1:
            raise ValueError("Found >1 event with the specified UID: Aborting deletion")
        if len(ev) == 0:
            print(f"Found no event with UID {self.id}")
        ev[0].delete()


def compare_event_lists(
    true_events: List[Event], derived_events: List[Event]
) -> Tuple[List[Event], List[Tuple[Event, Event]], List[Event]]:
    """
    Compare 2 event lists

    Returns:
        missing, differing, extra: Tuple of lists
            `missing` has all events that are missing from derived_events
            `differing` has tuples of mismatches where the ID aligns, but details don't.
                format: [(new_event, old_event)]
            `extra` has all events that are in derived_events but not in true_events
    """
    missing = []
    differing = []
    derived_by_id = {x.id: x for x in derived_events}
    for event in true_events:
        match = derived_by_id.get(event.id, None)
        if not match:
            missing.append(event)
            continue
        else:
            if match != event:
                differing.append((event, match))

    true_by_id = {x.id: x for x in true_events}
    extra = [x for x in derived_events if x.id not in true_by_id]

    return missing, differing, extra
