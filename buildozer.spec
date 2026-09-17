[app]

# (str) Title of your application
title = Atlas

# (str) Package name
package.name = atlas

# (str) Package domain (needed for android/ios packaging)
package.domain = org.test

# (str) Application versioning
version = 0.1

# (str) Source code where the main.py live
source.dir = .

# (list) Source files to include (let empty to include all the files)
source.include_exts = py,png,jpg,kv,atlas

# (list) Application requirements
# comma separated e.g. requirements = sqlite3,kivy
requirements = python3,kivy==2.2.1

# (str) Supported orientation (one of landscape, sensorLandscape, portrait or all)
orientation = portrait

# (bool) Indicate if the application should be fullscreen or not
fullscreen = 0

# (list) Permissions
android.permissions = INTERNET

# (int) Target Android API, should be as high as possible.
android.api = 33

# (int) Minimum API your APK will support.
android.minapi = 21

# (str) Android NDK version to use
android.ndk = 25b

# (bool) Accept SDK license automatically
android.accept_sdk_license = True

# (list) The Android archs to build for (Nur 64-Bit verhindert Toolchain-Konflikte):
android.archs = arm64-v8a

# (int) Begrenzt die Threads beim Bauen (verhindert RAM-Mangel/Timeouts):
android.num_build_threads = 2

[buildozer]

# (int) Log level (0 = error only, 1 = info, 2 = debug (with command output))
log_level = 2

# (int) Display warning if buildozer is run as root (0 = false, 1 = true)
warn_on_root = 1
