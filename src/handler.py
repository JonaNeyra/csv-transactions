from typing import Any


def handle(event: dict, context: Any):
    print("Event: ", event)
    print("Context: ", context)
    return "Hello Docker RIE"
