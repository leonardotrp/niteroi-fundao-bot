from emoji import emojize

MSGS = {
    "list_error": "%s Ocorreu um erro ao buscar a lista. Tente novamente." % emojize(":warning:", use_aliases=True),
    "add_error": "%s Ocorreu um erro ao adicionar a carona. Tente novamente." % emojize(":warning:", use_aliases=True),
    "invalid_time_error": "Horário inválido! %s" % emojize(":flushed:", use_aliases=True),
    "ida_err": "Entrada inválida! %s (Ex: /ida 08:00 4 obs_ida ou /volta 17:00 3 obs_volta)" % emojize(":flushed:", use_aliases=True),
    "vagas_err": "Entrada inválida! %s O número de vagas deve ser 0, 1, 2, 3 ou 4. (Ex: /vagas ida 4 ou /vagas volta 0)" % emojize(":flushed:", use_aliases=True),
    "vagas_inexistentes": "%s Você precisa primeiro cadastrar uma carona de {0}." % emojize(":no_entry:", use_aliases=True),
    "username_error": "%s Crie um username nas configurações do seu Telegram para poder utilizar este Bot" % emojize(":no_entry:", use_aliases=True),
    "general_error": "%s Ocorreu um erro. Tente novamente." % emojize(":warning:", use_aliases=True),
    "start": "Olá, eu sou o FregolaeBot!\nO seu bot de caronas para a Ilha do Fundão",
    "caronas_header": "%s *CARONAS* %s" % (emojize(":blue_car:", use_aliases=True), emojize(":car:", use_aliases=True)),
    "ida_titulo": "\n------------------------\n%s *IDA*\n" % emojize(":arrow_heading_up:", use_aliases=True),
    "volta_titulo": "\n------------------------\n%s *VOLTA*\n" % emojize(":arrow_heading_down:", use_aliases=True),
    "removed": "Carona de {0} removida com sucesso! %s" % emojize(":wink:", use_aliases=True),
    "vaga_alterarda": "Sua carona de {0} agora possui {1} vagas %s" % emojize(":wink:", use_aliases=True),
    "remove_err": "Entrada inválida! %s (Ex: /remover volta ou /remover ida)" % emojize(":flushed:", use_aliases=True),
    "help_header": "%s Comandos do bot:\n\n" % emojize(":book:", use_aliases=True),
    "help_footer": "*OBS*:" +
                   "\n\t\t%s Para utilizar o bot, é *imprescindível* que você tenha seu @username, definido em configurações." % emojize(":bust_in_silhouette:", use_aliases=True) +
                   "\n\t\t%s As caronas desaparecem da lista 20 minutos após passar o horário definido na IDA/VOLTA." % emojize(":hourglass:", use_aliases=True) +
                   "\n\t\t%s Atenção motoristas! Ofereça suas caronas *somente* através dos comandos /ida e /volta." % emojize(":warning:", use_aliases=True),
    "feature_line": "*{0})* /{1}{2}",
    "sobre":
        "FregolaeBot:\n" +
        "\tAutores: @pedropauloskf e @almeidakayan\n" +
        "\tVersão adaptada por @leonardo_pereira para o grupo Niterói-Fundão.\n\n" +
        "\tCódigo fonte: https://github.com/leonardotrp/niteroi-fundao-bot",
    "ida_description": " [horario] [num.vagas] [notas]: Adiciona uma carona de IDA, com o horário de *chegada* no Fundão, " +
                        "o número de vagas (opcional) seguido de demais informações relevantes (opcional).\n " +
                       "Ex: /ida 07:30 3 Fonseca\n\t\t> Se não for informado o horário, serão listadas as caronas de IDA." +
                        "\n\t\t> Se não for informado o número de vagas, serão assumidas 4 vagas.\n\n",
    "volta_description": " [horario] [num.vagas] [notas]: Adiciona uma carona de VOLTA, com o horário de *saída* do Fundão, " +
                        " o número de vagas (opcional) seguido de demais informações relevantes (opcional).\n " +
                       "Ex: /volta 17:30 3 Fonseca\n\t\t> Se não for informado o horário, serão listadas as caronas de VOLTA." +
                        "\n\t\t> Se não for informado o número de vagas, serão assumidas 4 vagas.\n\n",
    "remove_description": " [ida/volta]: Remove da lista a sua carona de IDA/VOLTA.\n\n",
    "vagas_description": " [ida/volta] [num.vagas]: Altera o número de vagas da sua carona de IDA/VOLTA.\n Ex: /vagas ida 3 ou /vagas volta 0.\n\n",
    "caronas_description": " : Lista todas as caronas ativas no momento, separadas por dia, IDA e VOLTA.\n\n"
}
