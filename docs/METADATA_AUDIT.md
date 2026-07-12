# Auditoría de portadas y metadata

## Objetivo

Detectar pistas de SoundCloud sin portada o con metadata incompleta y producir una cola segura de corrección.

## Ejecución

```bash
python scripts/audit_soundcloud_metadata.py
```

## Salidas

- `reports/soundcloud_metadata_audit.csv`: auditoría completa.
- `reports/soundcloud_repair_queue.csv`: solo registros incompletos, ordenados por prioridad y reproducciones.
- `reports/soundcloud_metadata_summary.json`: conteos globales.

## Prioridades

- `critical`: falta la portada.
- `high`: faltan al menos dos campos centrales.
- `medium`: falta metadata complementaria.
- `complete`: no se detectan vacíos.

## Política de reparación

La auditoría es automática. La escritura en SoundCloud no debe ejecutarse hasta confirmar:

1. portada correcta por canción;
2. género y etiquetas;
3. créditos y descripción;
4. que una versión no suplante a otra;
5. que el cambio use el ID exacto de la pista.

El sistema genera la cola; la edición externa debe ser aprobada y trazable.
