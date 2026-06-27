-- PoC de detecção de sobreposição — consultas (PostGIS)
-- Área em hectares: cast para geography mede no elipsoide (m²) → /10000 = ha.
-- ST_Overlaps detecta sobreposição parcial; usamos ST_Intersects para conter
-- também casos de contenção total (um imóvel dentro de outro).

\echo '== (1) Imóvel CAR x Assentamento (INCRA) — o gargalo nomeado pelo estudo CPI/PUC-Rio =='
SELECT i.cod_imovel,
       i.nome                                                   AS imovel,
       a.nome                                                   AS assentamento,
       round((ST_Area(ST_Intersection(i.geom, a.geom)::geography) / 10000.0)::numeric, 2) AS sobrep_ha,
       round((ST_Area(ST_Intersection(i.geom, a.geom)) / ST_Area(i.geom) * 100)::numeric, 1) AS sobrep_pct
FROM   imovel_car i
JOIN   assentamento a ON ST_Intersects(i.geom, a.geom)
ORDER  BY sobrep_ha DESC;

\echo '== (2) Imóvel CAR x Imóvel CAR — conflito entre cadastros =='
SELECT a.cod_imovel AS imovel_a,
       b.cod_imovel AS imovel_b,
       round((ST_Area(ST_Intersection(a.geom, b.geom)::geography) / 10000.0)::numeric, 2) AS sobrep_ha
FROM   imovel_car a
JOIN   imovel_car b ON a.cod_imovel < b.cod_imovel        -- cada par uma vez, sem auto-join
                    AND ST_Intersects(a.geom, b.geom)
ORDER  BY sobrep_ha DESC;

\echo '== (3) Fila priorizada — flags de sobreposição por imóvel (alimenta o painel R1) =='
SELECT i.cod_imovel,
       i.nome,
       EXISTS (SELECT 1 FROM assentamento a
                WHERE ST_Intersects(i.geom, a.geom))                       AS sobrep_assentamento,
       EXISTS (SELECT 1 FROM imovel_car j
                WHERE j.cod_imovel <> i.cod_imovel
                  AND ST_Intersects(i.geom, j.geom))                       AS sobrep_car,
       round((COALESCE((SELECT SUM(ST_Area(ST_Intersection(i.geom, a.geom)::geography))
                         FROM assentamento a WHERE ST_Intersects(i.geom, a.geom)), 0)
              / 10000.0)::numeric, 2)                                      AS sobrep_assent_ha
FROM   imovel_car i
ORDER  BY sobrep_assent_ha DESC, sobrep_car DESC;

\echo '== (4) Camada de sobreposições em GeoJSON (para o mapa Leaflet do painel) =='
-- Exporta a geometria das interseções (reprojetada para 4674) como FeatureCollection.
\copy (SELECT json_build_object('type','FeatureCollection','features', json_agg(f)) FROM ( \
  SELECT json_build_object('type','Feature','properties', json_build_object('imovel', i.cod_imovel, 'contra', a.nome, 'tipo','assentamento','sobrep_ha', round((ST_Area(ST_Intersection(i.geom,a.geom)::geography)/10000.0)::numeric,2)), 'geometry', ST_AsGeoJSON(ST_Intersection(i.geom,a.geom))::json) AS f \
  FROM imovel_car i JOIN assentamento a ON ST_Intersects(i.geom,a.geom) \
) sub) TO '/saida/sobreposicoes.geojson'
