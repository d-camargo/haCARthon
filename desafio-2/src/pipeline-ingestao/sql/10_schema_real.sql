-- Pipeline — passo 2b: saneamento pós-carga (PostGIS).
-- A tabela `imovel_car` é criada pelo ogr2ogr a partir do GeoJSON do SICAR
-- (ver carregar.sh). Aqui garantimos geometria válida e índice espacial.
CREATE EXTENSION IF NOT EXISTS postgis;

-- Dados reais do SICAR às vezes têm geometrias inválidas (auto-interseção etc.).
UPDATE imovel_car SET geom = ST_MakeValid(geom) WHERE NOT ST_IsValid(geom);

-- Índice espacial: indispensável para varrer a base inteira em tempo viável.
CREATE INDEX IF NOT EXISTS idx_imovel_car_geom ON imovel_car USING gist (geom);
ANALYZE imovel_car;
