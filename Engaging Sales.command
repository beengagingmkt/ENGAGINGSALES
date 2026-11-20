#!/bin/bash
# No macOS: dois cliques abrem o Engaging Sales (instala o que faltar na primeira vez).
cd "$(dirname "$0")" || exit 1
exec ./engaging-sales start
