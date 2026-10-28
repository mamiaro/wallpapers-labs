#!/bin/bash
# Doble clic para subir una carpeta de fondos a la landing (release de GitHub + wallpapers.json).
cd "$(dirname "$0")" || exit 1

pausa_y_salir() {
  echo
  read -n 1 -s -r -p "Presioná una tecla para cerrar..."
  exit "${1:-0}"
}

if ! command -v python3 >/dev/null 2>&1; then
  echo "No encontré python3. Instalalo (por ejemplo desde python.org) y volvé a ejecutar."
  pausa_y_salir 1
fi
if ! command -v gh >/dev/null 2>&1; then
  echo "No encontré GitHub CLI (gh)."
  echo "Bajalo de https://cli.github.com, instalalo y en la Terminal corré: gh auth login"
  pausa_y_salir 1
fi

python3 subir_coleccion.py "$@"
pausa_y_salir $?
