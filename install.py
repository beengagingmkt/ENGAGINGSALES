#!/usr/bin/env python3
"""Instalador do Engaging Sales.

Baixa, confere e instala os dois componentes de terceiros que o Engaging Sales usa, direto das fontes originais:

  1. Motor de busca do Google Maps  (Mahanaicoach/google-maps-scraper-kit, MIT)
     preso a um commit exato: o Git confere o conteúdo pelo hash do commit.
  2. Gateway do WhatsApp            (aldinokemal/go-whatsapp-web-multidevice, MIT)
     binário oficial da release, conferido pelo SHA-256 abaixo (o mesmo que o projeto publica).

Não precisa de sudo, só usa a biblioteca padrão do Python e não instala nada fora desta pasta.
Uso:  python3 install.py          (instala ou confere)
"""
import hashlib, os, platform, shutil, subprocess, sys, tempfile, zipfile

ROOT = os.path.dirname(os.path.abspath(__file__))

KIT_REPO = "https://github.com/Mahanaicoach/google-maps-scraper-kit.git"
KIT_COMMIT = "15dd80b584dfeab550271ba383b540af8f44d1d2"  # 2026-11-02

GOWA_REPO = "aldinokemal/go-whatsapp-web-multidevice"
GOWA_VERSION = "9.9.0"
GOWA_SHA256 = {  # checksums publicados na release v9.9.0 (checksums.txt e checksums-macos.txt)
    "darwin_amd64": "ead32e63f9338019f315d6e70159b44154bc6fc75637faa2c4deae2b90e38398",
    "darwin_arm64": "ac1d77adb15a31de558b8dca7871d0fbc7d05fdaab82ed49d9de357cdfe0e1b6",
    "linux_amd64": "b3a0afc3cd2721198de60032a21f7f0aa78e58d0a478a7b00566d1604b7aa574",
    "linux_arm64": "f9c2f376fc0c82ae1c2148615cf8f92505eeb8959786d7d61f9919d513646880",
}

BROWSERS = ["/Applications/Google Chrome.app", "/Applications/Chromium.app", "/Applications/Microsoft Edge.app",
            "/Applications/Brave Browser.app"]
BROWSER_BINS = ["google-chrome", "google-chrome-stable", "chromium", "chromium-browser", "microsoft-edge", "brave-browser"]


def say(msg=""):
    print(msg, flush=True)


def die(msg):
    say(f"\n✗ {msg}")
    sys.exit(1)


def run(args, **kw):
    return subprocess.run(args, capture_output=True, text=True, **kw)


def platform_key():
    system = {"Darwin": "darwin", "Linux": "linux"}.get(platform.system())
    arch = {"arm64": "arm64", "aarch64": "arm64", "x86_64": "amd64", "AMD64": "amd64"}.get(platform.machine())
    if not system or not arch or f"{system}_{arch}" not in GOWA_SHA256:
        die(f"Sistema não suportado ({platform.system()} {platform.machine()}). O Engaging Sales roda em macOS e Linux. "
            "No Windows, use o WSL2 (Ubuntu) e rode o instalador lá dentro.")
    return f"{system}_{arch}", system, arch


def check_basics():
    if sys.version_info < (3, 9):
        die(f"Preciso do Python 3.9 ou mais novo (você tem {platform.python_version()}).")
    for tool in ("git", "curl"):
        if not shutil.which(tool):
            die(f"Não achei o '{tool}'. Instale (no Mac: xcode-select --install) e rode de novo.")
    if not shutil.which("rsync"):
        say("• rsync não encontrado: só será necessário se você for publicar os diagnósticos num servidor.")
    found = any(os.path.exists(p) for p in BROWSERS) or any(shutil.which(b) for b in BROWSER_BINS)
    if found:
        say("✓ Navegador Chromium encontrado: o motor de busca vai usar ele.")
    else:
        say("• Nenhum Chrome, Chromium, Edge ou Brave encontrado. Na primeira busca o motor baixa o Chrome for Testing "
            "(cerca de 100 MB, do site oficial do Google).")


def install_kit():
    dest = os.path.join(ROOT, "vendor", "kit")
    head = run(["git", "-C", dest, "rev-parse", "HEAD"]).stdout.strip() if os.path.isdir(os.path.join(dest, ".git")) else ""
    if head == KIT_COMMIT:
        say(f"✓ Motor de busca já instalado (commit {KIT_COMMIT[:7]}).")
        return
    say(f"→ Baixando o motor de busca (google-maps-scraper-kit, commit {KIT_COMMIT[:7]})…")
    if os.path.isdir(dest):
        shutil.rmtree(dest)
    os.makedirs(dest)
    for step in (["git", "init", "-q"], ["git", "remote", "add", "origin", KIT_REPO],
                 ["git", "fetch", "-q", "--depth", "1", "origin", KIT_COMMIT], ["git", "checkout", "-q", "--detach", "FETCH_HEAD"]):
        r = run(step, cwd=dest)
        if r.returncode:
            die(f"Falhou ao baixar o motor ({' '.join(step[:2])}): {r.stderr.strip()[:300]}")
    got = run(["git", "rev-parse", "HEAD"], cwd=dest).stdout.strip()
    if got != KIT_COMMIT:
        shutil.rmtree(dest, ignore_errors=True)
        die(f"O commit baixado ({got[:7]}) não é o esperado ({KIT_COMMIT[:7]}). Parei por segurança.")
    say("✓ Motor de busca instalado e conferido.")


def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def install_gateway(key, system, arch):
    gdir = os.path.join(ROOT, "gateway")
    binp = os.path.join(gdir, "bin", "gowa")
    verf = os.path.join(gdir, "VERSION")
    if os.path.isfile(binp) and os.path.isfile(verf) and open(verf).read().strip() == GOWA_VERSION:
        say(f"✓ Gateway do WhatsApp já instalado (v{GOWA_VERSION}).")
        return
    name = f"whatsapp_{GOWA_VERSION}_{key}.zip"
    url = f"https://github.com/{GOWA_REPO}/releases/download/v{GOWA_VERSION}/{name}"
    say(f"→ Baixando o gateway do WhatsApp (go-whatsapp-web-multidevice v{GOWA_VERSION}, {key})…")
    tmp = tempfile.mkdtemp(prefix="engaging-gateway-")  # pasta nova e vazia: nada baixado roda a partir daqui
    try:
        zpath = os.path.join(tmp, name)
        r = run(["curl", "-fsSL", "--retry", "3", "-m", "300", "-o", zpath, url])
        if r.returncode:
            die(f"Não consegui baixar {url}: {r.stderr.strip()[:200]}")
        got = sha256(zpath)
        if got != GOWA_SHA256[key]:
            die(f"O checksum do gateway não bate!\n  esperado {GOWA_SHA256[key]}\n  recebido {got}\nParei por segurança.")
        say("✓ Checksum SHA-256 conferido com o publicado pelo projeto.")
        out = os.path.join(tmp, "x")
        with zipfile.ZipFile(zpath) as z:
            for n in z.namelist():  # impede caminho fora da pasta (zip slip)
                if os.path.isabs(n) or ".." in n.split("/"):
                    die("Arquivo zip com caminho suspeito. Parei por segurança.")
            z.extractall(out)
        cands = [os.path.join(out, n) for n in os.listdir(out) if n.startswith((f"{system}-{arch}", f"{system}_{arch}"))]
        cands = [c for c in cands if os.path.isfile(c)]
        if not cands:
            die("Não achei o programa dentro do zip do gateway.")
        os.makedirs(os.path.join(gdir, "bin"), exist_ok=True)
        os.makedirs(os.path.join(gdir, "data"), exist_ok=True)
        shutil.copyfile(cands[0], binp)
        os.chmod(binp, 0o755)
        if system == "darwin":
            run(["xattr", "-d", "com.apple.quarantine", binp])
        t = run([binp, "rest", "--help"], cwd=os.path.join(gdir, "data"), timeout=30)
        if t.returncode:
            die("O gateway baixou mas não executa neste computador: " + (t.stderr or t.stdout)[:200])
        with open(verf, "w") as f:
            f.write(GOWA_VERSION)
        say("✓ Gateway do WhatsApp instalado.")
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


def main():
    say("Engaging Sales: instalador\n")
    key, system, arch = platform_key()
    check_basics()
    os.makedirs(os.path.join(ROOT, "data"), exist_ok=True)
    install_kit()
    install_gateway(key, system, arch)
    say("\n✓ Tudo pronto.")
    say("  Para abrir o Engaging Sales:  ./engaging-sales start")
    say("  Na primeira vez ele mostra o aviso importante e já pede o QR code do WhatsApp.")


if __name__ == "__main__":
    main()
