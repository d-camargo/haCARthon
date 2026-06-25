-- PoC de detecção de sobreposição — carga de dados sintéticos (PostGIS)
-- Dados FICTÍCIOS para demonstração. Geometrias em EPSG:4674 (SIRGAS 2000).
-- Em produção, substituir por carga das bases reais do SICAR via ogr2ogr (ver README).

TRUNCATE imovel_car;
INSERT INTO imovel_car (cod_imovel, nome, ind_status, geom) VALUES
  ('PR-4110904-MV4', 'Fazenda Milho Verde IV', 'AT',
   ST_GeomFromText('POLYGON((-51.940 -22.620,-51.920 -22.620,-51.920 -22.640,-51.940 -22.640,-51.940 -22.620))', 4674)),
  ('PR-4128203-SBE', 'Sítio Boa Esperança', 'AT',
   ST_GeomFromText('POLYGON((-51.935 -22.632,-51.926 -22.632,-51.926 -22.648,-51.935 -22.648,-51.935 -22.632))', 4674)),
  ('PR-4119608-SF', 'Fazenda Santa Fé', 'AT',
   ST_GeomFromText('POLYGON((-51.975 -22.620,-51.955 -22.620,-51.955 -22.640,-51.975 -22.640,-51.975 -22.620))', 4674));

TRUNCATE assentamento;
INSERT INTO assentamento (codigo, nome, fonte, geom) VALUES
  ('PA-BV-001', 'PA Boa Vista', 'INCRA',
   ST_GeomFromText('POLYGON((-51.925 -22.615,-51.905 -22.615,-51.905 -22.635,-51.925 -22.635,-51.925 -22.615))', 4674));
