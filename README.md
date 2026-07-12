# Música — Iyari Gomez

Repositorio canónico del catálogo musical de **Iyari Gomez / BlackMamba RECORDS**.

## Estado del catálogo

| Fuente | Lanzamientos | Canciones |
|---|---:|---:|
| DistroKid | 230 | 274 |
| SoundCloud (perfil público) | — | 1,034 pistas |

## Motores

- `scripts/reconcile_catalogs.py`: cruza SoundCloud ↔ DistroKid.
- `scripts/audit_soundcloud_metadata.py`: detecta portadas y metadata faltante.
- `config/title_aliases.csv`: equivalencias confirmadas de títulos.
- `config/metadata_schema.csv`: contrato de metadata.
- `docs/RECONCILIATION.md`: reglas de reconciliación.
- `docs/METADATA_AUDIT.md`: reglas de auditoría y reparación.

## Ejecución

Guarda la exportación completa como `sources/soundcloud_tracks_public.json`:

```bash
python scripts/reconcile_catalogs.py
python scripts/audit_soundcloud_metadata.py
```

## Resultados

### Presencia por plataforma

- `reports/matched.csv`
- `reports/soundcloud_only.csv`
- `reports/distrokid_only.csv`
- `reports/needs_review.csv`
- `reports/summary.json`

### Portadas y metadata

- `reports/soundcloud_metadata_audit.csv`
- `reports/soundcloud_repair_queue.csv`
- `reports/soundcloud_metadata_summary.json`

La cola prioriza primero pistas sin portada y después registros con género, descripción, tags, BPM o tonalidad incompletos.

## Resumen DistroKid

- Lanzamientos: **230**
- Canciones: **274**
- Singles: **194**
- Lanzamientos con varias canciones: **36**

## Seguridad de edición

La detección es automática. Las modificaciones en SoundCloud requieren confirmar la pista exacta, la portada y la metadata propuesta antes de escribir externamente.

## Calidad

GitHub Actions ejecuta pruebas automáticas del reconciliador y del auditor en cada cambio relevante.
