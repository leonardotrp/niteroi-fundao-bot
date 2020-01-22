import datetime
import logging
import re

from pytz import timezone

from messages import MSGS

FUSO = timezone("America/Bahia")

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.DEBUG)
logger = logging.getLogger(__name__)


def valida_horario(arg):
    try:
        today = datetime.datetime.now(FUSO)
        hour = datetime.datetime.strptime(arg, "%H:%M")
        data_hora = datetime.datetime(today.year, today.month, today.day, hour.hour, hour.minute, tzinfo=today.tzinfo)
        if today > data_hora:
            data_hora = datetime.datetime(today.year, today.month, today.day+1, hour.hour, hour.minute)
        return {"horario": data_hora.replace(tzinfo=None)}
    except ValueError as e:
        logger.error(e.__str__())
        raise ValueError(MSGS["invalid_time_error"])
    # Do your logic for invalid format (maybe print some message?).


def valida_vagas(args):
    if len(args) > 1 and not re.search(r'^[0-4]+$', args[1]):
        raise ValueError(MSGS["ida_err"])
    return int(args[1])


def valida_bairro(feature, arg):
    bairro = feature.bd_cliente.get_bairro(int(arg))
    if not bairro:
        raise ValueError(MSGS['bairro_err'])
    return bairro