import telegram as tg
import telegram.ext as tg_ext

from .locale_service import LocaleService
from .state_service import StateService
from .user_service import UserService

from ..entities.user_state import UserStateValue
from ..entities.user_role import UserRole


class Bot:

    def __init__(self, token: str) -> None:
        self.__updater = tg_ext.Updater(token=token)
        self.__dispatcher = self.__updater.dispatcher

        self.__locale = LocaleService()
        self.__states = StateService()
        self.__users = UserService()

        self.__register_handlers()

    def __register_handlers(self) -> None:
        self.__dispatcher.add_handler(tg_ext.CommandHandler('start', self.__start_command_handler))
        self.__dispatcher.add_handler(tg_ext.CommandHandler('create', self.__create_command_handler))
        self.__dispatcher.add_handler(tg_ext.CommandHandler('cancel', self.__cancel_command_handler))


    # region Command handlers

    def __start_command_handler(self,
                                update: tg.Update,
                                context: tg_ext.CallbackContext) -> None:
        tg_user = update.effective_user

        self.__users.append(tg_user)
        if self.__states.get(tg_user.id) != UserStateValue.NONE:
            context.bot.sendMessage(chat_id=tg_user.id,
                                    text=self.__locale.get_by_key('cancel_response'))
        self.__states.set(tg_user.id, UserStateValue.NONE)

        context.bot.sendMessage(chat_id=tg_user.id,
                                text=self.__locale.get_by_key('start_response'))

    def __create_command_handler(self,
                                 update: tg.Update,
                                 context: tg_ext.CallbackContext) -> None:
        tg_user = update.effective_user

        if self.__users.get(tg_user.id).role != UserRole.ADMIN\
            or self.__states.get(tg_user.id) != UserStateValue.NONE:
            context.bot.sendMessage(chat_id=tg_user.id,
                                    text=self.__locale.get_by_key('unknown_command'))
            return

        self.__states.set(tg_user.id, UserStateValue.EVENT_NAME_CREATING)
        context.bot.sendMessage(chat_id=tg_user.id,
                                text=self.__locale.get_by_key('event_name_input'))

    def __cancel_command_handler(self,
                                 update: tg.Update,
                                 context: tg_ext.CallbackContext) -> None:
        tg_user = update.effective_user

        if self.__users.get(tg_user.id).role != UserRole.ADMIN\
                or self.__states.get(tg_user.id) == UserStateValue.NONE:
            context.bot.sendMessage(chat_id=tg_user.id,
                                    text=self.__locale.get_by_key('unknown_command'))
            return

        self.__states.set(tg_user.id, UserStateValue.NONE)
        context.bot.sendMessage(chat_id=tg_user.id,
                                text=self.__locale.get_by_key('cancel_response'))

    # endregion


    #region State

    def idle(self) -> None:
        self.__updater.start_polling()
        print('Bot has started')
        self.__updater.idle()

    #endregion
