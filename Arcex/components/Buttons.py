from Arcex.ax.Elements import Element
from Arcex.ax.Exceptions import AXError
from Arcex.ax.Events import register_event, EventTypes

class Button(Element):
    def __init__(self, text, id = None, *, styles=None, attrs=None, properties=None):
        super().__init__("button", [{"__text__": text}], id, attrs={
            "type": "button",
            EventTypes.click: f"axEvent(`{id}`, `{EventTypes.click}`)",
        **(attrs or {})}, styles=styles, properties=properties)

    def onclick(self, handler):
        if (handler is not None) and (self._id is None):
            raise AXError("ID is required when passing onclick for a button!")
        def onclick_handler(e=None):
            output = handler(e)
            return output.replace(self)
        if handler:
            register_event(self._id, onclick_handler, EventTypes.click)

    def set_text(self, text: str):
        texted = False
        for i in self._children:
            if isinstance(i, dict):
                if '__text__' in i:
                    i['__text__'] = text
                    texted += 1
        if not text:
            self._children.append({"__text__": text})
        return self
