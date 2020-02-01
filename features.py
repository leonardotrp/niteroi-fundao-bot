from abc import ABC, abstractmethod
from messages import MSGS
import util
import logging
import re

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)


class BotFeature(ABC):
    NOME = ""
    DESCRIPTION = ""

    def __init__(self, bd_cliente):
        self.bd_cliente = bd_cliente

    # Método abstrato para processar uma mensagem e retornar mensagem resposta
    @abstractmethod
    def processar(self, username, chat_id, args):
        pass


class BaseIdaVolta(BotFeature):
    TYPE = 1
    NOME = 'ida'
    DESCRIPTION = f"ida_description"

    def processar(self, username, chat_id, args):
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
                    'username': username,
                    'chat_id': chat_id,
                    'tipo': self.TYPE,
                    'ativo': 1,
                    'vagas': vagas,
                    'notes': notes,
                    'bairro': bairro
                })
                self.bd_cliente.insere_bd(carona)
                return self.get_message(username, carona)
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

    def processar(self, username, chat_id, args):
        if len(args) != 2 or args[0] not in ("ida", "volta") or not re.search(r'^[0-4]+$', args[1]):
            return MSGS["vagas_err"]
        else:
            tipo = 1 if args[0] == "ida" else 2
            vagas = int(args[1])
            if self.bd_cliente.set_vagas_bd(tipo, chat_id, username, vagas):
                return str.format(MSGS["vaga_alterarda"], args[0], vagas)
            else:
                return str.format(MSGS["vagas_inexistentes"], args[0])


class Bairros(BotFeature):
    NOME = "bairros"
    DESCRIPTION = "bairros_description"

    def processar(self, username, chat_id, args):
        return MSGS["bairros_header"] + self.bd_cliente.bairros_bd()


class Remover(BotFeature):
    NOME = "remover"
    DESCRIPTION = "remove_description"

    def processar(self, username, chat_id, args):
        if len(args) != 1 or args[0] not in ("ida", "volta"):
            return MSGS["remove_err"]
        else:
            tipo = 1 if args[0] == "ida" else 2
            self.bd_cliente.desativar_bd(tipo, chat_id, username)
            return str.format(MSGS["removed"], args[0])


class Caronas(BotFeature):
    NOME = "caronas"
    DESCRIPTION = "caronas_description"

    def processar(self, username, chat_id, args):
        try:
            ida = self.bd_cliente.busca_bd(1, chat_id, args)
            volta = self.bd_cliente.busca_bd(2, chat_id, args)
            return MSGS["caronas_header"] + MSGS["ida_titulo"] + ida + MSGS["volta_titulo"] + volta
        except Exception as e:
            logger.error(e.__str__())
            return "%s (%s)" % (MSGS["add_error"], e.__str__())


class Start(BotFeature):
    NOME = "start"

    def processar(self, username, chat_id, args):
        return MSGS["start"]


class Ajuda(BotFeature):
    NOME = "ajuda"

    def processar(self, username, chat_id, features):
        msg = MSGS["help_header"]
        i = 1
        for f in features:
            if f.NOME in ("start", "ajuda", "sobre"):
                continue
            msg += str.format(MSGS["feature_line"], i, f.NOME, MSGS.get(f.DESCRIPTION, f.DESCRIPTION))
            i += 1
        msg += MSGS["help_footer"]
        return msg


class Sobre(BotFeature):
    NOME = "sobre"

    def processar(self, username, chat_id, features):
        return MSGS["sobre"]
