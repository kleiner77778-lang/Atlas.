FROM kivy/buildozer:latest

USER root

RUN apt-get update && apt-get install -y \
    autoconf \
    libtool \
    pkg-config \
    libffi-dev \
    libltdl-dev \
    && rm -rf /var/lib/apt/lists/*

# Patche check_root direkt im Buildozer-Python-Code, damit nie wieder eine Abfrage kommt
RUN python3 -c "import buildozer; import inspect, os; path = os.path.dirname(inspect.getfile(buildozer)); print(path)" | xargs -I {} find {} -name "__init__.py" -exec sed -i 's/def check_root(self):/def check_root(self):\n        return/g' {} +

WORKDIR /app

COPY . .

ENV BUILDOZER_ALLOW_ROOT=1
ENV CI=1
