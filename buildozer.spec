[app]

title = Atlas
package.name = atlastracker
package.domain = org.atlas
source.dir = .
source.include_exts = py,png,jpg,kv,atlas,json
icon.filename = %(source.dir)s/icon.png
version = 1.0.0

requirements = python3,kivy==2.2.1,requests,pyjnius,openssl,urllib3,certifi,idna,charset-normalizer

# Gültige Werte: portrait, landscape, sensorPortrait, sensorLandscape
orientation = all

fullscreen = 0
android.permissions = INTERNET, ACCESS_FINE_LOCATION, ACCESS_COARSE_LOCATION, FOREGROUND_SERVICE, WAKE_LOCK
android.features = android.hardware.location.gps
android.api = 33
android.minapi = 21
android.ndk = 25b
android.accept_sdk_license = True
android.archs = arm64-v8a

[buildozer]
log_level = 2
warn_on_root = 1
