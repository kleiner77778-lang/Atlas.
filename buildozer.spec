[app]

# (str) Title of your application
title = Atlas

# (str) Package name
package.name = atlastracker

# (str) Package domain (needed for android/ios packaging)
package.domain = org.atlas

# (str) Source code where the main.py live
source.dir = .

# (list) Source files to include
source.include_exts = py,png,jpg,kv,atlas,json

# (str) Custom application icon
icon.filename = %(source.dir)s/icon.png

# (str) Application versioning
version = 1.0.0

# (list) Application requirements
requirements = python3,kivy==2.2.1,requests,pyjnius,openssl,urllib3,certifi,idna,charset-normalizer

# (str) Supported orientations (portrait, landscape, sensor, sensorLandscape)
orientation = sensor

# (bool) Indicate if the application should be fullscreen or not
fullscreen = 0

# (list) Permissions
android.permissions = INTERNET, ACCESS_FINE_LOCATION, ACCESS_COARSE_LOCATION, FOREGROUND_SERVICE, WAKE_LOCK

# (list) Features
android.features = android.hardware.location.gps

# (int) Target Android API
android.api = 33

# (int) Minimum API required
android.minapi = 21

# (str) Android NDK version
android.ndk = 25b

# (bool) Accept SDK licenses automatically
android.accept_sdk_license = True

# (str) Nur für arm64-v8a bauen
android.archs = arm64-v8a

[buildozer]

# (int) Log level
log_level = 2

# (int) Display warning if buildozer is run as root
warn_on_root = 1
