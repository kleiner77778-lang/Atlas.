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

# Arbeitsverzeichnis im bestehenden Home-Ordner von 'user' anlegen und Rechte vergeben
WORKDIR /home/user/app
RUN chown -R user:user /home/user/app

# Auf den bereits existierenden Nicht-Root-Benutzer 'user' wechseln
USER user

COPY --chown=user:user . .

RUN buildozer --version
