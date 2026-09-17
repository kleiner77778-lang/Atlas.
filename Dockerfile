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

# Alte 'user'-Einträge entfernen und 'builder' mit UID 1000 neu anlegen
RUN touch /etc/subuid /etc/subgid && \
    userdel -r user 2>/dev/null || true && \
    groupadd -g 1000 builder && \
    useradd -m -u 1000 -g builder -s /bin/bash builder && \
    chown -R builder:builder /home/builder

USER builder
WORKDIR /home/builder/app

COPY --chown=builder:builder . .

RUN buildozer --version
