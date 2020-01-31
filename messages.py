from emoji import emojize

MSGS = {
    "list_error": "%s Ocorreu um erro ao buscar a lista. Tente novamente." % emojize(":warning:", use_aliases=True),
    "add_error": "%s Ocorreu um erro ao adicionar a carona. Tente novamente." % emojize(":warning:", use_aliases=True),
    "invalid_time_error": "Horário inválido! %s" % emojize(":flushed:", use_aliases=True),
    "ida_err": "Entrada inválida! %s ( Ex: /ida {hh:mm} {0-4} {código bairro} {obs ida} )" % emojize(":flushed:", use_aliases=True),
    "vagas_err": "Número de vagas inválido! %s O número de vagas deve estar entre 0 e 4. (Ex: /vagas ida 4 ou /vagas volta 0)" % emojize(":flushed:", use_aliases=True),
    "bairro_err": "Bairro inválido! %s Verifique o código do seu bairro através do comando /bairros" % emojize(":flushed:", use_aliases=True),
    "vagas_inexistentes": "%s Você precisa primeiro cadastrar uma carona de {0}." % emojize(":no_entry:", use_aliases=True),
    "username_error": "%s Crie um username nas configurações do seu Telegram para poder utilizar este Bot" % emojize(":no_entry:", use_aliases=True),
    "general_error": "%s Ocorreu um erro. Tente novamente." % emojize(":warning:", use_aliases=True),
    "start": "Olá! Eu sou o <b>NiteroiFundaoBot</b> e sou o responsável pelo gerenciamento das caronas." +
             "\nPara o bom andamento do grupo, não deixe de ler as <b><a href='https://t.me/c/1330301957/9'>regras</a></b>." +
             "\n\nSeja bem-vindo e boas caronas!",
    "caronas_header": "%s <b>CARONAS</b> %s" % (emojize(":blue_car:", use_aliases=True), emojize(":car:", use_aliases=True)),
    "bairros_header": "%s <b>REGIÕES - BAIRROS</b>\n----------------------------------\n" % emojize(":house_with_garden:", use_aliases=True),
    "ida_titulo": "\n------------------------\n%s <b>IDA</b>\n" % emojize(":arrow_heading_up:", use_aliases=True),
    "volta_titulo": "\n------------------------\n%s <b>VOLTA</b>\n" % emojize(":arrow_heading_down:", use_aliases=True),
    "removed": "Carona de {0} removida com sucesso! %s" % emojize(":wink:", use_aliases=True),
    "vaga_alterarda": "Sua carona de {0} agora possui {1} vagas %s" % emojize(":wink:", use_aliases=True),
    "remove_err": "Entrada inválida! %s (Ex: /remover volta ou /remover ida)" % emojize(":flushed:", use_aliases=True),
    "help_header": "%s Comandos do bot:\n\n" % emojize(":book:", use_aliases=True),
    "help_footer": "<b>OBS</b>:" +
                   "\n\t\t%s Para utilizar o bot, é <b>imprescindível</b> que você tenha seu @username, definido em configurações." % emojize(":bust_in_silhouette:", use_aliases=True) +
                   "\n\t\t%s As caronas desaparecem da lista 20 minutos após passar o horário definido na IDA/VOLTA." % emojize(":hourglass:", use_aliases=True) +
                   "\n\t\t%s Atenção motoristas! Ofereça suas caronas <b>somente</b> através dos comandos /ida e /volta." % emojize(":warning:", use_aliases=True),
    "feature_line": "<b>{0})</b> /{1}{2}",
    "sobre":
        "<b>NiteroiFundaoBot</b>:\n" +
        "\tResponsável técnico: @leonardo_pereira\n"
        "\tAdaptação do <i>FregolaeBot</i>, Bot criado originalmente por @pedropauloskf e @almeidakayan.\n" +
        "\tCódigo fonte: https://github.com/leonardotrp/niteroi-fundao-bot",
    "ida_description": " {hh:mm} {0-4} {código bairro} {obs ida}: Adiciona uma carona de IDA, com o horário de <b>chegada</b> no Fundão, " +
                        "o número de vagas, seguido do código do bairro (origem) e demais informações relevantes (opcional).\n " +
                       "Ex: /ida 07:30 3 101 Obs.de ida\n\t\t> Se não for informado o horário, serão listadas as caronas de IDA." +
                        "\n\t\t> Se não for informado o número de vagas, serão assumidas 4 vagas.\n\n",
    "volta_description": " {hh:mm} {0-4} {código bairro} {obs volta}: Adiciona uma carona de VOLTA, com o horário de <b>saída</b> do Fundão, " +
                        "o número de vagas, seguido do código do bairro (destino) e demais informações relevantes (opcional).\n " +
                       "Ex: /ida 07:30 3 101 Obs.de volta\n\t\t> Se não for informado o horário, serão listadas as caronas de VOLTA." +
                        "\n\t\t> Se não for informado o número de vagas, serão assumidas 4 vagas.\n\n",
    "remove_description": " {ida/volta}: Remove da lista a sua carona de IDA/VOLTA.\n\n",
    "vagas_description": " {ida/volta} {0-4}: Altera o número de vagas da sua carona de IDA/VOLTA.\n Ex: /vagas ida 3 ou /vagas volta 0.\n\n",
    "bairros_description": " : Lista todos os bairros e suas regiões.\n\n",
    "caronas_description": " : Lista todas as caronas ativas no momento, separadas por dia, IDA e VOLTA.\n\n"
}
