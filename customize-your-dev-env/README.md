# Customize your Dev Env

1. Open `~/.bashrc`/`~/.zshrc`:
2. Add the following:
   ```bash
   alias dcps='docker compose ps --format "table {{.Service}}\t{{.Status}}\t{{.Ports}}"'
   alias dcd='docker compose down -v'
   alias dcu='docker compose up --build -d'
   alias fcount='ls -1 | wc -l' # File count
   alias rfcount='find . -type f | wc -l' # Recursive file count
   ```
3. Save it and then `source ~/.bashrc`/`source ~/.zshrc`.
