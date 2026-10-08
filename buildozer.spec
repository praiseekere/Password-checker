[app]

title = Password Checker
package.name = passwordchecker
package.domain = org.passwordchecker

source.dir = .
source.include_exts = py,png,jpg,jpeg,kv,atlas

version = 1.0

requirements = python3,kivy

orientation = portrait

fullscreen = 0


[buildozer]

log_level = 2


[app:android]

android.api = 35
android.minapi = 21
android.archs = arm64-v8a, armeabi-v7a

android.permissions = INTERNET


[buildozer:android]

android.accept_sdk_license = True
