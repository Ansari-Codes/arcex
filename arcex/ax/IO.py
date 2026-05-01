from arcex.ax.utils import html
from arcex.ax.Exceptions import AXError

class Output:
    def __init__(self):
        self.ops = {}

    def add(self, el):
        self._ensure_id(el)
        self.ops[el._id] = {
            "op": "add",
            "html": html(el)
        }
        return self

    def replace(self, el):
        self._ensure_id(el)
        self.ops[el._id] = {
            "op": "replace",
            "html": html(el)
        }
        return self

    def remove(self, el_id):
        self.ops[el_id] = {
            "op": "remove"
        }
        return self

    def value(self, el, value):
        self._ensure_id(el)
        self.ops[el._id] = {
            "op": "value",
            "value": value
        }
        return self

    def _ensure_id(self, el):
        if not el._id:
            raise AXError("Element must have id!")

    def get_output(self):
        return self.ops