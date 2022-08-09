# Generate new angular project + prettier`

- This script forces you to use pnpm as package manager.
- It will install prettier as dev dependency
- It adds `format` script in `package.json`
- It performs a prettier on the project and commit it.

1. `wget https://gist.githubusercontent.com/kasir-barati/5590e1420aedc2dc321571b4b9df7d33/raw/3cea996dd1a0a8895517c5fa1148ac6d027cfcf8/create-angular-app -O /usr/local/bin/create-angular-app`
2. `sudo chmod +x /usr/local/bin/create-angular-app`
3. `create-angular-app project-name --package-manager pnpm`

# Future improvements:

- Installing and configuring husky
