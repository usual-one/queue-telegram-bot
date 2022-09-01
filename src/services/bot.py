import telegram as tg
import telegram.ext as tg_ext

from .locale_service import LocaleService
from .state_service import StateService
from .user_service import UserService
from .queue_service import QueueService

from ..entities.user_state import UserStateValue
from ..entities.user_role import UserRole
from ..entities.queue import Queue


class Bot:

    def __init__(self, token: str, date_format: str) -> None:
        self.__date_format = date_format

        self.__updater = tg_ext.Updater(token=token)
        self.__dispatcher = self.__updater.dispatcher

        self.__locale = LocaleService()
        self.__states = StateService()
        self.__users = UserService()
        self.__queues = QueueService(date_format, self.__queue_create_handler)

        self.__register_handlers()

    def __register_handlers(self) -> None:
        self.__dispatcher.add_handler(tg_ext.CommandHandler('start', self.__start_command_handler))
        self.__dispatcher.add_handler(tg_ext.CommandHandler('create', self.__create_command_handler))
        self.__dispatcher.add_handler(tg_ext.CommandHandler('cancel', self.__cancel_command_handler))
        self.__dispatcher.add_handler(tg_ext.MessageHandler(tg_ext.Filters.text, self.__message_handler))


    #region Command handlers

    def __start_command_handler(self,
                                update: tg.Update,
                                context: tg_ext.CallbackContext) -> None:
        tg_user = update.effective_user

        self.__users.append(tg_user)
        if self.__states.get(tg_user.id) != None\
                and self.__states.get(tg_user.id).value != UserStateValue.NONE:
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
            or self.__states.get(tg_user.id).value != UserStateValue.NONE:
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
                or self.__states.get(tg_user.id).value == UserStateValue.NONE:
            context.bot.sendMessage(chat_id=tg_user.id,
                                    text=self.__locale.get_by_key('unknown_command'))
            return

        self.__states.set(tg_user.id, UserStateValue.NONE)
        context.bot.sendMessage(chat_id=tg_user.id,
                                text=self.__locale.get_by_key('cancel_response'))

    #endregion


    #region Message handler

    def __message_handler(self,
                          update: tg.Update,
                          context: tg_ext.CallbackContext) -> None:
        tg_user = update.effective_user
        user_state = self.__states.get(tg_user.id)
        message = update.message.text

        if user_state.value == UserStateValue.NONE:
            context.bot.sendMessage(chat_id=tg_user.id,
                                    text=self.__locale.get_by_key('unknown_command'))
            return

        if user_state.value == UserStateValue.EVENT_NAME_CREATING:
            updated_params = user_state.params.copy()
            updated_params['event_name'] = message

            self.__states.set(tg_user.id, UserStateValue.EVENT_TIME_CREATING, updated_params)
            context.bot.sendMessage(chat_id=tg_user.id,
                                    text=self.__locale.get_with_args('event_time_input', self.__date_format))
            return

        if user_state.value == UserStateValue.EVENT_TIME_CREATING:
            if not self.__queues.is_valid_datetime(message):
                context.bot.sendMessage(chat_id=tg_user.id,
                                        text=self.__locale.get_with_args('wrong_event_time_format', self.__date_format))
                return

            updated_params = user_state.params.copy()
            updated_params['event_time'] = message

            self.__states.set(tg_user.id, UserStateValue.QUEUE_TIME_CREATING, updated_params)
            context.bot.sendMessage(chat_id=tg_user.id,
                                    text=self.__locale.get_with_args('queue_time_input', self.__date_format))
            return

        if user_state.value == UserStateValue.QUEUE_TIME_CREATING:
            if not self.__queues.is_valid_datetime(message):
                context.bot.sendMessage(chat_id=tg_user.id,
                                        text=self.__locale.get_with_args('wrong_queue_time_format', self.__date_format))
                return

            self.__states.set(tg_user.id, UserStateValue.NONE)
            self.__queues.create_queue(user_state.params['event_name'],
                                       user_state.params['event_time'],
                                       message)
            return


    #endregion


    #region Inner events

    def __queue_create_handler(self, queue: Queue) -> None:
        text = self.__locale.get_with_args('new_queue_notifications_off',
                                           queue.event.name,
                                           queue.event.get_time(self.__date_format),
                                           queue.get_start_time(self.__date_format))\
                                                   .replace('!', '\!')\
                                                   .replace('.', '\.')
        for user_id in self.__users.users.keys():
            self.__updater.bot.sendMessage(chat_id=user_id, text=text,
                                           parse_mode=tg.ParseMode.MARKDOWN_V2)

    #endregion


    #region State

    def idle(self) -> None:
        self.__updater.start_polling()
        print('Bot has started')
        self.__updater.idle()

    #endregion
