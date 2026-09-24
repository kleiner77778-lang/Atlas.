[app]

# (str) Title of your application
title = Atlas E-Lkw Tracker

# (str) Package name
package.name = elkwtracker

# (str) Package domain (needed for android/ios packaging)
package.domain = org.elkw

# (str) Source code where the main.py lives
source.dir = .

# (list) Source files to include (let empty to include all the files)
source.include_exts = py,png,jpg,kv,atlas,json

# (str) Application versioning
version = 1.0.0

# (list) Application requirements
requirements = python3,kivy,requests,pyjnius,openssl,urllib3,chardet,certifi,idna,charset-normalizer

# (str) Custom application icon
icon.filename = %(source.dir)s/icon.png

# (str) Supported orientations (portrait, landscape, sensorLandscape, all)
orientation = portrait

# (bool) Indicate if the application should be fullscreen or not
fullscreen = 0

# (list) Permissions
android.permissions = INTERNET, ACCESS_FINE_LOCATION, ACCESS_COARSE_LOCATION, FOREGROUND_SERVICE, WAKE_LOCK

# (list) Features
android.features = android.hardware.location.gps

# (int) Target & Min Android API
android.api = 33
android.minapi = 21

# (str) Android NDK version to use
android.ndk = 25b

# (bool) If True, then skip building the ndk recipes
android.skip_update = False

# (bool) If True, accept all SDK licences
android.accept_sdk_license = True

# (str) Nur für arm64-v8a bauen (spart Zeit und verhindert Build-Timeouts)
android.archs = arm64-v8a

[buildozer]
# (int) Log level (0 = error only, 1 = info, 2 = debug (with command output))
log_level = 2

# (int) Display warning if buildozer is run as root (0 = disable, 1 = enable)
warn_on_root = 1
