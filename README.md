# wallpapers/lab

¡Hola! Bienvenido a **Wallpapers Labs**. 🎨

Hacemos arte abstracto para tu pantalla: fondos de pantalla gratis, en alta resolución, para escritorio y mobile. Sin registro y sin marca de agua.

## Dónde encontrar los fondos

Cada fondo nuevo se publica en X, en [@wallpaperslabs](https://x.com/wallpaperslabs), con su link de descarga. Seguinos para ver el próximo antes que nadie.

☕ Próximamente en [Cafecito](https://cafecito.app/wallpaperslabs): colecciones de wallpapers con variantes únicas.

## Apoyar el proyecto

Si algún fondo te gustó y querés dar una mano, podés invitarnos un [Cafecito](https://cafecito.app/wallpaperslabs). ☕

## Cómo está organizado el repo

- `index.html`: la landing, publicada con GitHub Pages. Se arma desde la URL:
  - `?collection=galaxy&wallpaper=1/2/3/4`: fecha, nombre y la grilla con esos fondos.
  - `?collection=galaxy`: la colección entera.
  - `?collection=galaxy&wallpaper=2`: el detalle de un fondo, con sus descargas.
- `wallpapers.json`: las colecciones publicadas; la más nueva va primero.
- Las imágenes no viven en el repo: cada colección es una [release](https://github.com/mamiaro/wallpapersLabs/releases) con el mismo nombre, con `<coleccion>-<n>-vista.jpg`, `<coleccion>-<n>-escritorio.jpg` y `<coleccion>-<n>-mobile.jpg`.
- `herramientas/subir-coleccion/`: doble clic en `subir-coleccion.command` para subir una carpeta de fondos (crea la release, sube los archivos y actualiza `wallpapers.json`). Necesita [GitHub CLI](https://cli.github.com) con `gh auth login`.
- Logo y favicons de la página, en la raíz.

Los fondos son gratis para uso personal.

---

Creado por [@feeeedda](https://x.com/feeeedda).
