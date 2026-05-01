from flask import Flask, request
from arcex.ax.Events import get_event, EventTypes
from arcex.ax.utils import html

app = Flask(__name__, static_folder='arcex/static')
app.secret_key = "secret-key"

@app.route("/.event/<id>/<type>", methods=['POST', 'GET'])
def event_handle(id: str, type: str = EventTypes.click):
    data = request.get_json(silent=True)
    ev = get_event(id, type)
    if ev:
        output = ev(data).get_output()
        return output
    else:
        return {}

def routate(page_cls, **flask_kwargs):
    @app.route(page_cls.route, **flask_kwargs)
    def page_route(**url_args):
        query_args = request.args.to_dict()
        body_args = request.get_json(silent=True) or {}
        all_args = {**url_args, **query_args, **body_args}
        page = page_cls(**all_args)
        return html(page)
    return page_route
