import telebot

def enviartip(tip):
    # Substitua "SEU_TOKEN_AQUI" pelo token do seu bot fornecido pelo BotFather no Telegram
    bot = telebot.TeleBot("6454882532:AAHL_YPOkMTpX7ys0623u2QdfI-a9CDB7tU")

    # Função que envia a mensagem
    def enviar_mensagem():
        chat_id = 809761831  # Substitua pelo chat_id do destinatário
        mensagem = tip
        bot.send_message(chat_id, mensagem)

    # Verifica se a variável é verdadeira e envia a mensagem
    if tip:
        enviar_mensagem()
    