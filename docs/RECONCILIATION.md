# Reconciliación SoundCloud ↔ DistroKid

## Clasificaciones

- `matched.csv`: presente en ambas plataformas.
- `soundcloud_only.csv`: publicada en SoundCloud pero no encontrada en DistroKid.
- `distrokid_only.csv`: distribuida por DistroKid pero no encontrada en SoundCloud.
- `needs_review.csv`: coincidencias ambiguas que requieren decisión humana.
- `summary.json`: conteos y tasa de coincidencia.

## Entrada SoundCloud

Guarda la exportación pública completa como:

`sources/soundcloud_tracks_public.json`

Formatos aceptados:

- arreglo JSON de pistas;
- objeto con `tracks`, `collection` o `items`;
- campos de título `title` o `name`;
- URL en `permalink_url`, `url` o `href`.

## Ejecución

```bash
python scripts/reconcile_catalogs.py
```

## Estrategia de coincidencia

1. Alias confirmado en `config/title_aliases.csv`.
2. Título normalizado exacto.
3. Título base sin marcadores como live, remix o version.
4. Similitud difusa con umbral conservador.
5. Casos múltiples o dudosos pasan a revisión; no se fuerzan.

El emparejamiento es uno a uno para evitar que una pista de SoundCloud cubra artificialmente varias canciones de DistroKid.
