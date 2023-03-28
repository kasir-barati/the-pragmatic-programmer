# Install apps

1. `wget https://gist.githubusercontent.com/kasir-barati/db54aeefb3f5c78f80a49b856b5ce4a7/raw/manjaro-apps`
2. `/bin/bash manjaro-apps`

# Keyboard layout
1. Press win+d and type `mangaro-setting-manager` and hit enter
2. Go to "Locale Settings" and "Language Packages" and install your languages
3. Install [gxkb](https://man.archlinux.org/man/gxkb.1.en) and configure it as it says in its `README.md`

# Connect your headphone to the laptop:

- `sudo pacman -S pulseaudio-bluetooth`

## Change audio:

1. `amixer --card=0`
2. `amixer -c 0 set Speaker playback 100% unmute`
   - You can change "Speaker" to whatever its name is

- [Config your system to work with bluetooth automatically](https://forum.manjaro.org/t/howto-bluetooth-headphones-paired-but-no-sound-after-a-while/33141)
