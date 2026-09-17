USER root
RUN apt-get update && apt-get install -y \
 autoconf \
 libtool \
 pkg-config \
 libffi-dev \
 libltdl-dev \
 && rm -rf /var/lib/apt/lists/*
USER kivy
WORKDIR /home/kivy/app
COPY --chown=kivy:kivy . .
RUN buildozer --version
