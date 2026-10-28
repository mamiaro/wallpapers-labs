#!/usr/bin/env python3
"""Sube una colección de wallpapers a una release de GitHub y la suma a wallpapers.json.

Uso:  python3 subir_coleccion.py [carpeta] [--coleccion galaxy] [--nombre Galaxia]

La carpeta tiene los fondos tal como salen de los kits (png o jpg). Los horizontales se toman
como escritorio y los verticales como mobile; se emparejan por nombre, ignorando palabras como
studio, mobile, escritorio o 5k (wallpaper-1-galaxia-studio.png va con wallpaper-1-galaxia-mobile.png).

Por cada fondo se suben a la release <coleccion>:
  <coleccion>-<n>-escritorio.jpg, <coleccion>-<n>-mobile.jpg y <coleccion>-<n>-vista.jpg (1600 px)
y wallpapers.json de main suma la colección arriba de todo, con la fecha de hoy.
Necesita sips (viene con macOS) y gh (cli.github.com) con sesión iniciada.
"""
import argparse
import base64
import datetime
import json
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

REPO = "mamiaro/wallpapersLabs"
RAMA = "main"
LANDING = "https://mamiaro.github.io/wallpapersLabs/"
EXTENSIONES = {".png", ".jpg", ".jpeg", ".webp", ".tif", ".tiff", ".heic"}
CALIDAD_DESCARGA = 95   # jpg de escritorio y mobile
CALIDAD_VISTA = 82      # jpg liviano para la landing
ANCHO_VISTA = 1600
# Palabras que se sacan del nombre para emparejar escritorio con mobile.
PALABRAS_FORMATO = r"(studio|5k|4k|qhd|uhd|fhd|escritorio|desktop|mobile|movil|móvil|celular|phone)"


def correr(cmd, **kw):
    return subprocess.run(cmd, check=True, text=True, capture_output=True, **kw).stdout


def gh(*args, entrada=None):
    return correr(["gh", *args], input=entrada)


def medidas(ruta):
    salida = correr(["sips", "-g", "pixelWidth", "-g", "pixelHeight", str(ruta)])
    w = int(re.search(r"pixelWidth: (\d+)", salida).group(1))
    h = int(re.search(r"pixelHeight: (\d+)", salida).group(1))
    return w, h


def a_jpg(origen, destino, calidad, ancho=None):
    cmd = ["sips", "-s", "format", "jpeg", "-s", "formatOptions", str(calidad)]
    if ancho:
        cmd += ["--resampleWidth", str(ancho)]
    correr(cmd + [str(origen), "--out", str(destino)])


def peso(ruta):
    mb = ruta.stat().st_size / 1_000_000
    texto = f"{mb:.0f}" if mb >= 10 else f"{mb:.1f}".replace(".", ",")
    return f"{texto} MB"


def clave(ruta):
    nombre = re.sub(PALABRAS_FORMATO, "", ruta.stem.lower())
    return re.sub(r"[-_ .]+", "-", nombre).strip("-")


def orden_natural(texto):
    return [int(p) if p.isdigit() else p for p in re.split(r"(\d+)", texto)]


def a_slug(texto):
    texto = re.sub(r"\s+wallpaper$", "", texto.strip(), flags=re.I).lower()
    for a, b in zip("áéíóúüñ", "aeiouun"):
        texto = texto.replace(a, b)
    return re.sub(r"[^a-z0-9]+", "-", texto).strip("-")


def preguntar(texto, defecto=""):
    extra = f" [{defecto}]" if defecto else ""
    respuesta = input(f"{texto}{extra}: ").strip()
    return respuesta or defecto


def elegir_carpeta():
    if sys.platform == "darwin":
        try:
            ruta = correr(["osascript", "-e",
                           'POSIX path of (choose folder with prompt "Elegí la carpeta con los fondos")'])
            return ruta.strip()
        except subprocess.CalledProcessError:
            pass
    return input("Arrastrá acá la carpeta con los fondos y apretá Enter: ").strip().strip("'\"").replace("\\ ", " ")


def leer_json():
    datos = json.loads(gh("api", f"repos/{REPO}/contents/wallpapers.json?ref={RAMA}"))
    contenido = json.loads(base64.b64decode(datos["content"]).decode("utf-8") or "{}")
    if not isinstance(contenido, dict):
        contenido = {}
    return contenido, datos["sha"]


def guardar_json(colecciones, sha, mensaje):
    texto = json.dumps(colecciones, ensure_ascii=False, indent=2) + "\n"
    cuerpo = json.dumps({
        "message": mensaje,
        "content": base64.b64encode(texto.encode("utf-8")).decode("ascii"),
        "sha": sha,
        "branch": RAMA,
    })
    gh("api", "-X", "PUT", f"repos/{REPO}/contents/wallpapers.json", "--input", "-", entrada=cuerpo)


def main():
    parser = argparse.ArgumentParser(description="Sube una colección de wallpapers a GitHub.")
    parser.add_argument("carpeta", nargs="?")
    parser.add_argument("--coleccion", help="nombre corto para la URL, ej. galaxy")
    parser.add_argument("--nombre", help="nombre que se ve en la landing, ej. Galaxia")
    args = parser.parse_args()

    for programa, ayuda in (("sips", "sips viene con macOS; este script es para Mac."),
                            ("gh", "Instalá GitHub CLI desde https://cli.github.com y corré: gh auth login")):
        if not shutil.which(programa):
            sys.exit(f"No encontré {programa}. {ayuda}")
    if subprocess.run(["gh", "auth", "status"], capture_output=True).returncode != 0:
        sys.exit("gh no tiene sesión iniciada. Abrí la Terminal, corré: gh auth login  y volvé a probar.")

    carpeta = Path(args.carpeta or elegir_carpeta()).expanduser()
    if not carpeta.is_dir():
        sys.exit(f"No encontré la carpeta '{carpeta}'.")

    # Emparejar escritorio (horizontal) y mobile (vertical) por nombre.
    grupos = {}
    for ruta in sorted(carpeta.iterdir()):
        if ruta.suffix.lower() not in EXTENSIONES or ruta.name.startswith("."):
            continue
        w, h = medidas(ruta)
        tipo = "escritorio" if w >= h else "mobile"
        grupo = grupos.setdefault(clave(ruta), {})
        if tipo in grupo:
            print(f"Aviso: '{ruta.name}' y '{grupo[tipo].name}' parecen el mismo fondo; uso el primero.")
            continue
        grupo[tipo] = ruta
    completos = []
    for k in sorted(grupos, key=orden_natural):
        g = grupos[k]
        if "escritorio" in g and "mobile" in g:
            completos.append(g)
        else:
            falta = "mobile" if "escritorio" in g else "escritorio"
            nombre = next(iter(g.values())).name
            print(f"Aviso: a '{nombre}' le falta la versión {falta}; no se sube.")
    if not completos:
        sys.exit("No encontré pares de escritorio y mobile en esa carpeta.")

    colecciones, sha = leer_json()
    slug = a_slug(args.coleccion or preguntar("Nombre corto de la colección (va en la URL)", a_slug(carpeta.name)))
    if not slug:
        sys.exit("La colección necesita un nombre.")
    existente = colecciones.get(slug, {})
    nombre = args.nombre or preguntar("Nombre que se ve en la landing",
                                      existente.get("nombre") or slug.replace("-", " ").title())
    tags = [t.strip() for t in preguntar("Tags para estos fondos, separados por coma (Enter: ninguno)").split(",") if t.strip()]
    fondos = existente.get("fondos", {})
    primero = max((int(n) for n in fondos if n.isdigit()), default=0) + 1
    numeros = list(range(primero, primero + len(completos)))

    print(f"\nVoy a subir {len(completos)} fondos a la colección '{slug}' ({nombre}), "
          f"numerados del {numeros[0]} al {numeros[-1]}.")
    if preguntar("¿Sigo? (s/n)", "s").lower() not in ("s", "si", "sí", "y"):
        sys.exit("Cancelado; no se subió nada.")

    # La release se llama igual que la colección.
    if subprocess.run(["gh", "release", "view", slug, "-R", REPO], capture_output=True).returncode != 0:
        print(f"Creando la release '{slug}'...")
        gh("release", "create", slug, "-R", REPO, "--target", RAMA, "--title", nombre,
           "--notes", f"Colección {nombre} de wallpapers/lab. Se ve en {LANDING}?collection={slug}")

    hoy = datetime.date.today().isoformat()
    with tempfile.TemporaryDirectory() as tmp:
        tmp = Path(tmp)
        for n, g in zip(numeros, completos):
            base = f"{slug}-{n}"
            archivos = {}
            for tipo in ("escritorio", "mobile"):
                origen, destino = g[tipo], tmp / f"{base}-{tipo}.jpg"
                if origen.suffix.lower() in (".jpg", ".jpeg"):
                    shutil.copyfile(origen, destino)
                else:
                    a_jpg(origen, destino, CALIDAD_DESCARGA)
                archivos[tipo] = destino
            vista = tmp / f"{base}-vista.jpg"
            a_jpg(g["escritorio"], vista, CALIDAD_VISTA, ANCHO_VISTA)
            print(f"Subiendo {nombre} {n} ({g['escritorio'].name})...")
            gh("release", "upload", slug, "-R", REPO, "--clobber",
               str(archivos["escritorio"]), str(archivos["mobile"]), str(vista))
            w, h = medidas(archivos["escritorio"])
            mw, mh = medidas(archivos["mobile"])
            fondos[str(n)] = {
                "fecha": hoy,
                "tags": tags,
                "escritorio": f"{w} × {h} · {peso(archivos['escritorio'])}",
                "mobile": f"{mw} × {mh} · {peso(archivos['mobile'])}",
            }

    # La colección recién subida queda primera: es la que abren el logo y "Ver más fondos".
    fondos = dict(sorted(fondos.items(), key=lambda kv: orden_natural(kv[0])))
    nuevas = {slug: {"nombre": nombre, "fondos": fondos}}
    nuevas.update((k, v) for k, v in colecciones.items() if k != slug)
    guardar_json(nuevas, sha, f"Suma {len(numeros)} fondos a {nombre}")

    link = f"{LANDING}?collection={slug}&wallpaper=" + "/".join(str(n) for n in numeros)
    print("\nListo. En un par de minutos se ve en la landing:")
    print(link)


if __name__ == "__main__":
    try:
        main()
    except subprocess.CalledProcessError as e:
        sys.exit(f"Falló: {' '.join(e.cmd)}\n{e.stderr or e.stdout}")
