# Música — Iyari Gomez

Repositorio canónico del catálogo musical de **Iyari Gomez / BlackMamba RECORDS**.

## Estado del catálogo

| Fuente | Lanzamientos | Canciones |
|---|---:|---:|
| DistroKid | 230 | 274 |
| SoundCloud (perfil público) | 1,034 pistas | Pendiente de normalización |

## Archivos

- `catalog/distrokid_catalog.csv`: una fila por canción, listo para Excel, análisis y cruces.
- `catalog/distrokid_catalog.json`: estructura lanzamiento → canciones para automatización.
- `sources/distrokid_lyrics_export.txt`: fuente textual original utilizada para reconstruir el catálogo.

## Criterio canónico

El conteo de DistroKid proviene del listado detallado de letras, porque incluye las canciones internas de cada lanzamiento y evita las omisiones causadas por capturas con desplazamiento.

### Resumen DistroKid

- Lanzamientos: **230**
- Canciones: **274**
- Singles: **194**
- Lanzamientos con varias canciones: **36**

## Próxima fase

Normalizar títulos y cruzar DistroKid contra SoundCloud para clasificar:

- publicado en ambas plataformas;
- exclusivo de SoundCloud;
- distribuido por DistroKid;
- duplicados, versiones y títulos reutilizados;
- pendiente de distribución.
