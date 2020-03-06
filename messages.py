from emoji import emojize

MSGS = {
    "list_error": "%s Ocorreu um erro ao buscar a lista. Tente novamente." % emojize(":warning:", use_aliases=True),
    "add_error": "%s Ocorreu um erro ao adicionar a carona. Tente novamente." % emojize(":warning:", use_aliases=True),
    "invalid_time_error": "Horário inválido! %s" % emojize(":flushed:", use_aliases=True),
    "ida_err": "IDA inválida! %s Uso: /ida [hh:mm] [0-4] [cód.bairro] [obs de ida]" % emojize(":flushed:", use_aliases=True),
    "volta_err": "VOLTA inválida! %s Uso: /volta [hh:mm] [0-4] [cód.bairro] [obs de volta]" % emojize(":flushed:", use_aliases=True),
    "vagas_err": "Alteração de vagas inválida! %s Uso: /vagas [ida ou volta] [0-4]" % emojize(":flushed:", use_aliases=True),
    "bairro_err": "Bairro inválido! %s Verifique o código do seu bairro através do comando /bairros" % emojize(":flushed:", use_aliases=True),
    "vagas_inexistentes": "%s Você precisa primeiro cadastrar uma carona de {0}." % emojize(":no_entry:", use_aliases=True),
    "username_error": "%s Crie um username nas configurações do seu Telegram para poder utilizar este Bot" % emojize(":no_entry:", use_aliases=True),
    "general_error": "%s Ocorreu um erro. Tente novamente." % emojize(":warning:", use_aliases=True),
    "general_start": "Olá <b>{member_name}</b>! Eu sou o <b><a href='https://t.me/niteroi_fundao_bot'>NiteroiFundaoBot</a></b> e sou o responsável pelo gerenciamento das caronas." +
             "\n\nSeja bem-vindo e boas caronas!",
    "caronas_header": "%s <b>CARONAS</b> %s" % (emojize(":blue_car:", use_aliases=True), emojize(":car:", use_aliases=True)),
    "bairros_header": "%s <b>REGIÕES - BAIRROS</b>\n----------------------------------\n" % emojize(":house_with_garden:", use_aliases=True),
    "ida_titulo": "\n------------------------\n%s <b>IDA</b>\n" % emojize(":arrow_heading_up:", use_aliases=True),
    "volta_titulo": "\n------------------------\n%s <b>VOLTA</b>\n" % emojize(":arrow_heading_down:", use_aliases=True),
    "removed": "Carona de {0} removida com sucesso! %s" % emojize(":wink:", use_aliases=True),
    "vaga_alterarda": "Sua carona de {0} agora possui {1} vagas %s" % emojize(":wink:", use_aliases=True),
    "remove_err": "Entrada inválida! %s (Ex: /remover volta ou /remover ida)" % emojize(":flushed:", use_aliases=True),
    "feature_line": "<b>{0})</b> /{1}{2}",
    "ida_description": " : Inclui uma carona de IDA.\n" +
                       "\tFormato: /ida [hh:mm] [0-4] [cód.bairro] [obs de ida].\n" +
                       "\tObs: O horário de IDA é o de <b>chegada</b> no Fundão.\n",
    "volta_description": " : Inclui uma carona de VOLTA.\n" +
                         "\t\tFormato: /volta [hh:mm] [0-4] [cód.bairro] [obs de volta].\n" +
                         "\t\tObs: O horário de VOLTA é o de <b>saída</b> do Fundão.\n",
    "remove_description": " : Remove uma carona.\n" +
                          "\t\tFormato: /remover [ida ou volta].\n",
    "vagas_description": " : Altera o número de vagas.\n" +
                         "\t\tFormato: /vagas [ida ou volta] [0-4]\n",
    "bairros_description": " : Lista todos os bairros e suas regiões.\n",
    "caronas_description": " : Lista das caronas, com filro opcional.\n" +
                           "\t\tFormato: /caronas [filtro]\n" +
                           "\t\tObs: O filtro pode ser código/nome do bairro/região ou parte da observação da carona.\n",
    "regras_description": " : Lista as regras do grupo.\n",
    "seguranca_description": " : Dicas para uma carona segura.\n",
    "moderadores_description": " : Lista os moderadores do grupo.\n",
    "praticas_description": " : Boas práticas para uma boa carona.\n"
}
