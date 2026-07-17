from icalendar import Calendar, Event
from datetime import datetime, timedelta


def create_ics(data):

    cal = Calendar()

    event = Event()

    event.add(
        "summary",
        data["title"]
    )

    # temporary date
    start = datetime(
        2026,
        7,
        17,
        int(data["time"].split(":")[0]),
        int(data["time"].split(":")[1])
    )

    event.add(
        "dtstart",
        start
    )

    event.add(
        "dtend",
        start + timedelta(
            minutes=data["duration"]
        )
    )

    cal.add_component(event)

    with open(
        "calendar_event.ics",
        "wb"
    ) as f:
        f.write(
            cal.to_ical()
        )

    print("Created calendar_event.ics")