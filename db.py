from abc import ABC, abstractmethod
import pymongo
from emoji import emojize
from pymongo import MongoClient
from datetime import datetime
from timeutil import FUSO


class DbClient(ABC):
    def __init__(self, mogodb_uri):
        self.client = MongoClient(mogodb_uri)
        self.db = self.client.get_default_database()

    # Funçao para inserir uma nova carona no banco de dados
    @abstractmethod
    def insere_bd(self, carona):
        pass

    # Funçao para recuperar a lista de caronas ativas
    @abstractmethod
    def busca_bd(self, tipo, chat_id):
        pass

    # Funçao para desativar caronas
    @abstractmethod
    def desativar_bd(self, tipo, chat_id, username):
        pass

    # Funçao para alterar o número de vagas
    @abstractmethod
    def set_vagas_bd(self, tipo, chat_id, username):
        pass

    # Funçao para desconectar cliente do banco
    @abstractmethod
    def desconectar(self):
        pass

    def __del__(self):
        if self.client is not None:
            self.desconectar()


class MongoDbClient(DbClient):
    def __init__(self, mongodb_uri):
        super().__init__(mongodb_uri)

    def insere_bd(self, carona):
        caronas_col = self.db.caronas
        conditions = {
            "ativo": 1, "tipo": carona["tipo"], "chat_id": carona["chat_id"],
            "username": carona["username"]}
        if caronas_col.count_documents(conditions) > 0:
            caronas_col.update_many(conditions, {"$set": {"ativo": 0}})
        caronas_col.insert_one(carona)

    def busca_bd(self, tipo, chat_id):
        caronas_col = self.db.caronas

        # Verifica se tem caronas para antes do horário atual ainda ativas e desativa-as
        time = datetime.now(FUSO)
        margem = datetime(time.year, time.month, time.day,
                          time.hour + (-1 if time.minute < 20 else 0),
                          time.minute + (40 if time.minute < 20 else -20))

        conditions = {"ativo": 1, "chat_id": chat_id, "horario": {"$lt": margem}}
        if caronas_col.count_documents(conditions) > 0:
            caronas_col.update_many(conditions, {"$set": {"ativo": 0}})

        res = caronas_col.find(
            {"ativo": 1, "tipo": tipo, "chat_id": chat_id}).sort(
            "horario", pymongo.ASCENDING)

        msg = ""
        dia = 0
        for carona in res:
            if carona["horario"].day != dia:
                dia = carona["horario"].day
                mes = carona["horario"].month
                msg += "\n%s *%s/%s*\n" % (emojize(":calendar:", use_aliases=True), str(dia), str(mes))
            carona_dsc = carona["horario"].time().strftime("%X")[:5] + \
                " - @" + carona["username"] + " " + \
                carona.get("notes", "")
            emoj = ":no_entry_sign:" if carona['vagas'] == 0 else ":white_check_mark:"
            msg += "%s (%s vagas) %s\n" % (carona_dsc, carona['vagas'],  emojize(emoj, use_aliases=True))
        return msg

    def desativar_bd(self, tipo, chat_id, username):
        caronas_col = self.db.caronas
        conditions = {"ativo": 1, "tipo": tipo, "username": username, "chat_id": chat_id}
        if caronas_col.count_documents(conditions) > 0:
            caronas_col.update_many(conditions, {"$set": {"ativo": 0}})

    def set_vagas_bd(self, tipo, chat_id, username, vagas=4):
        caronas_col = self.db.caronas
        conditions = {"ativo": 1, "tipo": tipo, "username": username, "chat_id": chat_id}
        if caronas_col.count_documents(conditions) > 0:
            caronas_col.update_many(conditions, {"$set": {"vagas": vagas}})
            return True
        else:
            return False

    def desconectar(self):
        if self.client is not None:
            self.client.close()
