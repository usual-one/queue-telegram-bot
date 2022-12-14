import dotenv

from src.services.bot import Bot



def main() -> None:
    dotenv.load_dotenv()
    token = dotenv.dotenv_values()['telegram_token']
    date_format = dotenv.dotenv_values()['date_format']

    bot = Bot(token, date_format)
    bot.idle()

if __name__ == '__main__':
    main()
