# UOC_Visualizacion_de_datos_PEC2_Parte3

Ridgeline de la temperatura media diaria de 2025 en 35 países europeos (representados por su capital).

## Datos

- **Fuente:** [Open-Meteo Historical Weather API](https://open-meteo.com/en/docs/historical-weather-api), variable `temperature_2m_mean` (°C), del 1 de enero al 31 de diciembre de 2025.
- **Origen:** reanálisis ERA5 de Copernicus Climate Change Service / ECMWF. Hersbach, H. et al. (2023): *ERA5 hourly data on single levels from 1940 to present*. Copernicus Climate Change Service (C3S) Climate Data Store (CDS). DOI: [10.24381/cds.adbb2d47](https://doi.org/10.24381/cds.adbb2d47).
- **Licencia:** CC BY 4.0.
- **Banderas:** [flagcdn.com](https://flagcdn.com) (dominio público).

Para regenerar `data/temperaturas-2025.json` y `data/flags/`:

```bash
python3 scripts/update_data.py
```

## Publicación

Sitio estático: basta con activar GitHub Pages sobre la rama `main` (carpeta raíz).
# UOC_Visualizacion_de_datos_PEC2_Parte3
