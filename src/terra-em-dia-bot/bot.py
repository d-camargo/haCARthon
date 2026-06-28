"""Terra em Dia — bot de Telegram (protótipo do Desafio 3 do haCARthon).

Conversa: o produtor manda o número do CAR; o bot guarda o atendimento, mostra
o mapa do imóvel e responde em mensagens curtas ao que ele perguntar sobre mata
ciliar, Reserva Legal e próximos passos no SICAR.

Rodar:
    pip install -r requirements.txt          (venv com --system-site-packages p/ osgeo)
    cp .env.example .env                      (TELEGRAM_TOKEN, OPENAI_API_KEY, TERRA_DEMO_COD)
    python bot.py
"""
import logging
import os
import tempfile

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.constants import ChatAction
from telegram.ext import (
    Application,
    CallbackQueryHandler,
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
import memoria
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

AGUARDA_CAR, CONVERSA = range(2)
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


def _user_id(update: Update) -> int:
    return update.effective_user.id


def _restaurar_contexto(update: Update, context: ContextTypes.DEFAULT_TYPE) -> bool:
    mem = memoria.carregar(_user_id(update))
    cod = mem.get("cod")
    if not cod:
        return False
    imovel = cadastro.carregar_imovel(cod)
    if not imovel:
        return False
    an = analise.analisar(imovel)
    context.user_data.update(
        imovel=imovel,
        an=an,
        historico=mem.get("historico", []),
        tentativas=mem.get("tentativas", 0),
    )
    return True


async def _enviar_mapa(update, context, imovel, modo, caption):
    chat = update.effective_chat
    if not chat:
        return
    await chat.send_action(ChatAction.UPLOAD_PHOTO)
    tmp_nome = None
    try:
        with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as tmp:
            tmp_nome = tmp.name
        if modo == "comparativo":
            ret = mapa.gerar_comparativo(imovel, tmp_nome, feicao="app")
            if ret is None:
                await context.bot.send_message(
                    chat_id=chat.id,
                    text="Não foi possível gerar o comparativo porque sua propriedade não possui mata ciliar mapeada localmente."
                )
                return
        else:
            mapa.gerar_mapa(imovel, tmp_nome, modo=modo)
        with open(tmp_nome, "rb") as fp:
            await context.bot.send_photo(chat_id=chat.id, photo=fp, caption=caption)
        context.user_data["ultimo_mapa"] = modo
    except Exception as e:  # mapa é um plus; não derruba a conversa
        logger.warning("falha ao gerar mapa (%s): %s", modo, e)
    finally:
        if tmp_nome:
            try:
                os.unlink(tmp_nome)
            except OSError:
                pass


def _teclado_solucao() -> InlineKeyboardMarkup:
    keyboard = [
        [InlineKeyboardButton("🌳 Ver como fica em dia", callback_data="sol")],
        [InlineKeyboardButton("🔍 Comparar agora × depois", callback_data="cmp")],
        [InlineKeyboardButton("📋 Passos no SICAR", callback_data="sicar")],
        [InlineKeyboardButton("❓ Responder 2 perguntas rápidas", callback_data="quiz:0")],
    ]
    return InlineKeyboardMarkup(keyboard)


def _teclado_pergunta(idx: int) -> InlineKeyboardMarkup:
    p = conteudo.PERGUNTAS[idx]
    keyboard = [
        [InlineKeyboardButton(txt, callback_data=f"resp:{idx}:{i}")]
        for i, (txt, _ok) in enumerate(p["opcoes"])
    ]
    return InlineKeyboardMarkup(keyboard)


async def _enviar_pergunta(context: ContextTypes.DEFAULT_TYPE, chat_id: int, idx: int) -> None:
    p = conteudo.PERGUNTAS[idx]
    await context.bot.send_message(
        chat_id=chat_id, text=p["texto"], parse_mode=MD,
        reply_markup=_teclado_pergunta(idx),
    )


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    context.user_data.clear()
    if _restaurar_contexto(update, context):
        await update.message.reply_text(conteudo.RETOMADA, parse_mode=MD)
        return CONVERSA
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
    memoria.atualizar(_user_id(update), cod=imovel["cod"], tentativas=0, historico=[])

    await update.message.reply_text(conteudo.VENDO_CADASTRO)
    await _enviar_mapa(update, context, imovel, "atual", conteudo.CAPTION_ATUAL)
    await update.message.reply_text(conteudo.resumo_imovel(an), parse_mode=MD)

    if an.get("tem_app") or an.get("tem_rl"):
        await update.message.reply_text(
            "Posso te mostrar como sua terra fica em dia 👇",
            reply_markup=_teclado_solucao()
        )
    return CONVERSA


async def mapa_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if "imovel" not in context.user_data and not _restaurar_contexto(update, context):
        await update.message.reply_text("Por favor, me mande primeiro o número do seu CAR ou a foto da carta.")
        return
    imovel = context.user_data["imovel"]
    await _enviar_mapa(update, context, imovel, "atual", conteudo.CAPTION_ATUAL)


async def comofica_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if "imovel" not in context.user_data and not _restaurar_contexto(update, context):
        await update.message.reply_text("Por favor, me mande primeiro o número do seu CAR ou a foto da carta.")
        return
    imovel = context.user_data["imovel"]
    await _enviar_mapa(update, context, imovel, "meta", conteudo.CAPTION_META)


async def botao(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()

    if "imovel" not in context.user_data and not _restaurar_contexto(update, context):
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text="Por favor, me mande primeiro o número do seu CAR ou a foto da carta."
        )
        return

    imovel = context.user_data["imovel"]
    an = context.user_data["an"]

    data = query.data

    # Perguntas de checagem: "quiz:<idx>" inicia; "resp:<idx>:<opcao>" responde.
    if data.startswith("quiz:"):
        idx = int(data.split(":")[1])
        await _enviar_pergunta(context, update.effective_chat.id, idx)
        return
    if data.startswith("resp:"):
        _, sidx, sopt = data.split(":")
        idx, opt = int(sidx), int(sopt)
        p = conteudo.PERGUNTAS[idx]
        _texto, acertou = p["opcoes"][opt]
        tentativas = context.user_data.get("tentativas", 0) + 1
        context.user_data["tentativas"] = tentativas
        memoria.atualizar(_user_id(update), tentativas=tentativas)
        metricas.registrar(_user_id(update), acertou, tentativas)
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=p["certo"] if acertou else p["errado"],
            parse_mode=MD,
        )
        if idx + 1 < len(conteudo.PERGUNTAS):
            await _enviar_pergunta(context, update.effective_chat.id, idx + 1)
        return

    if data == "sol":
        await _enviar_mapa(update, context, imovel, "meta", conteudo.CAPTION_META)
        keyboard = [[InlineKeyboardButton("🔍 Comparar agora × depois", callback_data="cmp")]]
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text="Quer ver a diferença aproximando na sua mata e reserva? 👇",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )
    elif data == "cmp":
        await _enviar_mapa(update, context, imovel, "comparativo", conteudo.CAPTION_COMPARATIVO)
        if an.get("tem_rl") and an.get("rl_deficit_ha", 0) > 0:
            await context.bot.send_message(
                chat_id=update.effective_chat.id,
                text=(
                    f"E sobre a Reserva Legal: na sua terra ainda faltam cerca de *{an['rl_deficit_ha']} ha* "
                    "de mato a compensar ou recompor. Não desenhamos a Reserva no mapa acima porque não há "
                    "uma área demarcada ainda, mas esse ajuste é feito na regularização."
                ),
                parse_mode=MD
            )
    elif data == "sicar":
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=conteudo.guia_acao(an),
            parse_mode=MD
        )


async def conversa_livre(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    if "an" not in context.user_data and not _restaurar_contexto(update, context):
        imovel = _resolver(update.message.text)
        if imovel:
            return await _apresentar(update, context, imovel)
        await update.message.reply_text(conteudo.SAUDACAO, parse_mode=MD)
        return AGUARDA_CAR

    an = context.user_data.get("an", {})
    texto = update.message.text
    hist = memoria.adicionar_mensagem(_user_id(update), "user", texto)
    context.user_data["historico"] = hist
    await update.message.chat.send_action(ChatAction.TYPING)
    resp = llm.conversar(hist, an) or conteudo.resposta_curta(texto, an)

    enviar_meta = conteudo.pediu_meta(texto)
    enviar_atual = conteudo.pediu_mapa(texto)

    # Envio automático do mapa meta quando explica a mata ciliar
    if any(p in conteudo._normaliza(texto) for p in ["mata", "ciliar", "app", "rio", "beira"]):
        if context.user_data.get("ultimo_mapa") != "meta":
            enviar_meta = True

    if enviar_meta:
        await _enviar_mapa(update, context, context.user_data.get("imovel"), "meta", conteudo.CAPTION_META)
    elif enviar_atual:
        await _enviar_mapa(update, context, context.user_data.get("imovel"), "atual", conteudo.CAPTION_ATUAL)

    if conteudo.compreendeu(texto):
        tentativas = context.user_data.get("tentativas", 0) + 1
        context.user_data["tentativas"] = tentativas
        memoria.atualizar(_user_id(update), tentativas=tentativas)
        metricas.registrar(_user_id(update), True, tentativas)

    hist = memoria.adicionar_mensagem(_user_id(update), "assistant", resp)
    context.user_data["historico"] = hist
    await update.message.reply_text(resp, parse_mode=MD)
    return CONVERSA


async def pergunta_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if "imovel" not in context.user_data and not _restaurar_contexto(update, context):
        await update.message.reply_text("Por favor, me mande primeiro o número do seu CAR ou a foto da carta.")
        return
    await _enviar_pergunta(context, update.effective_chat.id, 0)


async def metricas_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    r = metricas.resumo()
    await update.message.reply_text(
        f"📊 *Terra em Dia* — eficácia\nConversas: {r['total']}\n"
        f"Entenderam: {r['entenderam']}\n*Compreensão: {r['pct']}%*",
        parse_mode=MD,
    )


async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    context.user_data.clear()
    memoria.limpar(_user_id(update))
    await update.message.reply_text("Apaguei o atendimento deste chat.")
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
            CONVERSA: [
                CommandHandler("mapa", mapa_cmd),
                CommandHandler("comofica", comofica_cmd),
                CommandHandler("mapadepois", comofica_cmd),
                CommandHandler("pergunta", pergunta_cmd),
                MessageHandler(texto, conversa_livre)
            ],
        },
        fallbacks=[CommandHandler("cancel", cancel), CommandHandler("start", start)],
    )
    app.add_handler(conversa)
    app.add_handler(CommandHandler("metricas", metricas_cmd))
    app.add_handler(CommandHandler("pergunta", pergunta_cmd))
    app.add_handler(CommandHandler("mapa", mapa_cmd))
    app.add_handler(CommandHandler("comofica", comofica_cmd))
    app.add_handler(CommandHandler("mapadepois", comofica_cmd))
    app.add_handler(CallbackQueryHandler(botao))
    app.add_handler(MessageHandler(filters.PHOTO, recebeu_foto))
    app.add_handler(MessageHandler(texto, conversa_livre))

    logger.info("Terra em Dia no ar (LLM: %s). Ctrl+C para parar.",
                "on" if llm.tem_llm() else "off (roteiro)")
    app.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
