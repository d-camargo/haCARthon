"""Terra em Dia — bot de Telegram (protótipo do Desafio 3 do haCARthon).

Conversa: o produtor manda o número do CAR; o bot mostra o mapa do imóvel,
pergunta se ele sabe por que recebeu a carta, explica a mata ciliar em balões
curtos, manda um 2º mapa de "como deve ficar", sugere o caminho da Reserva
Legal, mede a compreensão e o guia até o SICAR.

Rodar:
    pip install -r requirements.txt          (venv com --system-site-packages p/ osgeo)
    cp .env.example .env                      (TELEGRAM_TOKEN, OPENAI_API_KEY, TERRA_DEMO_COD)
    python bot.py
"""
import logging
import os
import tempfile

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

import analise
import cadastro
import conteudo
import llm
import mapa
import metricas

try:
    from dotenv import load_dotenv

    load_dotenv()
except ImportError:
    pass

logging.basicConfig(
    format="%(asctime)s %(name)s %(levelname)s %(message)s", level=logging.INFO
)
logger = logging.getLogger("terra-em-dia")

AGUARDA_CAR, AGUARDA_MOTIVO, AGUARDA_COMPREENSAO, CONVERSA = range(4)
MD = "Markdown"
DEMO_COD = os.environ.get("TERRA_DEMO_COD")


def _resolver(texto: str):
    cod = (texto or "").strip()
    im = cadastro.carregar_imovel(cod) if len(cod) >= 5 else None
    if im:
        return im
    if DEMO_COD:
        return cadastro.carregar_imovel(DEMO_COD)
    return None


async def _enviar_mapa(update, imovel, modo, caption):
    await update.message.chat.send_action(ChatAction.UPLOAD_PHOTO)
    tmp_nome = None
    try:
        with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as tmp:
            tmp_nome = tmp.name
        mapa.gerar_mapa(imovel, tmp_nome, modo=modo)
        with open(tmp_nome, "rb") as fp:
            await update.message.reply_photo(photo=fp, caption=caption)
    except Exception as e:  # mapa é um plus; não derruba a conversa
        logger.warning("falha ao gerar mapa (%s): %s", modo, e)
    finally:
        if tmp_nome:
            try:
                os.unlink(tmp_nome)
            except OSError:
                pass


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    context.user_data.clear()
    await update.message.reply_text(conteudo.SAUDACAO, parse_mode=MD)
    return AGUARDA_CAR


async def recebeu_foto(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    await update.message.reply_text(conteudo.RECEBI_FOTO)
    return await _apresentar(update, context, _resolver(DEMO_COD or ""))


async def recebeu_car(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    return await _apresentar(update, context, _resolver(update.message.text))


async def _apresentar(update, context, imovel) -> int:
    if not imovel:
        await update.message.reply_text(conteudo.NAO_ACHEI, parse_mode=MD)
        return AGUARDA_CAR

    an = analise.analisar(imovel)
    context.user_data.update(imovel=imovel, an=an, historico=[], tentativas=0)

    await update.message.reply_text(conteudo.VENDO_CADASTRO)
    await _enviar_mapa(update, imovel, "atual", conteudo.CAPTION_ATUAL)
    await update.message.reply_text(conteudo.intro_sitio(an), parse_mode=MD)
    await update.message.reply_text(conteudo.PERGUNTA_MOTIVO, parse_mode=MD)
    return AGUARDA_MOTIVO


async def apos_motivo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    imovel = context.user_data.get("imovel")
    an = context.user_data.get("an", {})
    await update.message.reply_text(conteudo.reage_motivo(update.message.text))
    await update.message.reply_text(conteudo.explica_mata(an), parse_mode=MD)
    await _enviar_mapa(update, imovel, "meta", conteudo.CAPTION_META)
    sugestao = conteudo.sugestao_rl(an)
    if sugestao:
        await update.message.reply_text(sugestao, parse_mode=MD)
    await update.message.reply_text(conteudo.PERGUNTA_COMPREENSAO, parse_mode=MD)
    return AGUARDA_COMPREENSAO


async def avalia_compreensao(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    an = context.user_data.get("an", {})
    entendeu = conteudo.compreendeu(update.message.text)
    tentativas = context.user_data.get("tentativas", 0) + 1
    context.user_data["tentativas"] = tentativas

    if not entendeu and tentativas == 1:
        metricas.registrar(update.effective_user.id, False, tentativas)
        await update.message.reply_text(conteudo.REEXPLICA, parse_mode=MD)
        return AGUARDA_COMPREENSAO

    if entendeu:
        metricas.registrar(update.effective_user.id, True, tentativas)
        await update.message.reply_text(conteudo.ELOGIO_ENTENDEU, parse_mode=MD)

    await update.message.reply_text(conteudo.guia_acao(an), parse_mode=MD)
    await update.message.reply_text(conteudo.FECHO, parse_mode=MD)
    return CONVERSA


async def conversa_livre(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    an = context.user_data.get("an", {})
    hist = context.user_data.setdefault("historico", [])
    hist.append({"role": "user", "content": update.message.text})
    await update.message.chat.send_action(ChatAction.TYPING)
    resp = llm.conversar(hist, an) or (
        "Boa pergunta! Pra essa eu prefiro te orientar com calma — chama a Casa "
        "da Agricultura ou um técnico de confiança que eu te ajudo a entender. 🌱"
    )
    hist.append({"role": "assistant", "content": resp})
    await update.message.reply_text(resp, parse_mode=MD)
    return CONVERSA


async def metricas_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    r = metricas.resumo()
    await update.message.reply_text(
        f"📊 *Terra em Dia* — eficácia\nConversas: {r['total']}\n"
        f"Entenderam: {r['entenderam']}\n*Compreensão: {r['pct']}%*",
        parse_mode=MD,
    )


async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    context.user_data.clear()
    await update.message.reply_text("Beleza! Qualquer coisa é só mandar /start. 🌱")
    return ConversationHandler.END


def main() -> None:
    token = os.environ.get("TELEGRAM_TOKEN")
    if not token:
        raise SystemExit("Defina TELEGRAM_TOKEN (token do @BotFather) no .env ou no ambiente.")

    app = Application.builder().token(token).build()
    texto = filters.TEXT & ~filters.COMMAND

    conversa = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            AGUARDA_CAR: [MessageHandler(filters.PHOTO, recebeu_foto),
                          MessageHandler(texto, recebeu_car)],
            AGUARDA_MOTIVO: [MessageHandler(texto, apos_motivo)],
            AGUARDA_COMPREENSAO: [MessageHandler(texto, avalia_compreensao)],
            CONVERSA: [MessageHandler(texto, conversa_livre)],
        },
        fallbacks=[CommandHandler("cancel", cancel), CommandHandler("start", start)],
    )
    app.add_handler(conversa)
    app.add_handler(CommandHandler("metricas", metricas_cmd))

    logger.info("Terra em Dia no ar (LLM: %s). Ctrl+C para parar.",
                "on" if llm.tem_llm() else "off (roteiro)")
    app.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
