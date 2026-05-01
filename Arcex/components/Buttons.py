from Arcex.ax.Elements import Element
from Arcex.ax.Exceptions import AXError
from Arcex.ax.Events import register_event, EventTypes

class Button(Element):
    def __init__(self, text, onclick=None, id = None):
        if (onclick is not None) and (id is None):
            raise AXError("ID is required when passing onclick for a button!")
        super().__init__("button", [text], id, attrs={EventTypes.click: f"axEvent(`{id}`, `{EventTypes.click}`)"})
        if onclick: register_event(id, onclick, EventTypes.click)

