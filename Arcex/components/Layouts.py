from Arcex.ax import Output
from Arcex.ax.Elements import Element
from Arcex.ax.Exceptions import AXError

class Div(Element):
    def __init__(self, children=None, id=None, attrs=None, properties=None, styles=None):
        super().__init__('div', children, id, attrs, properties, styles)

class Row(Element):
    def __init__(self, children=None, id=None, attrs=None, properties=None, styles=None):
        super().__init__('row', children, id, attrs, properties, styles)

class Col(Element):
    def __init__(self, children=None, id=None, attrs=None, properties=None, styles=None):
        super().__init__('col', children, id, attrs, properties, styles)
