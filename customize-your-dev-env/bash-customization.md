# Create file and its parent directory

1. `sudo vim /usr/local/bin/my-touch`
2. Then write the following script in it

   ```bash
   #!/bin/bash
   mkdir -p "$(dirname "$1")" && touch "$1"
   ```

3. `sudo chmod +x /usr/local/bin/my-touch`
4. `my-touch /path/to/the/heaven/file.js`
