from Arcex.ax.IO import Output
from Arcex.ax.Exceptions import AXError

class EventTypes:
    click = "onclick"
    input = "oninput"

_events = {}

def ensure_output(fn):
    def wrapper(*args, **kwargs):
        result = fn(*args, **kwargs)
        if not isinstance(result, Output):
            raise AXError("Event callback must return an Output object...!")
        return result
    return wrapper

def register_event(element_id, event, event_type=EventTypes.click):
    if element_id not in _events: _events[element_id] = {}
    _events[element_id][event_type] = ensure_output(event)

def get_event(element_id, event_type=EventTypes.click):
    if element_id not in _events: return None
    if not event_type in _events[element_id]: return None
    return _events[element_id][event_type]
