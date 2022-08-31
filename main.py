import dotenv

from src.services.bot import Bot



def main() -> None:
    dotenv.load_dotenv()
    token = dotenv.dotenv_values()['telegram_token']

    bot = Bot(token)
    bot.idle()

if __name__ == '__main__':
    main()
