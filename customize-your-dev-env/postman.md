> [!CAUTION]
>
> Nowadays I prefer to write tests in Jest and other tools like that to free myself from manually testing my RESTful APIs.

# Install postman

1.  `wget https://dl.pstmn.io/download/latest/linux64`
2.  `tar xfz postman-linux-x64.tar.gz`
3.  `sudo mv Postman /opt`
4.  `cd ~` and `vim .local/share/applications/postman.desktop`

    ```desktop
    [Desktop Entry]
    Encoding=UTF-8
    Name=Postman
    Exec=postman
    Icon=/opt/Postman/app/resources/app/assets/icon.png
    Terminal=false
    Path=/opt/Postman
    Exec=/opt/Postman/Postman
    Type=Application
    Categories=Development;
    ```

5.  Reload desktop env:
    - Gnome: `gnome-shell --replace & disown`
    - XFCE: `xfce4-panel -r && xfwm4 --replace`
    - [ref](https://www.makeuseof.com/tag/refresh-linux-desktop-without-rebooting/#:~:text=Just%20hold%20down%20Ctrl%20%2B%20Alt,the%20desktop%20will%20be%20refreshed.)
