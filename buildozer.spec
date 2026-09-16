[app]
# ... deine normalen App-Einstellungen (title, package.name, etc.) ...

# Requirements fest definieren (Cython in Version 0.29.x erzwingen)
requirements = python3,kivy==2.2.1

# Android SDK/NDK Einstellungen fixieren
android.api = 33
android.minapi = 21
android.ndk = 25b

# WICHTIG: Threads begrenzen, um Abbrüche bei autoconf/Python-JIT zu verhindern
android.num_build_threads = 2

# Akzeptiere Lizenzen automatisch
android.accept_sdk_license = True
