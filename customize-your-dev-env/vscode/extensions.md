# General

```bash
code --install-extension alefragnani.project-manager
code --install-extension apollographql.vscode-apollo
code --install-extension arturock.gitstash
code --install-extension dbaeumer.vscode-eslint
code --install-extension eamodio.gitlens
code --install-extension esbenp.prettier-vscode
code --install-extension firsttris.vscode-jest-runner
code --install-extension github.copilot
code --install-extension github.copilot-chat
code --install-extension graphql.vscode-graphql-syntax
code --install-extension jonathanlewis.vs-code-gen-mongo-id
code --install-extension kangping.protobuf
code --install-extension ms-python.debugpy
code --install-extension ms-python.python
code --install-extension ms-python.vscode-pylance
code --install-extension ms-vsliveshare.vsliveshare
code --install-extension netcorext.uuid-generator
code --install-extension saoudrizwan.claude-dev
code --install-extension streetsidesoftware.code-spell-checker
code --install-extension tamasfe.even-better-toml
code --install-extension wayou.vscode-todo-highlight
code --install-extension prisma.prisma
code --install-extension enosislabs.rainysnap
code --install-extension dpkshrma.insert-iso-timestamp
code --install-extension wallabyjs.quokka-vscode
```

## Customize

<details>
<summary>Todo config in <code>~/.config/Code/User/settings.json</code></summary>

```json
"todohighlight.isEnable": true,
"todohighlight.isCaseSensitive": true,
"todohighlight.keywords": [
    "DEBUG:",
    "REVIEW:",
    {
    "text": "README:",
    "color": "white",
    "backgroundColor": "#007acc",
    "borderRadius": "2px",
    "fontWeight": "bold",
    "overviewRulerColor": "grey"
    },
    {
        "text": "NOTE:",
        "color": "black",
        "backgroundColor": "#0b66da",
        "borderRadius": "2px",
        "fontWeight": "bold",
        "overviewRulerColor": "grey"
    },
    {
        "text": "IMPORTANT:",
        "color": "black",
        "backgroundColor": "#8353dc",
        "borderRadius": "4px",
        "fontWeight": "bold",
        "overviewRulerColor": "grey"
    },
    {
        "text": "HACK:",
        "color": "#000",
        "isWholeLine": false,
    },
    {
        "text": "TODO:",
        "color": "red",
        "border": "1px solid red",
        "borderRadius": "2px", // NOTE: using borderRadius along with `border` or you will see nothing change
        "backgroundColor": "rgba(0,0,0,.2)",
        //other styling properties goes here ... 
    }
],
```

</details>
