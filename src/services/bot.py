import telegram as tg
import telegram.ext as tg_ext

from .user_service import UserService
from .locale_service import LocaleService


class Bot:

    def __init__(self, token: str) -> None:
        self.__updater = tg_ext.Updater(token=token)
        self.__dispatcher = self.__updater.dispatcher

        self.__users = UserService()
        self.__locale = LocaleService()

        self.__register_handlers()

    def __register_handlers(self) -> None:
        self.__dispatcher.add_handler(tg_ext.CommandHandler('start', self.__start_command_handler))


    # region Command handlers

    def __start_command_handler(self,
                                update: tg.Update,
                                context: tg_ext.CallbackContext) -> None:
        tg_user = update.effective_user
        self.__users.append(tg_user)

        context.bot.sendMessage(chat_id=tg_user.id,
                                text=self.__locale.get_by_key('start_response'))


    # endregion


    #region State

    def idle(self) -> None:
        self.__updater.start_polling()
        print('Bot has started')
        self.__updater.idle()

    #endregion
