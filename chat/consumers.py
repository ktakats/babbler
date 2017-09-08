from channels import Group

def ws_add(message):
    message.reply_channel.send({"accept": True})
    Group('chat').add(message.reply_channel)

def ws_message(message):

    Group('chat').send({
        "text": message.content['text'],
    })