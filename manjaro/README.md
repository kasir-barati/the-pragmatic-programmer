# Install apps

1. `wget https://gist.githubusercontent.com/kasir-barati/db54aeefb3f5c78f80a49b856b5ce4a7/raw/manjaro-apps`.
2. `/bin/bash manjaro-apps`.

# Keyboard layout

## 1 option

- fcitx: https://youtu.be/lJoXhS4EUJs?si=4jrUJaAyxuSCeEBp

## 2 option

1. Press win+d and type `mangaro-setting-manager` and hit enter.
2. Go to "Locale Settings" and "Language Packages" and install your languages.
3. `localectl list-x11-keymap-layouts` to see available layouts.
   - e.x. ir, de, us, etc.
4. `vim ~/.i3/config`.
   - Add this line at the end of it: `exec "setxkbmap -layout us,de,ir -option 'grp:alt_shift_toggle'"`.

# Audio

## AudioRelay

1. `sudo pamac install audiorelay`.
2. Change the "Audio Device" in AudioRelay app to "Monitor of Built-in Audio Analog Stereo".
3. Install it on your Andriod device.

## Connect your headphone to the laptop:

- `sudo pacman -S pulseaudio-bluetooth`.

## Change audio:

1. `amixer --card=0`.
2. `amixer -c 0 set Speaker playback 100% unmute`.
   - You can change "Speaker" to whatever its name is.

- [Config your system to work with bluetooth automatically](https://forum.manjaro.org/t/howto-bluetooth-headphones-paired-but-no-sound-after-a-while/33141).
