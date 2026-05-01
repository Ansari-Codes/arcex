from Arcex.ax import Output
from Arcex.ax.Elements import Element
from Arcex.ax.Events import EventTypes, register_event
from Arcex.ax.Exceptions import AXError

def _wrap_handler(component, handler):
    def wrapper(value):
        result = handler(value)
        if not isinstance(result, Output):
            raise AXError("Handler must return Output")
        component.set_value(value)
        result.value(component, value)
        return result
    return wrapper

class Input(Element):
    def __init__(self, name, input_type="text", value="", id=None):
        self._value = value
        self._id = id

        super().__init__("input", [], id, attrs={"name": name, "type": input_type, "value": value})

    def _apply_events(self, events):
        for k in ["oninput", "onkeydown", "onkeyup", "onkeypress"]:
            self.attrs.pop(k, None)
        triggers = [events] if not isinstance(events, list) else events
        for ev in triggers:
            if ev == "input":
                self.attrs["oninput"] = f"axInputEvent(`{self._id}`, this.value)"
            elif ev in ("keydown", "keyup", "keypress"):
                self.attrs[f"on{ev}"] = f"axInputEvent(`{self._id}`, this.value)"
            elif ev.lower() == "enter":
                self.attrs["onkeydown"] = (
                    f"if(event.key === 'Enter') "
                    f"{{ axInputEvent(`{self._id}`, this.value); }}"
                )
        return self

    def onchange(self, events="input", handler=None):
        self._apply_events(events)
        if handler:
            register_event(self._id, _wrap_handler(self, handler), EventTypes.input)
        return self

    def set_value(self, value):
        self._value = value
        self.attrs["value"] = value
        return self    

class Select(Element):
    def __init__(self, name, options, value=None, id=None):
        self._options = options
        self._value = value
        self._id = id

        super().__init__("select", [], id, attrs={"name": name})
        self._build_options()

    def _build_options(self):
        with self:
            for option in self._options:
                if isinstance(option, tuple):
                    label, val = option
                else:
                    label, val = option, option

                attrs = {"value": val}
                if val == self._value:
                    attrs["selected"] = "selected"

                Element("option", [label], attrs=attrs)

    def onchange(self, handler):
        self.attrs["onchange"] = f"axEvent(`{self._id}`, `{EventTypes.input}`, this.value)"
        if handler:
            register_event(self._id, _wrap_handler(self, handler), EventTypes.input)
        return self

    def set_value(self, value):
        self._value = value
        self._build_options()
        return self

class Date(Element):
    def __init__(self, name, value="", id=None):
        self._value = value
        self._id = id

        super().__init__("input", [], id, attrs={"name": name, "type": "date", "value": value})

    def onchange(self, handler):
        if self._id is None:
            raise AXError("ID required")
        self.attrs["onchange"] = f"axInputEvent('{self._id}', this.value)"

        register_event(self._id, _wrap_handler(self, handler), EventTypes.input)

        return self


    def set_value(self, value):
        if self._value != value:
            self._value = value
            self.attrs["value"] = value
        return self