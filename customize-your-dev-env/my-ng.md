# Generate new angular project + prettier`

1. `sudo vim /usr/local/bin/my-ng`
2. Then write the following script in it

   ```bash
    #!/bin/bash
    isPackageManagerSpecified="false";

    for ((i=1; i<=$#; i++))
    do
      nextArgumentIndex=$((i+1));
      if [[ "${!i}" == "--package-manager" ]] && [[ "${!nextArgumentIndex}" == "pnpm" ]];
      then
        isPackageManagerSpecified="true";
      fi
    done

    if [[ $isPackageManagerSpecified != "true" ]]
    then
      echo "Please specify package manager";
      exit 1;
    fi

    ng "$@"

    cd "$1"
    pnpm add -D prettier

    wget https://gist.githubusercontent.com/kasir-barati/2bcdeea964f88712eca171adb3fbd979/raw/441f66a604f90efbfd2f1ac4fd2fb9ec88c8b892/.prettierrc

    wget https://gist.githubusercontent.com/kasir-barati/8b32cf62e69e6f87a6bed899eefe1cb5/raw/83f21438587f85d1419f6cbc7205771e2030765e/.prettierignore

    # Add format script
    node -e "const { readFileSync, writeFileSync } = require('fs'); const packageJson = JSON.parse(readFileSync('package.json', 'utf-8')); packageJson.scripts = { ...packageJson.scripts, \"format\": \"prettier -w . -u\" }; writeFileSync('package.json', JSON.stringify(packageJson))"

    pnpm format

    git add .
    git commit -m "cleanup: prettified"
   ```

3. `sudo chmod +x /usr/local/bin/my-ng`
4. `my-ng project-name --package-manager pnpm`
