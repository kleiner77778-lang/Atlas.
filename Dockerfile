FROM kivy/buildozer:latest

USER root

RUN apt-get update && apt-get install -y \
    autoconf \
    libtool \
    pkg-config \
    libffi-dev \
    libltdl-dev \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY . .

ENV BUILDOZER_ALLOW_ROOT=1
ENV CI=1
