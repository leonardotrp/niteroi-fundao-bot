import logging
import os

import telegram
from telegram.error import Unauthorized
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

import features
# If you want to test bot without persistence
# from tests import DummyDb
from db import MongoDbClient
from messages import MSGS

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)


class CaronaBot(object):
    def __init__(self, bd_cliente):
        self.bd_cliente = bd_cliente
        self.features = [
            features.Caronas(self.bd_cliente), features.Ida(self.bd_cliente, True),
            features.Volta(self.bd_cliente, True), features.Bairros(self.bd_cliente),
            features.Vagas(self.bd_cliente, True), features.Remover(self.bd_cliente, True),
            features.Start(self.bd_cliente), features.Ajuda(self.bd_cliente),
            features.Regras(self.bd_cliente), features.Seguranca(self.bd_cliente),
            features.Praticas(self.bd_cliente), features.Moderadores(self.bd_cliente),
            features.Sobre(self.bd_cliente)
        ]
        self.feature_handler = {}
        self.init_features()
        self.init_chat_members()

    def init_features(self):
        for f in self.features:
            self.feature_handler[f.NOME] = f
            dispatcher.add_handler(CommandHandler(f.NOME, self.command_handler, pass_args=True))

    def init_chat_members(self):
        new_members_handle = MessageHandler(Filters.status_update.new_chat_members, self.new_chat_members)
        dispatcher.add_handler(new_members_handle)

        left_member_handle = MessageHandler(Filters.status_update.left_chat_member, self.left_chat_member)
        dispatcher.add_handler(left_member_handle)

    def new_chat_members(self, bot, update):
        chat_id = update.message.chat.id
        for user in update.message.new_chat_members:
            if not user.is_bot:
                group_start_msg = open("files/start_group.txt", "r").read()
                if self.bd_cliente.ativar_membro(user.id, 1):
                    res = group_start_msg.format(member_name=user.first_name, bem_vindo='Bem-vindo de volta.')
                else:
                    self.bd_cliente.insere_membro(user)
                    res = group_start_msg.format(member_name=user.first_name, bem_vindo='Seja bem-vindo.')
                bot.send_message(chat_id=chat_id, text=res, parse_mode=telegram.ParseMode.HTML, disable_web_page_preview=True)

    def left_chat_member(self, bot, update):
        user = update.message.left_chat_member
        self.bd_cliente.ativar_membro(user.id, 0) # desativar

    @staticmethod
    def __contains_args__(small, big):
        for i in range(len(big) - len(small) + 1):
            for j in range(len(small)):
                if big[i + j] != small[j]:
                    break
            else:
                return i, i + len(small)
        return False

    @staticmethod
    def __get_cmd_args__(cmd, msg, args):
        cmd_text = '/%s' % cmd
        result_contains = CaronaBot.__contains_args__(msg.split(' '), args)
        if cmd_text in args and result_contains:
            return args[result_contains[0]+1:result_contains[1]]
        elif not result_contains:
            idx_next = len(args)
            for idx in range(0, len(args)):
                if args[idx].startswith('/'):
                    idx_next = idx
                    break
            return args[0:idx_next]

    def command_handler(self, bot, update, args):
        user = update.message.from_user
        chat_id = update.message.chat.id
        message_text = update.message.text
        if user is None or user.username is None:
            res = MSGS["username_error"]
            bot.send_message(chat_id=chat_id, text=res, parse_mode=telegram.ParseMode.HTML, disable_web_page_preview=True)
        else:
            for message in message_text.split('\n'):
                cmd = message.replace("@", " ").split(' ')[0].replace('/', '')
                cmd_args = CaronaBot.__get_cmd_args__(cmd, message, args)
                try:
                    cmd_args = cmd_args if cmd not in ("start", "ajuda", "sobre") else self.features
                    res = self.feature_handler[cmd].processar(bot, user, chat_id, cmd_args)
                except Unauthorized as e:
                    logger.error(e.__str__())
                    res = e.__str__()
                except Exception as e:
                    logger.error(e.__str__())
                    res = "%s (%s)" % (MSGS["general_error"], e.__str__())
                bot.send_message(chat_id=chat_id, text=res, parse_mode=telegram.ParseMode.HTML, disable_web_page_preview=True)


if __name__ == '__main__':
    MONGO = os.environ.get("FREGOLAE_MLAB")
    TOKEN = os.environ.get('FREGOLAE_TOKEN')
    updater = Updater(token=TOKEN)
    dispatcher = updater.dispatcher
    CaronaBot(MongoDbClient(MONGO))

    updater.start_polling()
