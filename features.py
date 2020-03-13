import logging
import os
import re
from abc import ABC

from telegram.error import Unauthorized

import util
from util import emoji
from messages import MSGS

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

GROUP_ID = -1001330301957
GROUP_TEST_ID = -302317240
BOT_USERNAME = 'niteroi_fundao_bot'
BOT_TEST_USERNAME = 'caronas_fundao_bot'
RIDER_BOT_USERNAME = 'niteroi_fundao_rider_bot'


class BotFeature(ABC):
    NOME = ""
    DESCRIPTION = ""

    def __init__(self, bd_cliente, driver_mode=False):
        self.bd_cliente = bd_cliente
        self.group_id = int(os.environ.get("GROUP_ID"))
        self.driver_mode = driver_mode

    @staticmethod
    def is_group_chat(chat_id):
        return chat_id in [GROUP_ID, GROUP_TEST_ID]  # group chat

    @staticmethod
    def is_private_chat(user, chat_id):
        return chat_id == user.id  # private chat

    @staticmethod
    def is_bot_driver(bot):
        return bot.username in [BOT_USERNAME, BOT_TEST_USERNAME]  # bot to driver

    @staticmethod
    def is_bot_rider(bot):
        return bot.username == RIDER_BOT_USERNAME  # bot to rider

    def processar(self, bot, user, chat_id, args):
        membro = self.bd_cliente.get_membro(user.id)
        if self.is_group_chat(chat_id):
            if not membro:
                self.bd_cliente.insere_membro(user) # TODO depois que ficar garantido que todos os usuários do grupo estão devidamente cadastrados, retirar essa inclusão automática
        elif not self.is_private_chat(user, chat_id) or not membro or membro['ativo'] == 0:
            raise Unauthorized(MSGS['unauthorized_error'])


class BaseIdaVolta(BotFeature):
    TYPE = 1
    NOME = 'ida'
    DESCRIPTION = f"ida_description"

    def processar(self, bot, user, chat_id, args):
        super(BaseIdaVolta, self).processar(bot, user, chat_id, args)
        chat_id = self.group_id
        if len(args) == 0:
            try:
                return MSGS[f"{self.NOME}_titulo"] + self.bd_cliente.busca_bd(self.TYPE, chat_id, args)
            except Exception as e:
                logger.error(e.__str__())
                return "%s (%s)" % (MSGS["list_error"], e.__str__())
        elif len(args) < 3:
            return MSGS["ida_err"]
        else:
            try:
                carona = util.valida_horario(args[0])
                vagas = util.valida_vagas(self.NOME, args)
                bairro = util.valida_bairro(self, args[2])
                notes = "" if len(args) == 3 else " ".join(args[3:])
                carona.update({
                    'username': user.username,
                    'chat_id': chat_id,
                    'tipo': self.TYPE,
                    'ativo': 1,
                    'vagas': vagas,
                    'notes': notes,
                    'bairro': bairro
                })
                self.bd_cliente.insere_bd(carona)
                return self.get_message(user.username, carona)
            except ValueError as e:
                logger.error(e.__str__())
                return e.__str__()
            except Exception as e:
                logger.error(e.__str__())
                return "%s (%s)" % (MSGS["add_error"], e.__str__())

    def get_message(self, username, carona):
        data_carona = carona["horario"].time().strftime("%X")[:5]
        vagas = carona["vagas"]
        preffix = "IDA" if self.TYPE == 1 else "VOLTA"
        suffix = "origem" if self.TYPE == 1 else "destino"
        suffix = "%s '%s'" % (suffix, carona['bairro']['nome'])
        return f"Carona de {preffix} às {data_carona} " + \
            f"oferecida por @{username}, {suffix} com {vagas} vagas.\nObs.: {carona.get('notes', '')}"


class Ida(BaseIdaVolta):
    pass


class Volta(BaseIdaVolta):
    TYPE = 2
    NOME = 'volta'
    DESCRIPTION = f"volta_description"


class Vagas(BotFeature):
    NOME = "vagas"
    DESCRIPTION = "vagas_description"

    def processar(self, bot, user, chat_id, args):
        super(Vagas, self).processar(bot, user, chat_id, args)
        chat_id = self.group_id
        if len(args) != 2 or args[0] not in ("ida", "volta") or not re.search(r'^[0-4]+$', args[1]):
            return MSGS["vagas_err"]
        else:
            tipo = 1 if args[0] == "ida" else 2
            vagas = int(args[1])
            if self.bd_cliente.set_vagas_bd(tipo, chat_id, user.username, vagas):
                return str.format(MSGS["vaga_alterarda"], args[0], vagas)
            else:
                return str.format(MSGS["vagas_inexistentes"], args[0])


class Bairros(BotFeature):
    NOME = "bairros"
    DESCRIPTION = "bairros_description"

    def processar(self, bot, user, chat_id, args):
        super(Bairros, self).processar(bot, user, chat_id, args)
        return MSGS["bairros_header"] + self.bd_cliente.bairros_bd()


class Remover(BotFeature):
    NOME = "remover"
    DESCRIPTION = "remove_description"

    def processar(self, bot, user, chat_id, args):
        super(Remover, self).processar(bot, user, chat_id, args)
        chat_id = self.group_id
        if len(args) != 1 or args[0] not in ("ida", "volta"):
            return MSGS["remove_err"]
        else:
            tipo = 1 if args[0] == "ida" else 2
            self.bd_cliente.desativar_bd(tipo, chat_id, user.username)
            return str.format(MSGS["removed"], args[0])


class Caronas(BotFeature):
    NOME = "caronas"
    DESCRIPTION = "caronas_description"

    def processar(self, bot, user, chat_id, args):
        super(Caronas, self).processar(bot, user, chat_id, args)
        chat_id = self.group_id
        try:
            ida = self.bd_cliente.busca_bd(1, chat_id, args)
            volta = self.bd_cliente.busca_bd(2, chat_id, args)
            return MSGS["caronas_header"] + MSGS["ida_titulo"] + ida + MSGS["volta_titulo"] + volta
        except Exception as e:
            logger.error(e.__str__())
            return "%s (%s)" % (MSGS["add_error"], e.__str__())


class Start(BotFeature):
    NOME = "start"

    def processar(self, bot, user, chat_id, args):
        super(Start, self).processar(bot, user, chat_id, args)
        if self.is_group_chat(chat_id):
            group_start_msg = open("files/start_group.txt", "r").read()
            return group_start_msg.format(member_name=user.first_name, bem_vindo='Seja bem-vindo.')
        elif self.is_private_chat(user, chat_id):
            if self.is_bot_driver(bot):
                private_start_msg = open("files/start_private.txt", "r").read()
            elif self.is_bot_rider(bot):
                private_start_msg = open("files/start_private_rider.txt", "r").read()
            return private_start_msg.format(member_name=user.first_name)


class Ajuda(BotFeature):
    NOME = "ajuda"

    def processar(self, bot, user, chat_id, args):
        super(Ajuda, self).processar(bot, user, chat_id, args)
        features = ''
        idx = 0
        for feature in args:
            if feature.NOME not in ("start", "ajuda", "sobre"):
                show = not feature.driver_mode or (self.is_bot_driver(bot) and feature.driver_mode)
                if show:
                    features += str.format(MSGS["feature_line"], (idx+1), feature.NOME, MSGS.get(feature.DESCRIPTION))
                    idx = idx + 1
        msg = open("files/help.txt", "r").read()
        msg = msg.format(emoji_title=emoji('book'),
                         features=features,
                         emoji_obs_1=emoji('bust_in_silhouette'),
                         emoji_obs_2=emoji('hourglass'),
                         emoji_obs_3=emoji('car'),
                         emoji_obs_4=emoji('thumbsup'),
                         emoji_obs_5=emoji('warning'))
        return msg


class Sobre(BotFeature):
    NOME = "sobre"

    def processar(self, bot, user, chat_id, args):
        super(Sobre, self).processar(bot, user, chat_id, args)
        return open("files/about.txt", "r").read()


class Regras(BotFeature):
    NOME = "regras"
    DESCRIPTION = f"regras_description"

    def processar(self, bot, user, chat_id, args):
        super(Regras, self).processar(bot, user, chat_id, args)
        return open("files/rules.txt", "r").read()


class Seguranca(BotFeature):
    NOME = "seguranca"
    DESCRIPTION = f"seguranca_description"

    def processar(self, bot, user, chat_id, args):
        super(Seguranca, self).processar(bot, user, chat_id, args)
        return open("files/security.txt", "r").read()


class Praticas(BotFeature):
    NOME = "praticas"
    DESCRIPTION = f"praticas_description"

    def processar(self, bot, user, chat_id, args):
        super(Praticas, self).processar(bot, user, chat_id, args)
        return open("files/practices.txt", "r").read()


class Moderadores(BotFeature):
    NOME = "moderadores"
    DESCRIPTION = f"moderadores_description"

    def processar(self, bot, user, chat_id, args):
        super(Moderadores, self).processar(bot, user, chat_id, args)
        return open("files/moderators.txt", "r").read()