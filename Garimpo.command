#!/bin/bash
# No macOS: dois cliques abrem o Garimpo (instala o que faltar na primeira vez).
cd "$(dirname "$0")" || exit 1
exec ./garimpo start
