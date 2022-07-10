# Break long lines

## Faster way

- `code $HOME/.config/Code\ -\ OSS/User/settings.json`
  - `code $HOME/.config/Code/User/settings.json`
- Paste these key values:
  ```json
  "diffEditor.wordWrap": "on",
  "editor.wordWrap": "on",
  "editor.wordWrapColumn": 70
  ```

## Secure way

- Press `ctrl+,`
- Type `wordWrap`
- From drop down choose `on`
- Enter 70 in Word Wrap Column
