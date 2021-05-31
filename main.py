#Импортировали библиотеку vk_api (pip install vkapi)
from settings import VK_TOKEN, WEATHER_TOKEN
import vk_api
from vk_api import longpoll 
#Достали из библиотеки две функции
from vk_api.longpoll import VkLongPoll, VkEventType
import requests
from settings import VK_TOKEN,WEATHER_TOKEN
#Адрес сайта для запроса погоды
url = "http://api.openweathermap.org/data/2.5/weather"
api_key = WEATHER_TOKEN
token = VK_TOKEN
#Подключение api key
#Переменная для хранения токена группы ВК
keyboard = '{"buttons":[[{"action":{"type":"text","label":"Погода","payload":""},"color":"negative"}],[{"action":{"type":"text","label":"Москва","payload":""},"color":"positive"},{"action":{"type":"text","label":"Санкт-Петербург","payload":""},"color":"positive"}],[{"action":{"type":"text","label":"Новосибирск","payload":""},"color":"positive"},{"action":{"type":"text","label":"Екатеринбург","payload":""},"color":"positive"}],[{"action":{"type":"text","label":"Казань","payload":""},"color":"positive"},{"action":{"type":"text","label":"Нижний Новгород","payload":""},"color":"positive"}],[{"action":{"type":"text","label":"Челябинск","payload":""},"color":"positive"},{"action":{"type":"text","label":"Самара","payload":""},"color":"positive"}]]}'
#Подключаем токен и longpoll
token_connection = vk_api.VkApi(token = VK_TOKEN)
#Посылаем запрос на подключение
give = token_connection.get_api()
#Связываем бота с api группы
longpoll = VkLongPoll(token_connection)
#Функция для ответа на сообщения в ЛС группы

def weather(city_name):
    params = {"APPID": WEATHER_TOKEN, "q": city_name, "units": "metric", "lang": "ru"}
    result = requests.get(url, params=params)
    weather = result.json()
    print(weather)
    result = ""
    if weather['cod'] == '404':
        result = "Город не найден"
    else:
        result = "В городе " + weather["name"] + "--"
        result += weather["weather"][0]["description"] + "\n"
        result += "Температура " + str(weather["main"]["temp"])+" °С" + "\n"
        result += "Ощущается " + str(weather["main"]["feels_like"])+" °С" + "\n"
        result += "Ветер "+ str(weather["wind"]["speed"])+" м/с" + "\n"
        result += "Давление " + str(weather["main"]["pressure"])+" мм.рт" + "\n"
        result += "Влажность " + str(weather["main"]["humidity"])+"%" + "\n"



    return result

def write_msg(id, text):
    #Отправка сообщение человеку
    token_connection.method('messages.send', {'user_id' : id, 'message' : text, 'random_id' : 0, 'keyboard' : keyboard})

#Функция формирования ответа бота
def answer(id, text):
    if text == 'привет' or text == 'Начать' or text == 'ку' or text == 'хай' or text == 'здарова' or text == 'hi' or text == 'hello':
        return 'Привет,༼ つ ◕_◕ ༽つ я погодный ботツ'
    elif text == 'как дела?':
        return "Хорошо,а как твои?(●'◡'●)"
    elif text == 'хорошо' or text == 'отлично' or text == 'круто':
        return "Ну и хорошо :-D"
    elif text == 'погода':
        write_msg(id, "Напиши мне название города")
        for event in longpoll.listen():
            if event.type == VkEventType.MESSAGE_NEW:
                #Если сообщение для бота
                if event.to_me:
                    #Получем текст сообщение и переводим его в нижний регистер
                    message = event.text.lower()
                    return weather(message)
    else:
        return weather(text)

    
try:
    #Слушаем longpoll и ждем новое сообщение боту
    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW:
            #Если сообщение для бота
            if event.to_me:
                #Получем текст сообщение и переводим его в нижний регистер
                message = event.text.lower()
                #Получаем id пользователя
                id = event.user_id
                text = answer(id, message)
                write_msg(id, text)
                print(id, message, event.datetime)
except KeyboardInterrupt: 
    print(" Bot stop")             
finally:
    print()
