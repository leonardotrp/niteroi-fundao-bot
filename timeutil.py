import datetime
from pytz import timezone
FUSO = timezone("America/Bahia")


def valida_horario(arg):
    try:
        today = datetime.datetime.now(FUSO)
        hour = datetime.datetime.strptime(arg, "%H:%M")
        data_hora = datetime.datetime(today.year, today.month, today.day, hour.hour, hour.minute, tzinfo=today.tzinfo)
        if today > data_hora:
            data_hora = datetime.datetime(today.year, today.month, today.day+1, hour.hour, hour.minute)
        return {"horario": data_hora.replace(tzinfo=None)}
    except ValueError as e:
        print("ValueError %s" % e.__str__())
        raise e
    # Do your logic for invalid format (maybe print some message?).