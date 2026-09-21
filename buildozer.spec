[app]
title = Atlas
package.name = atlas
package.domain = org.test
source.dir = .
source.include_exts = py,png,jpg,kv,atlas
source.exclude_patterns = license, lambda*, kivy/tests/*
version = 0.1
requirements = python3,kivy,requests,pyjnius

# Automatische Sensor-Drehung (Gültiger Buildozer-Wert)
orientation = sensor

fullscreen = 0

# Standort- & GPS-Berechtigungen sowie Hintergrunddienst
android.permissions = INTERNET, ACCESS_FINE_LOCATION, ACCESS_COARSE_LOCATION, FOREGROUND_SERVICE, WAKE_LOCK

# GPS Hardware-Feature explizit aktivieren
android.features = android.hardware.location.gps

android.api = 33
android.minapi = 21
android.ndk = 25b
android.private_storage = True
android.archs = arm64-v8a

[buildozer]
log_level = 2
warn_on_root = 1
