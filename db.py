from abc import ABC, abstractmethod
import pymongo
import logging
import re
from emoji import emojize
from pymongo import MongoClient
from datetime import datetime
from util import FUSO

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)


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
    def busca_bd(self, tipo, chat_id, args):
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

    @abstractmethod
    def get_membro(self, membro_id):
        pass

    @abstractmethod
    def ativar_membro(self, membro_id, ativar):
        pass

    @abstractmethod
    def insere_membro(self, membro):
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

    def filtro_bairros(self, args, filtros):
        if len(args) > 0:
            filtro = " ".join(args[0:])

            try:
                id = int(filtro)

                # tenta filtrar bairros pelo código do bairro
                bairro_by_id = self.get_bairro(id)
                if bairro_by_id:
                    return [bairro_by_id]

                # tenta filtrar bairros pelo codigo da região
                bairros_by_regiao = self.get_bairros(id)
                if bairros_by_regiao:
                    return bairros_by_regiao

            except Exception:
                bairros = []
                # tenta filtrar bairros pelo nome da região
                regiao_by_name = list(self.db.regioes.find({'nome': re.compile(filtro, re.IGNORECASE)}))
                if len(regiao_by_name) > 0:
                    bairros_by_regiao = self.get_bairros(regiao_by_name[0]['id'])
                    if bairros_by_regiao:
                        bairros.extend(bairros_by_regiao)

                # tenta filtrar bairros pelo nome do bairro
                bairros_by_name = list(self.db.bairros.find({'nome': re.compile(filtro, re.IGNORECASE)}))
                if len(bairros_by_name) > 0:
                    bairros.extend(bairros_by_name)

                # tenta filtrar bairros pela nota das caronas
                filtro_caronas = {}
                filtro_caronas.update(filtros)
                filtro_caronas.update({'notes': re.compile(filtro, re.IGNORECASE)})
                for carona in self.db.caronas.find(filtro_caronas):
                    bairros.append(carona['bairro'])

                return bairros

        return None

    def busca_bd(self, tipo, chat_id, args):
        caronas_col = self.db.caronas

        # Verifica se tem caronas para antes do horário atual ainda ativas e desativa-as
        time = datetime.now(FUSO)
        margem = datetime(time.year, time.month, time.day,
                          time.hour + (-1 if time.minute < 20 else 0),
                          time.minute + (40 if time.minute < 20 else -20))

        conditions = {"ativo": 1, "chat_id": chat_id, "horario": {"$lt": margem}}
        if caronas_col.count_documents(conditions) > 0:
            caronas_col.update_many(conditions, {"$set": {"ativo": 0}})

        filtros = {"ativo": 1, "tipo": tipo, "chat_id": chat_id}
        bairros = self.filtro_bairros(args, filtros)
        if bairros is not None:
            filtros.update({'bairro': {'$in': bairros}})

        res = caronas_col.find(filtros).sort("horario", pymongo.ASCENDING)
        msg = ""
        dia = 0
        for carona in res:
            if carona["horario"].day != dia:
                dia = carona["horario"].day
                mes = carona["horario"].month
                msg += "\n%s <b>%s/%s</b>\n" % (emojize(":calendar:", use_aliases=True), str(dia), str(mes))
            horario = carona["horario"].time().strftime("%X")[:5]
            username = '@%s' % carona['username']
            bairro = carona['bairro']['nome']
            vagas = carona['vagas']
            notes = carona.get("notes", "")
            carona_dsc = f"<b>{horario}</b> - {username} - {bairro} ({vagas} vagas). {notes}"
            carona_dsc = ("<s>%s</s>" % carona_dsc) if carona['vagas'] == 0 else carona_dsc
            msg += "%s\n" % carona_dsc
        return msg

    def bairros_bd(self):
        msg = ''
        for regiao in self.db.regioes.find().sort([('id', 1)]):
            msg += '\t<b>%s. %s</b>\n' % (regiao['id'], regiao['nome'])
            bairros = self.db.bairros.find({'regiao_id': regiao['id']}).sort([('id', 1)])
            for bairro in bairros:
                msg += '\t\t\t%s. %s\n' % (bairro['id'], bairro['nome'])
        return msg

    def get_bairro(self, bairro_id):
        return self.db.bairros.find_one({'id': bairro_id})

    def get_bairros(self, regiao_id):
        return list(self.db.bairros.find({'regiao_id': regiao_id}))

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

    def get_membro(self, membro_id):
        return self.db.membros.find_one({'id': membro_id})

    def ativar_membro(self, membro_id, ativar):
        membro = self.db.membros.find_one_and_update({'id': membro_id}, {'$set': {'ativo': ativar}})
        return True if membro else False

    def insere_membro(self, user):
        membro = {
            'id': user.id,
            'username': user.username,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'ativo': 1
        }
        self.db.membros.insert_one(membro)