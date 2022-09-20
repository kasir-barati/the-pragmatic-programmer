# Generate new NestJS

- This script checks if pnpm is selected as package manager, otherwise it throw an error
- It updates `format` script in `package.json`
- It performs a prettier on the project and commit it.

1. `sudo wget https://gist.githubusercontent.com/kasir-barati/7877d6668188fad0b0765ef8ffe32a05/raw/my-nest -O /usr/local/bin/my-nest`
2. `sudo chmod +x /usr/local/bin/my-nest`
3. `my-nest project-name --package-manager pnpm`

# Future improvements:

- Installing and configuring husky
