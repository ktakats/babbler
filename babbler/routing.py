from channels.routing import route
from chat.consumers import ws_add,ws_message, ws_disconnect

channel_routing = [
    route("websocket.receive", ws_message),
    route('websocket.connect', ws_add, path=r'^/chat/(?P<room>.*)$'),
    route("websocket.disconnect", ws_disconnect, path=r"^/(?P<room_name>[a-zA-Z0-9_]+)$"),
]
