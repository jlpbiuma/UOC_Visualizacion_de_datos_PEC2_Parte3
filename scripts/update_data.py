"""Descarga la temperatura media diaria de 2025 de cada capital europea y la guarda en data/temperaturas-2025.json.

Fuente: Open-Meteo Historical Weather API (reanálisis ERA5 de Copernicus/ECMWF), CC BY 4.0.
Cada país se representa por su capital. Las banderas se guardan en data/flags/ para no
depender de flagcdn.com al cargar la página.
"""
import json
import pathlib
import urllib.parse
import urllib.request

API = "https://archive-api.open-meteo.com/v1/archive"
YEAR = "2025"
OUT = pathlib.Path(__file__).resolve().parent.parent / "data" / "temperaturas-2025.json"
FLAGS = OUT.parent / "flags"

# (código ISO 3166-1 alfa-2, país, capital, latitud, longitud)
COUNTRIES = [
    ("al", "Albania", "Tirana", 41.33, 19.82),
    ("de", "Alemania", "Berlín", 52.52, 13.40),
    ("at", "Austria", "Viena", 48.21, 16.37),
    ("be", "Bélgica", "Bruselas", 50.85, 4.35),
    ("ba", "Bosnia y Herzegovina", "Sarajevo", 43.86, 18.41),
    ("bg", "Bulgaria", "Sofía", 42.70, 23.32),
    ("hr", "Croacia", "Zagreb", 45.81, 15.98),
    ("dk", "Dinamarca", "Copenhague", 55.68, 12.57),
    ("sk", "Eslovaquia", "Bratislava", 48.15, 17.11),
    ("si", "Eslovenia", "Liubliana", 46.06, 14.51),
    ("es", "España", "Madrid", 40.42, -3.70),
    ("ee", "Estonia", "Tallin", 59.44, 24.75),
    ("fi", "Finlandia", "Helsinki", 60.17, 24.94),
    ("fr", "Francia", "París", 48.86, 2.35),
    ("gr", "Grecia", "Atenas", 37.98, 23.73),
    ("hu", "Hungría", "Budapest", 47.50, 19.04),
    ("ie", "Irlanda", "Dublín", 53.35, -6.26),
    ("is", "Islandia", "Reikiavik", 64.15, -21.94),
    ("it", "Italia", "Roma", 41.90, 12.50),
    ("lv", "Letonia", "Riga", 56.95, 24.11),
    ("lt", "Lituania", "Vilna", 54.69, 25.28),
    ("lu", "Luxemburgo", "Luxemburgo", 49.61, 6.13),
    ("mk", "Macedonia del Norte", "Skopie", 42.00, 21.43),
    ("mt", "Malta", "La Valeta", 35.90, 14.51),
    ("no", "Noruega", "Oslo", 59.91, 10.75),
    ("nl", "Países Bajos", "Ámsterdam", 52.37, 4.90),
    ("pl", "Polonia", "Varsovia", 52.23, 21.01),
    ("pt", "Portugal", "Lisboa", 38.72, -9.14),
    ("gb", "Reino Unido", "Londres", 51.51, -0.13),
    ("cz", "República Checa", "Praga", 50.08, 14.44),
    ("ro", "Rumanía", "Bucarest", 44.43, 26.10),
    ("rs", "Serbia", "Belgrado", 44.79, 20.45),
    ("se", "Suecia", "Estocolmo", 59.33, 18.07),
    ("ch", "Suiza", "Berna", 46.95, 7.45),
    ("ua", "Ucrania", "Kiev", 50.45, 30.52),
]


def download(url):
    req = urllib.request.Request(url, headers={"User-Agent": "temperaturas-europa-pages", "Accept": "*/*"})
    with urllib.request.urlopen(req) as res:
        return res.read()


def main():
    query = urllib.parse.urlencode({
        "latitude": ",".join(str(c[3]) for c in COUNTRIES),
        "longitude": ",".join(str(c[4]) for c in COUNTRIES),
        "start_date": f"{YEAR}-01-01",
        "end_date": f"{YEAR}-12-31",
        "daily": "temperature_2m_mean",
        "timezone": "auto",
    })
    results = json.loads(download(f"{API}?{query}"))

    FLAGS.mkdir(parents=True, exist_ok=True)
    countries = []
    for (code, name, capital, *_), res in zip(COUNTRIES, results):
        flag = FLAGS / f"{code}.svg"
        if not flag.exists():
            flag.write_bytes(download(f"https://flagcdn.com/{code}.svg"))
        countries.append({
            "code": code,
            "name": name,
            "capital": capital,
            "temps": [round(t, 1) if t is not None else None for t in res["daily"]["temperature_2m_mean"]],
        })

    OUT.write_text(json.dumps({
        "year": int(YEAR),
        "start": results[0]["daily"]["time"][0],
        "countries": countries,
    }, ensure_ascii=False, separators=(",", ":")))
    print(f"{len(countries)} países guardados ({results[0]['daily']['time'][0]} → {results[0]['daily']['time'][-1]})")


if __name__ == "__main__":
    main()
