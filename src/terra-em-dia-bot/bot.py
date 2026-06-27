"""Terra em Dia — bot de Telegram (protótipo do Desafio 3 do haCARthon).

O produtor chama no "Zap", manda o número do CAR; o bot consulta os dados reais
do imóvel, **manda um mapa com as feições** (perímetro, mata ciliar, Reserva
Legal), **explica em linguagem simples** (LLM, com fallback roteirizado), faz
uma **pergunta despretensiosa** pra medir compreensão e o **guia até o SICAR**.

Rodar:
    pip install -r requirements.txt
    cp .env.example .env        # preencha TELEGRAM_TOKEN e (opcional) OPENAI_API_KEY
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

AGUARDA_CAR, AGUARDA_COMPREENSAO, CONVERSA = range(3)
MD = "Markdown"
DEMO_COD = os.environ.get("TERRA_DEMO_COD")  # cod_imovel de demonstração (.env)


def _resolver(texto: str):
    """Retorna (cod, imovel). Usa o cod digitado se existir; senão o de demo."""
    cod = (texto or "").strip()
    im = cadastro.carregar_imovel(cod) if len(cod) >= 5 else None
    if im:
        return cod, im
    if DEMO_COD:
        return DEMO_COD, cadastro.carregar_imovel(DEMO_COD)
    return cod, None


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    context.user_data.clear()
    await update.message.reply_text(conteudo.SAUDACAO, parse_mode=MD)
    return AGUARDA_CAR


async def recebeu_foto(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    await update.message.reply_text(conteudo.RECEBI_FOTO)
    _, im = _resolver(DEMO_COD or "")
    return await _apresentar(update, context, im)


async def recebeu_car(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    _, im = _resolver(update.message.text)
    return await _apresentar(update, context, im)


async def _apresentar(update, context, imovel) -> int:
    if not imovel:
        await update.message.reply_text(conteudo.NAO_ACHEI, parse_mode=MD)
        return AGUARDA_CAR

    an = analise.analisar(imovel)
    context.user_data["an"] = an
    context.user_data["historico"] = []
    context.user_data["tentativas"] = 0

    await update.message.reply_text(conteudo.VENDO_CADASTRO)
    await update.message.chat.send_action(ChatAction.UPLOAD_PHOTO)
    try:
        with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as tmp:
            mapa.gerar_mapa(imovel, tmp.name)
        with open(tmp.name, "rb") as fp:
            await update.message.reply_photo(photo=fp, caption="📍 O seu sítio no mapa")
    except Exception as e:  # mapa é um plus; não derruba a conversa
        logger.warning("falha ao gerar mapa: %s", e)
    finally:
        if "tmp" in dir():
            try:
                os.unlink(tmp.name)
            except OSError:
                pass

    await update.message.chat.send_action(ChatAction.TYPING)
    explicacao = llm.explicar(an) or conteudo.explicacao(an)
    await update.message.reply_text(explicacao, parse_mode=MD)
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
    resp = llm.conversar(hist, an)
    if not resp:
        resp = (
            "Boa pergunta! Pra essa eu prefiro te orientar com calma — chama a "
            "Casa da Agricultura ou um técnico de confiança, e me diga que eu te "
            "ajudo a entender. 🌱"
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
