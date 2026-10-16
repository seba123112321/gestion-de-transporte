USE gestion_transporte;

INSERT INTO transport_app_ruta (
    nombre,
    origen,
    destino,
    distancia_km,
    activa,
    creado_en,
    actualizado_en
)
SELECT
    'Santiago - Valparaiso',
    'Santiago',
    'Valparaiso',
    116.00,
    TRUE,
    NOW(),
    NOW()
WHERE NOT EXISTS (
    SELECT 1
    FROM transport_app_ruta
    WHERE nombre = 'Santiago - Valparaiso'
      AND origen = 'Santiago'
      AND destino = 'Valparaiso'
);
