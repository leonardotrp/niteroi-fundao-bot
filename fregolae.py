import telegram
from telegram.ext import Updater, CommandHandler
import os
import features
from messages import MSGS
# If you want to test bot without persistence
# from tests import DummyDb
from db import MongoDbClient

import logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.DEBUG)
logger = logging.getLogger(__name__)


class CaronaBot(object):
    def __init__(self, bd_cliente):
        self.bd_cliente = bd_cliente
        self.features = [
            features.Caronas(self.bd_cliente), features.Ida(self.bd_cliente),
            features.Volta(self.bd_cliente), features.Bairros(self.bd_cliente),
            features.Vagas(self.bd_cliente), features.Remover(self.bd_cliente),
            features.Ola(None), features.Ajuda(None), features.Sobre(None)]
        self.feature_handler = {}
        self.init_features()

    def init_features(self):
        for f in self.features:
            self.feature_handler[f.NOME] = f
            dispatcher.add_handler(CommandHandler(f.NOME, self.command_handler, pass_args=True))

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
            bot.send_message(chat_id=chat_id, text=res, parse_mode=telegram.ParseMode.HTML)
        else:
            for message in message_text.split('\n'):
                cmd = message.replace("@", " ").split(' ')[0].replace('/', '')
                cmd_args = CaronaBot.__get_cmd_args__(cmd, message, args)
                try:
                    cmd_args = cmd_args if cmd not in ("ola", "ajuda", "sobre") else self.features
                    res = self.feature_handler[cmd].processar(user.username, chat_id, cmd_args)
                except Exception as e:
                    logger.error(e.__str__())
                    return "%s (%s)" % (MSGS["general_error"], e.__str__())
                bot.send_message(chat_id=chat_id, text=res, parse_mode=telegram.ParseMode.HTML)


if __name__ == '__main__':
    MONGO = os.environ.get("FREGOLAE_MLAB")
    TOKEN = os.environ.get('FREGOLAE_TOKEN')
    updater = Updater(token=TOKEN)
    dispatcher = updater.dispatcher
    CaronaBot(MongoDbClient(MONGO))
    updater.start_polling()
