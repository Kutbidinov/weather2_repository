import requests
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

TELEGRAM_TOKEN = "7049222427:AAFZHOejH7JfXx_SQZrD5UUCBDLDZkDBXog"
WEATHER_API_KEY = "bf9db279414da0c2e50da36f6e0dc994"

def get_weather(city):
    url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={WEATHER_API_KEY}&units=metric&lang=ru'
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        city = data['name']
        temp = data['main']['temp']
        description = data['weather'][0]['description']
        weather_info = f"Погода в {city}:\nТемпература: {temp}°C\nОписание: {description}"
        return weather_info
    else:
        return "Не удалось получить данные о погоде. Убедитесь, что город введен правильно."

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text('Привет! Я бот Данислана, который может показать погоду. Используй команду /weather <город>, чтобы узнать прогноз погоды.')

async def weather(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if context.args:
        city = ' '.join(context.args)
        weather_info = get_weather(city)
        await update.message.reply_text(weather_info)
    else:
        await update.message.reply_text("Пожалуйста, укажите название города после команды /weather.")

def main():
    application = ApplicationBuilder().token(TELEGRAM_TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("weather", weather))

    # Запуск бота
    application.run_polling()

if __name__ == '__main__':
    main()
