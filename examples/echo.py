from vk_bots import Client

GROUP_ID = 0
ACCESS_TOKEN = ''

bot = Client(GROUP_ID, ACCESS_TOKEN)


@bot.event
async def ready():
    print('Bot started')


@bot.event
async def message_new(message, _):
    print(f'New message from id{message.from_id}: {message.text}')
    await bot.api.messages.send(peer_id=message.peer_id,
                                message=message.text)


bot.run()
