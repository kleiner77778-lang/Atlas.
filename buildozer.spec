[app]

# (str) Title of your application
title = Atlas E-Lkw Tracker

# (str) Package name
package.name = elkwtracker

# (str) Package domain (needed for android packaging)
package.domain = org.elkw

# (str) Source code where the main.py lives
source.dir = .

# (list) Source files to include
source.include_exts = py,png,jpg,kv,atlas,json

# (str) Application versioning
version = 1.0.0

# (list) Application requirements
# WICHTIG: cryptography, openssl und certifi sind zwingend fuer Telegram HTTPS
requirements = python3,kivy==2.2.1,requests,urllib3,openssl,certifi,cryptography,pyjnius

# (str) Custom application icon
Fallback: Wenn icon.png im Ordner fehlt, diese Zeile mit # auskommentieren!
icon.filename = %(source.dir)s/icon.png

# (str) Supported orientations
orientation = portrait

# (bool) Indicate if the application should be fullscreen
fullscreen = 1

# (list) Permissions
android.permissions = INTERNET, ACCESS_FINE_LOCATION, ACCESS_COARSE_LOCATION

# (int) Target Android API
android.api = 33

# (int) Minimum API required
android.minapi = 24

# (str) Android NDK version
android.ndk = 25b

# (bool) Accept SDK license automatically
android.accept_sdk_license = True

# (list) The Android archs to build for (arm64-v8a ist perfekt fuer moderna Smartphones wie S22+)
android.archs = arm64-v8a

[buildozer]

# (int) Log level (2 = debug info)
log_level = 2

# (int) Display warning if buildozer is run as root
warn_on_root = 1
