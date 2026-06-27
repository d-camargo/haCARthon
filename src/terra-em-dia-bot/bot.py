"""Terra em Dia — bot de Telegram (protótipo do Desafio 3 do haCARthon).

Fluxo: o produtor chama no "Zap", manda o número do CAR (ou foto da carta),
o bot explica a obrigação ambiental do imóvel dele em linguagem simples,
faz uma pergunta despretensiosa pra ver se entendeu (vira métrica) e o guia
até o botão do SICAR.

Rodar:
    pip install -r requirements.txt
    export TELEGRAM_TOKEN=...    # token do @BotFather (ou use um .env)
    python bot.py
"""
import logging
import os

from telegram import Update
from telegram.constants import ChatAction
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
    ConversationHandler,
    MessageHandler,
    filters,
)

import conteudo
import imoveis
import metricas

try:  # carrega .env se houver (opcional)
    from dotenv import load_dotenv

    load_dotenv()
except ImportError:
    pass

logging.basicConfig(
    format="%(asctime)s %(name)s %(levelname)s %(message)s", level=logging.INFO
)
logger = logging.getLogger("terra-em-dia")

AGUARDA_CAR, AGUARDA_COMPREENSAO = range(2)
MD = "Markdown"


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    context.user_data.clear()
    await update.message.reply_text(conteudo.SAUDACAO, parse_mode=MD)
    return AGUARDA_CAR


async def recebeu_foto(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    await update.message.reply_text(conteudo.RECEBI_FOTO)
    return await _explica_imovel(update, context, texto="foto-da-carta")


async def recebeu_car(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    return await _explica_imovel(update, context, texto=update.message.text)


async def _explica_imovel(update, context, texto: str) -> int:
    imovel = imoveis.buscar_imovel(texto)
    if not imovel:
        await update.message.reply_text(conteudo.NAO_ACHEI, parse_mode=MD)
        return AGUARDA_CAR

    context.user_data["imovel"] = imovel
    await update.message.chat.send_action(ChatAction.TYPING)
    await update.message.reply_text(conteudo.explicacao_app(imovel), parse_mode=MD)
    await update.message.reply_text(conteudo.PERGUNTA_COMPREENSAO, parse_mode=MD)
    return AGUARDA_COMPREENSAO


async def avalia_compreensao(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    imovel = context.user_data.get("imovel", imoveis.IMOVEL_EXEMPLO)
    entendeu = conteudo.compreendeu(update.message.text)
    tentativas = context.user_data.get("tentativas", 0) + 1
    context.user_data["tentativas"] = tentativas

    if entendeu:
        metricas.registrar(update.effective_user.id, True, tentativas)
        await update.message.reply_text(conteudo.ELOGIO_ENTENDEU, parse_mode=MD)
        await update.message.reply_text(conteudo.guia_acao(imovel), parse_mode=MD)
        await update.message.reply_text(conteudo.FECHO, parse_mode=MD)
        return ConversationHandler.END

    if tentativas == 1:
        # Não entendeu na primeira: registra e reexplica uma vez.
        metricas.registrar(update.effective_user.id, False, tentativas)
        await update.message.reply_text(conteudo.REEXPLICA, parse_mode=MD)
        return AGUARDA_COMPREENSAO

    # Reexplicado: segue para a ação mesmo assim.
    await update.message.reply_text(conteudo.guia_acao(imovel), parse_mode=MD)
    await update.message.reply_text(conteudo.FECHO, parse_mode=MD)
    return ConversationHandler.END


async def metricas_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    r = metricas.resumo()
    await update.message.reply_text(
        f"📊 *Terra em Dia* — eficácia\n"
        f"Conversas: {r['total']}\n"
        f"Entenderam: {r['entenderam']}\n"
        f"*Compreensão: {r['pct']}%*",
        parse_mode=MD,
    )


async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    context.user_data.clear()
    await update.message.reply_text("Beleza, qualquer coisa é só mandar /start. 🌱")
    return ConversationHandler.END


def main() -> None:
    token = os.environ.get("TELEGRAM_TOKEN")
    if not token:
        raise SystemExit(
            "Defina TELEGRAM_TOKEN (token do @BotFather) no ambiente ou no .env"
        )

    app = Application.builder().token(token).build()

    conversa = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            AGUARDA_CAR: [
                MessageHandler(filters.PHOTO, recebeu_foto),
                MessageHandler(filters.TEXT & ~filters.COMMAND, recebeu_car),
            ],
            AGUARDA_COMPREENSAO: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, avalia_compreensao),
            ],
        },
        fallbacks=[CommandHandler("cancel", cancel)],
    )

    app.add_handler(conversa)
    app.add_handler(CommandHandler("metricas", metricas_cmd))

    logger.info("Terra em Dia no ar. Ctrl+C para parar.")
    app.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
