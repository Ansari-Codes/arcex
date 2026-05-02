from flask import session
import uuid
from Arcex.ax.Elements import Element

_state = {}

class Context:
    @staticmethod
    def sid():
        if "sid" not in session:
            session["sid"] = str(uuid.uuid4())
        return session["sid"]

class Page(Element):
    route = '/'
    title = 'A Page'
    favicon = "🤖"
    def __init__(self, props=None):
        self.props = props or {}
        self._built = False
        self.session_id = Context.sid()
        if self.session_id not in _state:
            _state[self.session_id] = {}
        self.state = _state[self.session_id]
        super().__init__('html')
        with self:
            self.head_elem = Element('head')
            self.body_elem = Element('body')
        with self.head_elem:
            Element('title', [self.title])
            Element('meta', attrs={"charset": "UTF-8"})
            Element('meta', attrs={
                "name": "viewport",
                "content": "width=device-width, initial-scale=1.0"
            })
            Element('link', attrs={
                "rel": "icon",
                "type": "image/x-icon",
                "href": self.favicon
            })
            Element('script', attrs={"src": "/static/core/ax.js"})

    def body(self):
        raise NotImplementedError("Define the body method for this Page!!!")

    def __html__(self):
        if not self._built:
            with self.body_elem: self.body()
            self._built = True    
        return super().__html__()
