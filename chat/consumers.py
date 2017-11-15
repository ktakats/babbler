from channels import Group
from channels.sessions import channel_session
from channels.auth import channel_session_user, channel_session_user_from_http
import json

@channel_session
@channel_session_user_from_http
def ws_add(message, room):
    message.reply_channel.send({"accept": True})
    Group('chat-%s' % (room)).add(message.reply_channel)
    message.channel_session['room'] = room

@channel_session
@channel_session_user
def ws_message(message):
    print message.channel_session.keys()
    room = message.channel_session['room']
    Group('chat-%s' %  (room)).send({
        "text": json.dumps({'msg': message.content['text'], 'author': message.user.first_name})
    })

@channel_session
@channel_session_user
def ws_disconnect(message, room):
    Group("chat-%s" % room).discard(message.reply_channel)