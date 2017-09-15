from channels.routing import route
from chat.consumers import ws_add,ws_message

channel_routing = [
    route("websocket.receive", ws_message),
    route('websocket.connect', ws_add, path=r'^/chat/(?P<room>\w+)$'),
]
