from flask import Flask, request, send_file
from flask_cors import CORS
from transformers import pipeline
from icalendar import Calendar, Event
from datetime import datetime, timedelta
import json
import re


app = Flask(__name__)
CORS(app)


print("Loading model...")

model = pipeline(
    "text-generation",
    model="aarchoksi/calendar-ai-model"
)

print("Model loaded!")


def create_ics(data):

    cal = Calendar()

    event = Event()

    event.add(
        "summary",
        data["title"]
    )

    start = datetime(
        2026,
        7,
        20,
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


    filename = "calendar_event.ics"

    with open(filename, "wb") as f:
        f.write(
            cal.to_ical()
        )

    return filename



@app.route("/create-event", methods=["POST"])
def create_event():

    user_text = request.json["text"]


    prompt = f"""
User:
{user_text}

JSON:
"""


    result = model(
        prompt,
        max_new_tokens=100,
        temperature=0.1
    )


    output = result[0]["generated_text"]


    match = re.search(
        r"\{.*\}",
        output,
        re.DOTALL
    )


    data = json.loads(
        match.group()
    )


    file = create_ics(data)


    return send_file(
        file,
        as_attachment=True
    )



app.run(
    host="0.0.0.0",
    port=7860
)
