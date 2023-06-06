import requests
import datetime as dt
import pytz
# from config import tg_bot_token, open_weather_token
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor


bot = Bot(token="Ваш токен бота")
dp = Dispatcher(bot)


@dp.message_handler(commands=["start"])
async def start_command(message: types.Message):
    await message.reply("Привет напиши мне название города и я пришлю сводку погоды!")

@dp.message_handler()
async def get_weather(message: types.Message):
    code_to_smile = {
        "Clear": "Ясно \U00002600",
        "Clouds": "Облачно \U00002681",
        "Rain": "Дождь \U00002614",
        "Drizzle": "Дождь \U00002614",
        "THunderstorm": "Гроза \U000026A1",
        "Snow": "Снег \U0001F328",
        "Mist": "Туман \U0001F32B"
    }

    try:

        r = requests.get(
            f'https://api.openweathermap.org/data/2.5/weather?q={message.text}&appid={"ваш токен с сайта open weather"}&units=metric'
        )
        data = r.json()

        city = data["name"]
        temperature = data["main"]["temp"]
        humidity = data["main"]["humidity"]
        pressure = data["main"]["pressure"]
        wind = data["wind"]["speed"]
        sunrise_timestamp = dt.datetime.fromtimestamp(data["sys"]["sunrise"])
        sunset_timestamp = dt.datetime.fromtimestamp(data["sys"]["sunset"])
        length_of_the_day = dt.datetime.fromtimestamp(data["sys"]["sunset"]) - dt.datetime.fromtimestamp(
            data["sys"]["sunrise"])
        weather_description = data['weather'][0]['main']
        if city == 'Moscow' or 'москва':
            if weather_description in code_to_smile:
                wd = code_to_smile[weather_description]
            moscow_tz = dt.datetime.now(pytz.timezone('Europe/Moscow'))
            sunrise_timestamp = dt.datetime.fromtimestamp(data["sys"]["sunrise"], pytz.timezone('Europe/Moscow')).strftime("%Y-%m-%d %H:%M")
            sunset_timestamp = dt.datetime.fromtimestamp(data["sys"]["sunset"], pytz.timezone('Europe/Moscow')).strftime("%Y-%m-%d %H:%M")
            await message.reply(f'***{moscow_tz.strftime("%Y-%m-%d %H:%M")}***\n'
                  f'Погода в городе: Москва\nТемпература: {temperature}°C {wd}\n'
                  f'Влажность: {humidity}\nДавление: {pressure} мм.рт.ст\nВетер: {wind} м/с\n'
                  f'Восход солнца: {sunrise_timestamp}\n'
                  f'Закат солнца: {sunset_timestamp}\nПродолжительность дня: {length_of_the_day}\n'
                  f'***Хорошего дня!***')

        elif weather_description in code_to_smile:
            wd = code_to_smile[weather_description]
            await message.reply(f'***{dt.datetime.now().strftime("%Y-%m-%d %H:%M")}***\n'
                  f'Погода в городе: {city}\nТемпература: {temperature}°C {wd}\n'
                  f'Влажность: {humidity}\nДавление: {pressure} мм.рт.ст\nВетер: {wind} м/с\n'
                  f'Восход солнца: {sunrise_timestamp}\n'
                  f'Закат солнца: {sunset_timestamp}\nПродолжительность дня: {length_of_the_day}\n'
                  f'***Хорошего дня!***')

        else:
            wd = "Посмотри в окно, не пойму что там за погода!"
            await message.reply(f'***{dt.datetime.now().strftime("%Y-%m-%d %H:%M")}***\n'
                  f'Погода в городе: {city}\nТемпература: {temperature}°C {wd}\n'
                  f'Влажность: {humidity}\nДавление: {pressure} мм.рт.ст\nВетер: {wind} м/с\n'
                  f'Восход солнца: {sunrise_timestamp}\n'
                  f'Закат солнца: {sunset_timestamp}\nПродолжительность дня: {length_of_the_day}\n'
                  f'***Хорошего дня!***')

    except:
        await message.reply('\U00002620 Проверьте название города \U00002620')



if __name__ == '__main__':
    executor.start_polling(dp)

