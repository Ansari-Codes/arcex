from Arcex.ax import Output
from Arcex.ax.Elements import Element
from Arcex.ax.Exceptions import AXError

class Div(Element):
    def __init__(self, children=None, *,id=None, attrs=None, properties=None, styles=None):
        super().__init__('div', children, id, attrs, properties, styles)

class Card(Element):
    def __init__(self, children=None, *,id=None, attrs=None, properties=None, styles=None):
        super().__init__('card', children, id, attrs, properties, styles)

class Row(Element):
    def __init__(self, children=None, *,id=None, attrs=None, properties=None, styles=None):
        super().__init__('row', children, id, attrs, properties, styles)

class Col(Element):
    def __init__(self, children=None, *,id=None, attrs=None, properties=None, styles=None):
        super().__init__('col', children, id, attrs, properties, styles)

class LBreak(Element):
    def __init__(self):
        super().__init__('br')

class LHl(Element):
    def __init__(self, children=None, *,id=None, attrs=None, properties=None, styles=None):
        super().__init__('hl', children, id, attrs, properties, styles)

class LVl(Element):
    def __init__(self, children=None, *,id=None, attrs=None, properties=None, styles=None):
        super().__init__('vl', children, id, attrs, properties, styles)



