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
- Las imágenes no viven en el repo: cada colección es una [release](https://github.com/mamiaro/wallpapersLabs/releases) cuyo tag es el nombre de la colección (`galaxy`) y cuyo título es el nombre que se ve en la landing (`Galaxia`). Cada fondo lleva `wallpaper-<n>-studio.png` (escritorio), `wallpaper-<n>-mobile.png` (mobile), `wallpaper-<n>-studio-preview.jpg` (la vista de la landing) y `wallpaper-<n>-mobile-preview.jpg`. La landing lee la release desde la API de GitHub: para publicar alcanza con crear la release, sin tocar el repo.
- Logo y favicons de la página, en la raíz.

Los fondos son gratis para uso personal.

---

Creado por [@feeeedda](https://x.com/feeeedda).
