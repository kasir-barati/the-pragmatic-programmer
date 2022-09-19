# Generate new angular project + prettier`

- This script won't uses pnpm as package manager by default. use `--use-pnpm` flag explicitly
- This script won't uses typescript by default. use `--typescript` flag explicitly
- It will install prettier as dev dependency
- It adds `format` script in `package.json`
- It performs a prettier on the project and commit it.

1. `sudo wget https://gist.githubusercontent.com/kasir-barati/83fc3e23326d1cb1dc93ac790595286d/raw/my-next -O /usr/local/bin/my-next`
2. `sudo chmod +x /usr/local/bin/my-next`
3. `my-next project-name --typescript --use-pnpm`

# Future improvements:

- Installing and configuring husky
