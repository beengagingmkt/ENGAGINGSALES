#!/usr/bin/env bash
# Instala o Garimpo (motor de busca + gateway do WhatsApp) e abre o painel.
set -e
cd "$(dirname "$0")"
command -v python3 >/dev/null || { echo "Preciso do Python 3.9 ou mais novo (python3)."; exit 1; }
chmod +x garimpo Garimpo.command 2>/dev/null || true
python3 install.py
echo
read -r -p "Abrir o Garimpo agora? [S/n] " ans
case "${ans:-S}" in
  [nN]*) echo "Quando quiser: ./garimpo start" ;;
  *) exec ./garimpo start ;;
esac
