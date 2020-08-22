import vk_api
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
import random
import requests
import os

token = '677612bf31d1c9ba14468cc5d8abc64ed42ebc578e68509190bda5005c1ebc830fabafa886a12b32ecd4c'
vk = vk_api.VkApi(token=token)
longpoll = VkBotLongPoll(vk, 189639189)
bot_api = vk.get_api()
url = "http://www.oodbnk.ru/image/R.jpg"

rasp = "Обычные дни:\n1 - 8:30 – 10:05\n2 - 10:15 - 11:50\n3 - 12:20 – 13:55\n4 - 14:10 – 15:40\n5 - 15:50 – 17:20\n\nСуббота\n1 - 8:30 – 10:05\n2 - 10:15 - 11:50\n3 - 12:00 – 13:35\n4 - 13:45 – 15:15\n5 - 15:25 – 16:55"
menu = 'pks_bot пока умеет:\n\n1 - бот изменения\n2 - бот номер ОА\n3 - бот расписание звонков\n4 - бот номер ДА\n\nВводить можно с любым регистром'
name = ['Дмитрий Егоров', 'Никита Зимин', 'Дмитрий Чертанов', 'Марина Мироненко', 'Алексей Рябин', 'Альбина Хаметова', 'Даниил Федоров', 'Александр Шандыба', 'Глеб Мамыкин', 'Эдуард Соловьев', 'Анатолий Прилипко', 'Максим Селедков', 'Максим Сотников', 'Денис Казаев', 'Иван Ульянов']


def sendMessage(event, message):
    if event.from_user:
        bot_api.messages.send(
            user_id=event.object.message['from_id'],
            message=message,
            random_id=random.randint(0, 10000)
        )
    elif event.from_chat:
        bot_api.messages.send(
            random_id=random.randint(0, 10000),
            message=message,
            chat_id=event.chat_id
        )


def sendMessagePhoto(event):
    path = os.path.join(os.path.abspath(os.path.dirname(__file__)), '1.jpg')
    if path:
        os.remove(path)
    file = open('1.jpg', 'wb')
    p = requests.get(url)
    file.write(p.content)
    file.close()
    a = vk.method("photos.getMessagesUploadServer")
    b = requests.post(a['upload_url'], files={'photo': open('1.jpg', 'rb')}).json()
    c = vk.method('photos.saveMessagesPhoto', {'photo': b['photo'], 'server': b['server'], 'hash': b['hash']})[
        0]
    d = "photo{}_{}".format(c["owner_id"], c["id"])
    if event.from_user:
        bot_api.messages.send(
            user_id=event.object.message['from_id'],
            message='Привет!',
            attachment=d,
            random_id=random.randint(0, 10000)
        )
    elif event.from_chat:
        bot_api.messages.send(
            random_id=random.randint(0, 10000),
            message='Изменения',
            attachment=d,
            chat_id=event.chat_id
        )


def main():
    for event in longpoll.listen():
        if event.type == VkBotEventType.MESSAGE_NEW:
            value = event.object.message['text']
            if value.lower() == 'бот помощь':
                sendMessage(event, menu)

            if value.lower() == 'бот изменения':
                sendMessagePhoto(event)

            if value.lower() == 'бот номер оа':
                sendMessage(event, '+7 922 547-32-32')

            if value.lower() == 'бот номер да':
                sendMessage(event, '8 929 281-50-00')

            if value.lower() == 'бот расписание звонков':
                sendMessage(event, rasp)

            if value.lower() == 'бот кто в группе лох?':
                rand = random.randint(0, 14)
                sendMessage(event, name[rand])


if __name__ == '__main__':
    main()