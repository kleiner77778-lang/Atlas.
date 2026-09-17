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

# Benutzer ohne feste UID/GID anlegen
RUN useradd -m -s /bin/bash builder

USER builder
WORKDIR /home/builder/app

COPY --chown=builder:builder . .

RUN buildozer --version
