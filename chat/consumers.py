
def ws_message(message):
    print message
    message.reply_channel.send({
        "text": message.content['text'],
    })