# Install apps

1. `wget https://gist.githubusercontent.com/kasir-barati/db54aeefb3f5c78f80a49b856b5ce4a7/raw/manjaro-apps`
2. `/bin/bash manjaro-apps`

# Connect your headphone to the laptop:
  - `sudo pacman -S pulseaudio-bluetooth`

# Change audio:

1. `amixer --card=0`
2. `amixer -c 0 set Speaker playback 100% unmute`
   - You can change "Speaker" to whatever its name is
