# Move from VSCode to Neovim

> [!CAUTION]
>
> I had to still keep using VSCode for Jupyter Notebook. So I disabled quite a lot of its features in `~/.config/Code/User/settings.json`:
> ```json
>   "files.watcherExclude": {
>    "**/node_modules/**": true,
>    "**/.git/**": true,
>    "**/dist/**": true,
>    "**/build/**": true,
>    "**/.vscode/**": true,
>    "**/__pycache__/**": true
>  },
>  "search.exclude": {
>    "**/node_modules": true,
>    "**/dist": true,
>    "**/build": true,
>    "**/.next": true,
>        "**/.git": true,
>    "**/__pycache__": true,
>    "**/.DS_Store": true
>  },
>  "editor.minimap.enabled": false,
>  "editor.codeLens": false,
>  "workbench.statusBar.visible": false,
>  "js/ts.validate.enabled": false,
>  "editor.undoStackSize": 1000,
>  "workbench.activityBar.location": "hidden",
>  "workbench.editor.showTabs": "single",
>  "workbench.editor.enablePreview": false,
>  "git.enabled": false,
> ```

> [!TIP]
>
> Use https://vim-adventures.com/ to first build your muscle memory and learn the basics while enjoying your time.

1. Install Neovim: https://neovim.io/doc/install/
2. Goto `~/.config/nvim` and type `nvim .`.

## Equivalent of VSCode Explorer

1. Press `Esc`.
2. Type `:Ex`.
   - To create a new File just press `shift + 5`.
   - Now let's create `init.lua` (something akin to `.bashrc` which is called everytime we open a new bash).

## Common Shortcuts

- Cut next 3 lines: press `Esc` and then `3dd`.
- To create a new file in Explorer press `shift + 5`.
- To create a new dir in Explorer press `Esc + d`.
- To select everything when you are in the first line press `shift + v` and then press `shift + g`.
- To jump to line #4 press `Esc` and then `:4`.
