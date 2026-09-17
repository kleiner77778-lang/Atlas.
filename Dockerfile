FROM kivy/buildozer:latest

USER root

# Systempakete installieren
RUN apt-get update && apt-get install -y \
    autoconf \
    libtool \
    pkg-config \
    libffi-dev \
    libltdl-dev \
    && rm -rf /var/lib/apt/lists/*

# Direkt auf den bestehenden Benutzer wechseln und Arbeitsverzeichnis setzen
USER user
WORKDIR /home/user/app

# Dateien als Benutzer kopieren
COPY --chown=user . .

RUN buildozer --version
