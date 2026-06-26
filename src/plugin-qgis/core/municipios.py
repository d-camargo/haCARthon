# -*- coding: utf-8 -*-
"""
Resolução do nome de município para a grafia oficial (IBGE), casando sem acento/caixa.

O filtro do SICAR é no servidor (match exato, sensível a acento e maiúscula), então
"querencia do norte" ou "MARINGA" não retornam nada. Aqui resolvemos a grafia canônica
("Querência do Norte", "Maringá") antes de montar a consulta.
"""
from qgis.core import QgsBlockingNetworkRequest
from qgis.PyQt.QtCore import QUrl
from qgis.PyQt.QtNetwork import QNetworkRequest
import json
import unicodedata

_CACHE = {}
_IBGE = "https://servicodados.ibge.gov.br/api/v1/localidades/estados/{uf}/municipios"


def normalizar(s):
    return unicodedata.normalize('NFKD', s or '').encode('ascii', 'ignore').decode('ascii').strip().upper()


def _municipios_uf(uf):
    uf = uf.upper()
    if uf in _CACHE:
        return _CACHE[uf]
    nomes = []
    try:
        req = QNetworkRequest(QUrl(_IBGE.format(uf=uf)))
        req.setRawHeader(b"User-Agent", b"PreValCAR-QGIS/0.1")
        blocking = QgsBlockingNetworkRequest()
        blocking.get(req, True)
        data = bytes(blocking.reply().content())
        if data:
            nomes = [m['nome'] for m in json.loads(data)]
    except Exception:
        nomes = []
    _CACHE[uf] = nomes
    return nomes


def resolver_municipio(uf, municipio):
    """
    Retorna (nome_canonico, status):
      - (nome, 'ok')         -> casou com a grafia oficial do IBGE
      - (municipio, 'sem_ibge') -> IBGE indisponível; usa o que foi digitado
      - (None, 'nao_existe') -> IBGE ok, mas não existe esse município na UF
    """
    nomes = _municipios_uf(uf)
    if not nomes:
        return municipio, 'sem_ibge'
    alvo = normalizar(municipio)
    for nome in nomes:
        if normalizar(nome) == alvo:
            return nome, 'ok'
    return None, 'nao_existe'
