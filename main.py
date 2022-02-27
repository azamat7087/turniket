import requests
import urllib3
import json
import telebot
from models import Parents, SessionLocal, ChildActivities
from schemas import ChildActivitiesBase, ChildActivitiesDBBase, ParentsBase, ParentsDBBase
from sqlalchemy import select
TOKEN_API = 'master'
TOKEN_TELE = '5252378629:AAHs4BmpAH3jh_2BZkVaUB0g95nfTxJzPx4'
headers = {'User-agent': 'Mozilla/5.0'}

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

bot = telebot.TeleBot(TOKEN_TELE)

is_activated = False

session = SessionLocal()


@bot.message_handler(commands=['start'])
def start(message):

    parent = session.query(Parents).filter_by(telegram_id=str(message.chat.id)).scalar()
    if not parent:
        obj = Parents(**{'telegram_id': message.chat.id,
                         'username': f"{message.from_user.first_name} {message.from_user.last_name}"})
        session.add(obj)
        session.commit()
        session.refresh(obj)
        parent = session.query(Parents).filter_by(telegram_id=str(message.chat.id)).scalar()

    if parent.is_activated:
        bot.send_message(message.chat.id, 'Здравствуйте, вы уже ввели id')
    else:
        bot.send_message(message.chat.id, 'Здравствуйте, введите id')


@bot.message_handler()
def get_id(message):
    parent = session.query(Parents).filter_by(telegram_id=str(message.chat.id)).scalar()
    url = 'https://ru.percoweb.com/api/users/visitor/'
    pk = "None"
    if not parent.is_activated:
        pk: str = message.json['text']
    elif parent.is_activated:
        pk: str = str(parent.child.db_id)

    if pk.isdigit():
        url = url + pk + '?&' + TOKEN_API
        response = requests.get(url, verify=False)
        if response.status_code == 200:
            text = response.json()['last_name'] + ' ' + response.json()['first_name'] + '\n' + response.json()[
                'begin_datetime'] + '\n' + response.json()['end_datetime']

            child = session.query(ChildActivities).filter_by(db_id=int(pk)).scalar()
            if not child:
                child = ChildActivities(**{'name': f"{response.json()['first_name']} {response.json()['last_name']}",
                                           'db_id': f"{response.json()['id']}",
                                           'arrive_time': f"{response.json()['begin_datetime']}",
                                           'leaving_time': f"{response.json()['end_datetime']}"
                                           })
                session.add(child)
                session.commit()
                session.refresh(child)
            child = session.query(ChildActivities).filter_by(db_id=int(pk)).scalar()

            parent.child_id = child.id
            parent.is_activated = True
            session.add(parent)
            session.commit()
            session.refresh(parent)

            bot.send_message(message.chat.id, text)
        elif response.status_code == 500:
            bot.send_message(message.chat.id, f"{response.json()['error']}")
        else:
            bot.send_message(message.chat.id, "Непредвиденная ошибка, попробуйте еще раз")
    else:
        bot.send_message(message.chat.id, 'Введите валидный id')
    session.close()


while True:
    try:
        bot.polling(none_stop=True)
        break
    except Exception as e:
        print(str(e))
        pass

