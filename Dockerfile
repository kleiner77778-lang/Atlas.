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

# Eigenen Nicht-Root-Benutzer 'builder' anlegen
RUN groupadd -g 1000 builder && \
    useradd -m -u 1000 -g builder -s /bin/bash builder

USER builder
WORKDIR /home/builder/app

COPY --chown=builder:builder . .

RUN buildozer --version
