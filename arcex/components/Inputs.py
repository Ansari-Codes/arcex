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

    def on(self, events="input", handler=None):
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

    def on(self, handler):
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

    def on(self, handler):
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

class Textarea(Element):
    def __init__(self, name: str, value: str = "", rows: int = 4, id: str|None = None):
        self._value = value
        self._id = id

        super().__init__(
            "textarea",
            children=[value] if value else [],
            id=self._id,
            attrs={"name": name, "rows": rows}
        )

    def _apply_events(self, events):
        for k in ["oninput", "onkeydown", "onchange"]:
            self.attrs.pop(k, None)

        triggers = [events] if isinstance(events, str) else events or []

        for ev in triggers:
            ev = ev.lower().strip()

            if ev == "input":
                self.attrs["oninput"] = f"axInputEvent(`{self._id}`, this.value, false)"

            elif ev in ("keydown", "keyup", "keypress"):
                self.attrs[f"on{ev}"] = f"axInputEvent(`{self._id}`, this.value, false)"

            elif ev == "enter":
                self.attrs["onkeydown"] = (
                    f"if(event.key === 'Enter') {{"
                    f"event.preventDefault(); "
                    f"axInputEvent(`{self._id}`, this.value, true);"
                    f"}}"
                )

        return self

    def on(self, events: str | list = "input", handler=None):
        self._apply_events(events)
        if handler:
            register_event(self._id, _wrap_handler(self, handler), EventTypes.input)
        return self

    def set_value(self, value: str):
        self._value = value
        self._children = [str(value)] if value else []
        return self

class Checkbox(Element):
    def __init__(self, name: str, label: str = "", checked: bool = False, id: str|None = None):
        self._checked = bool(checked)
        
        self._label = label
        self._id = str(id) + 'label'

        super().__init__(
            _tag="span",
            children=[self._label],
            id=self._id,
        )

        with self:
            self._check = Element('input', attrs={"type": "checkbox", "name": name, "id": self._id})
            if self._checked:
                self._check.attrs["checked"] = "checked"

    def _apply_events(self):
        self._check.attrs.pop("onchange", None)
        self._check.attrs["onchange"] = f"axInputEvent(`{self._id}`, this.checked, false)"
        return self

    def on(self, handler=None):
        self._apply_events()
        if handler:
            register_event(self._id, _wrap_handler(self, handler), EventTypes.input)
        return self

    def set_value(self, checked: bool):
        self._checked = bool(checked)
        if self._checked:
            self._check.attrs["checked"] = "checked"
        else:
            self._check.attrs.pop("checked", None)
        return self
    
    def set_label(self, label):
        self._label = label
        return self

class Number(Element):
    def __init__(self, name: str, value: int | float = 0, min=None, max=None, step=1, id: str|None = None):
        self._value = value
        self._id = id

        attrs = {
            "name": name,
            "type": "number",
            "value": str(value),
            "step": str(step)
        }
        if min is not None:
            attrs["min"] = str(min)
        if max is not None:
            attrs["max"] = str(max)

        super().__init__("input", [], id=self._id, attrs=attrs)

    def _apply_events(self, events):
        for k in ["oninput", "onkeydown", "onchange"]:
            self.attrs.pop(k, None)

        triggers = [events] if isinstance(events, str) else events or []

        for ev in triggers:
            ev = ev.lower().strip()

            if ev == "input":
                self.attrs["oninput"] = f"axInputEvent(`{self._id}`, this.value, false)"

            elif ev in ("keydown", "keyup", "keypress"):
                self.attrs[f"on{ev}"] = f"axInputEvent(`{self._id}`, this.value, false)"

            elif ev == "enter":
                self.attrs["onkeydown"] = (
                    f"if(event.key === 'Enter') {{"
                    f"event.preventDefault(); "
                    f"axInputEvent(`{self._id}`, this.value, true);"
                    f"}}"
                )

        return self

    def on(self, events: str | list = "input", handler=None):
        self._apply_events(events)
        if handler:
            register_event(self._id, _wrap_handler(self, handler), EventTypes.input)
        return self

    def set_value(self, value):
        self._value = value
        self.attrs["value"] = str(value)
        return self

