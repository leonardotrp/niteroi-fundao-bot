import logging
import os
import re
from abc import ABC

from telegram.error import Unauthorized

import util
from messages import MSGS

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

NITEROI_FUNDAO_ID = -1001330301957
NITEROI_FUNDAO_TEST_ID = -302317240


class BotFeature(ABC):
    NOME = ""
    DESCRIPTION = ""

    def __init__(self, bd_cliente):
        self.bd_cliente = bd_cliente
        self.group_id = int(os.environ.get("NITEROI_FUNDAO_ID"))

    @staticmethod
    def is_group_chat(chat_id):
        return chat_id in [NITEROI_FUNDAO_ID, NITEROI_FUNDAO_TEST_ID]  # group chat

    @staticmethod
    def is_private_chat(user, chat_id):
        return chat_id == user.id  # private chat

    def processar(self, user, chat_id, args):
        membro = self.bd_cliente.get_membro(user.id)
        if self.is_group_chat(chat_id):
            if not membro:
                self.bd_cliente.insere_membro(user) # TODO depois que ficar garantido que todos os usuários do grupo estão devidamente cadastrados, retirar essa inclusão automática
        elif not self.is_private_chat(user, chat_id) or not membro or membro['ativo'] == 0:
            raise Unauthorized('Desculpe-me. Você não tem permissão para usar este Bot.\n\nSe você for um membro do nosso grupo de caronas, envie um comando ao Bot de dentro do grupo e volte aqui novamente.')


class BaseIdaVolta(BotFeature):
    TYPE = 1
    NOME = 'ida'
    DESCRIPTION = f"ida_description"

    def processar(self, user, chat_id, args):
        super(BaseIdaVolta, self).processar(user, chat_id, args)
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

    def processar(self, user, chat_id, args):
        super(Vagas, self).processar(user, chat_id, args)
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

    def processar(self, user, chat_id, args):
        super(Bairros, self).processar(user, chat_id, args)
        return MSGS["bairros_header"] + self.bd_cliente.bairros_bd()


class Remover(BotFeature):
    NOME = "remover"
    DESCRIPTION = "remove_description"

    def processar(self, user, chat_id, args):
        super(Remover, self).processar(user, chat_id, args)
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

    def processar(self, user, chat_id, args):
        super(Caronas, self).processar(user, chat_id, args)
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

    def processar(self, user, chat_id, args):
        super(Start, self).processar(user, chat_id, args)
        if self.is_group_chat(chat_id):
            return MSGS["group_start"].format(member_name=user.first_name, bem_vindo='Seja bem-vindo.')
        elif self.is_private_chat(user, chat_id):
            return MSGS["private_start"].format(member_name=user.first_name)


class Ajuda(BotFeature):
    NOME = "ajuda"

    def processar(self, user, chat_id, args):
        super(Ajuda, self).processar(user, chat_id, args)
        msg = MSGS["help_header"]
        i = 1
        for f in args:
            if f.NOME in ("start", "ajuda", "sobre"):
                continue
            msg += str.format(MSGS["feature_line"], i, f.NOME, MSGS.get(f.DESCRIPTION, f.DESCRIPTION))
            i += 1
        msg += MSGS["help_footer"]
        return msg


class Sobre(BotFeature):
    NOME = "sobre"

    def processar(self, user, chat_id, features):
        return MSGS["sobre"]
