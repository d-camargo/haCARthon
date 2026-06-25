-- Pipeline — detecção CAR x Assentamento (INCRA) sobre dados reais (PostGIS).
-- Pré-requisito: tabelas `imovel_car` e `assentamento` carregadas via ogr2ogr
-- (ver carregar.sh) e saneadas (10_schema_real.sql aplica ST_MakeValid/índice).
-- Garante geometria/índice também para a tabela de assentamentos:
UPDATE assentamento SET geom = ST_MakeValid(geom) WHERE NOT ST_IsValid(geom);
CREATE INDEX IF NOT EXISTS idx_assentamento_geom ON assentamento USING gist (geom);
ANALYZE assentamento;

\echo '== Imóveis CAR que sobrepõem assentamento (gargalo nº 1 do estudo CPI/PUC-Rio) =='
SELECT i.cod_imovel,
       a.nome                                                                AS assentamento,
       round((ST_Area(ST_Intersection(i.geom, a.geom)::geography) / 10000.0)::numeric, 3) AS sobrep_ha,
       round((100 * ST_Area(ST_Intersection(i.geom, a.geom)) / ST_Area(i.geom))::numeric, 1) AS pct_imovel
FROM   imovel_car i
JOIN   assentamento a ON ST_Intersects(i.geom, a.geom)
WHERE  ST_Area(ST_Intersection(i.geom, a.geom)::geography) > 100   -- tolerância
ORDER  BY sobrep_ha DESC;

\echo '== Quantos imóveis em conflito com assentamento (dimensiona o problema) =='
SELECT count(DISTINCT i.cod_imovel) AS imoveis_em_conflito
FROM   imovel_car i
JOIN   assentamento a ON ST_Intersects(i.geom, a.geom)
                      AND ST_Area(ST_Intersection(i.geom, a.geom)::geography) > 100;

\echo '== Exporta sobreposições CAR x assentamento para GeoJSON (camada do mapa) =='
\copy (SELECT json_build_object('type','FeatureCollection','features',json_agg(f)) FROM ( \
  SELECT json_build_object('type','Feature','properties', json_build_object('imovel',i.cod_imovel,'assentamento',a.nome,'tipo','assentamento','sobrep_ha',round((ST_Area(ST_Intersection(i.geom,a.geom)::geography)/10000.0)::numeric,3)),'geometry',ST_AsGeoJSON(ST_Intersection(i.geom,a.geom))::json) AS f \
  FROM imovel_car i JOIN assentamento a ON ST_Intersects(i.geom,a.geom) \
  WHERE ST_Area(ST_Intersection(i.geom,a.geom)::geography) > 100 \
) sub) TO '/saida/sobreposicoes_assentamento.geojson'
