# Música — Iyari Gomez

Repositorio canónico del catálogo musical de **Iyari Gomez / BlackMamba RECORDS**.

## Estado del catálogo

| Fuente | Lanzamientos | Canciones |
|---|---:|---:|
| DistroKid | 230 | 274 |
| SoundCloud (perfil público) | — | 1,034 pistas |

## Catálogo disponible

- `catalog/distrokid_catalog.csv`: una fila por canción.
- `catalog/distrokid_catalog.json`: estructura lanzamiento → canciones.
- `sources/distrokid_lyrics_export.txt`: fuente original del catálogo.
- `scripts/reconcile_catalogs.py`: motor de reconciliación SoundCloud ↔ DistroKid.
- `docs/RECONCILIATION.md`: contrato operativo y formatos.

## Reconciliación

El motor clasifica cada canción en:

1. presente en ambas plataformas;
2. exclusiva de SoundCloud;
3. distribuida por DistroKid pero ausente en SoundCloud;
4. coincidencia ambigua pendiente de revisión.

Usa aliases confirmados, normalización Unicode, títulos base y similitud difusa conservadora. Nunca fuerza coincidencias ambiguas.

### Ejecución

Guarda la exportación completa como `sources/soundcloud_tracks_public.json` y ejecuta:

```bash
python scripts/reconcile_catalogs.py
```

Resultados:

- `reports/matched.csv`
- `reports/soundcloud_only.csv`
- `reports/distrokid_only.csv`
- `reports/needs_review.csv`
- `reports/summary.json`

## Resumen DistroKid

- Lanzamientos: **230**
- Canciones: **274**
- Singles: **194**
- Lanzamientos con varias canciones: **36**

## Calidad

GitHub Actions ejecuta pruebas automáticas del normalizador y del clasificador en cada cambio relevante.
