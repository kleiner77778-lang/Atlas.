FROM kivy/buildozer:latest

USER root

# Systempakete installieren
RUN apt-get update && apt-get install -y \
    autoconf \
    libtool \
    pkg-config \
    libffi-dev \
    libltdl-dev \
    sudo \
    && rm -rf /var/lib/apt/lists/*

# Benutzer 'user' sauber anlegen
RUN useradd -m -u 1000 -s /bin/bash user && \
    echo "user ALL=(ALL) NOPASSWD:ALL" >> /etc/sudoers

# Standardbenutzer und Arbeitsverzeichnis setzen
USER user
WORKDIR /home/user/app

COPY --chown=user:user . .

RUN buildozer --version
