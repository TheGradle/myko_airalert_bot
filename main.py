import os
import random

import telebot
from telethon import TelegramClient, events

from secret import api_id, api_hash, TOKEN

client = TelegramClient('client', api_id, api_hash).start()
client_bot = TelegramClient('bot', api_id, api_hash).start(bot_token=TOKEN)
bot = telebot.TeleBot(TOKEN)


@client_bot.on(events.NewMessage(pattern='/start'))
async def send_welcome(event):
    await event.respond('👋 Вітання!\n\n'
                        'Тепер я сповіщатиму вас про повітряну тривогу, і про її відбій (наразі тільки для м. Миколаєва'
                        ' та Миколаївської області). Дані беруться з каналу @air_alert_ua.\n\n'
                        'Слава Україні! 🇺🇦')
    group_id = str(event.chat_id)
    with open('subscribers.txt', 'r') as file_r:
        subs = file_r.read()
        if group_id not in subs:
            with open('subscribers.txt', 'a') as file_a:
                file_a.write(group_id + '\n')


@client_bot.on(events.NewMessage(pattern='/help'))
async def send_welcome(event):
    await event.respond('🤔 Навіщо цей бот?\n'
                        '"По приколу" - відповідає автор :D\n\n'
                        '🤔 Як налаштувати сповіщення?\n'
                        'Все просто! Введіть команду /start для того щоб їх тримувати, і команду /stop, щоб перестати їх отримувати.\n\n'
                        '🤔 Які області України доступні?\n'
                        'Насьогодні бот сповіщає про Миколаївську область та Миколаївську територіальну громаду, але в майбутньому стануть доступні і інші області.\n\n'
                        '🤔 Звідки береться інформація про тривоги?\n'
                        'З каналу @air_alert_ua, який в свою чергу отримує інформацію з органів виконавчої влади України.\n\n'
                        '🤔 Де я можу переглянути код цього бота?\n'
                        'Код доступний на https://github.com/TheGradle/myko_airalert_bot, можете використовувати його як заманеться :)\n\n'
                        'Будьте в безпеці та не ігноруйте повітряну тривогу! Слава Україні! 🇺🇦')


@client.on(events.NewMessage(chats='air_alert_ua'))
async def alert_handler(event):
    message = event.message.to_dict()['message']
    if '#м_Миколаїв_та_Миколаївська_територіальна_громада' in message or '#Миколаївська_область' in message:
        with open('subscribers.txt', 'r') as file:
            for group_id in file:
                path = 'media/alert_on/' if '🔴' in message else 'media/alert_off/'
                message = '‍🚨 Увага! Повітряна тривога!' if '🔴' in message else '✅ Увага! Відбій повітряної тривоги!'
                media = random.choice(os.listdir(path))
                if media[-3:] == 'jpg':
                    bot.send_photo(group_id, open(path + media, 'rb'), caption=message)
                else:
                    bot.send_video(group_id, open(path + media, 'rb'), caption=message)
    else:
        print(f'{message[2:7]}: bot is working')

client.run_until_disconnected()
bot.infinity_polling()
