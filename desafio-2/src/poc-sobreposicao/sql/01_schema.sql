-- PoC de detecção de sobreposição — esquema (PostGIS)
-- Desafio 2 / recorte R2. CRS oficial do CAR: SIRGAS 2000 (EPSG:4674).
CREATE EXTENSION IF NOT EXISTS postgis;

DROP TABLE IF EXISTS imovel_car;
CREATE TABLE imovel_car (
  cod_imovel  text PRIMARY KEY,          -- identificador do imóvel no SICAR
  nome        text,
  ind_status  text,                      -- AT (ativo), PE (pendente), CA (cancelado)
  geom        geometry(Polygon, 4674)
);

DROP TABLE IF EXISTS assentamento;
CREATE TABLE assentamento (
  codigo  text PRIMARY KEY,
  nome    text,
  fonte   text,                          -- ex.: INCRA
  geom    geometry(Polygon, 4674)
);

-- Índices espaciais: tornam a varredura da fila inteira viável em escala.
CREATE INDEX idx_imovel_geom        ON imovel_car  USING gist (geom);
CREATE INDEX idx_assentamento_geom  ON assentamento USING gist (geom);
