#!/usr/bin/env bash
# Instala o Engaging Sales (motor de busca + gateway do WhatsApp) e abre o painel.
set -e
cd "$(dirname "$0")"
command -v python3 >/dev/null || { echo "Preciso do Python 3.9 ou mais novo (python3)."; exit 1; }
chmod +x engaging-sales "Engaging Sales.command" 2>/dev/null || true
python3 install.py
echo
read -r -p "Abrir o Engaging Sales agora? [S/n] " ans
case "${ans:-S}" in
  [nN]*) echo "Quando quiser: ./engaging-sales start" ;;
  *) exec ./engaging-sales start ;;
esac
