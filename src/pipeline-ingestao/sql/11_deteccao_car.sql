-- Pipeline — passo 3: detecção de sobreposição CAR x CAR sobre dados reais (PostGIS).
-- Tolerância: ignora divisas que apenas se tocam (interseção de área ~0) e pequenos
-- slivers de digitalização. Ajuste o limite conforme o "limite legal de tolerância".

\echo '== Pares CAR x CAR com sobreposição acima da tolerância (0,01 ha) =='
WITH pares AS (
  SELECT a.cod_imovel AS imovel_a,
         b.cod_imovel AS imovel_b,
         ST_Area(ST_Intersection(a.geom, b.geom)::geography) / 10000.0 AS sobrep_ha,
         LEAST(ST_Area(a.geom::geography), ST_Area(b.geom::geography)) / 10000.0 AS menor_ha
  FROM   imovel_car a
  JOIN   imovel_car b ON a.cod_imovel < b.cod_imovel
                      AND ST_Intersects(a.geom, b.geom)
)
SELECT imovel_a, imovel_b,
       round(sobrep_ha::numeric, 3)                              AS sobrep_ha,
       round((100 * sobrep_ha / NULLIF(menor_ha, 0))::numeric, 1) AS pct_do_menor
FROM   pares
WHERE  sobrep_ha > 0.01
ORDER  BY sobrep_ha DESC;

\echo '== Total de pares conflitantes (dimensiona o problema no município) =='
SELECT count(*) AS pares_conflito
FROM   imovel_car a
JOIN   imovel_car b ON a.cod_imovel < b.cod_imovel
                    AND ST_Intersects(a.geom, b.geom)
                    AND ST_Area(ST_Intersection(a.geom, b.geom)::geography) > 100;

\echo '== Exporta sobreposições para GeoJSON (camada do mapa Leaflet) =='
\copy (SELECT json_build_object('type','FeatureCollection','features',json_agg(f)) FROM ( \
  SELECT json_build_object('type','Feature','properties', json_build_object('imovel_a',a.cod_imovel,'imovel_b',b.cod_imovel,'sobrep_ha',round((ST_Area(ST_Intersection(a.geom,b.geom)::geography)/10000.0)::numeric,3)),'geometry',ST_AsGeoJSON(ST_Intersection(a.geom,b.geom))::json) AS f \
  FROM imovel_car a JOIN imovel_car b ON a.cod_imovel<b.cod_imovel AND ST_Intersects(a.geom,b.geom) \
  WHERE ST_Area(ST_Intersection(a.geom,b.geom)::geography) > 100 \
) sub) TO '/saida/sobreposicoes_reais.geojson'
